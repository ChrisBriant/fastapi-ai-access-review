from openai import OpenAI
from pathlib import Path
import os
import dotenv
import json

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

dotenv_file = PROJECT_ROOT / ".env"

if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

API_KEY = os.environ.get("OPENAI_API_KEY")

client = OpenAI(api_key=API_KEY)




def get_role_assignments(questionData):
    response = client.responses.create(
        prompt={
            "id": os.environ.get("ROLE_ASSIGNMENT_PROMPT_ID"),
            "version": "2",
            "variables": {
                "user_question_answers": {
                    "type": "input_text",
                    "text": json.dumps(questionData)
                }
            }
        },
        input=[
            {
                "role": "user",
                "content":  f"""
                    You are an IAM Analyst for a technology company performing an access review.

                    The user is submitting responses to a questionnaire which is designed for assesmenet of the role assignments they are given. You are to assess the responses they have made to each of the questions and output a list of the roles they will be assigned to.

                    User Questions and Responses:
                    {questionData}

                    You must make the judgment based on the rules given in the uploaded document and the role assignment set must only include the roles defined in the uploaded document.

                    Requirements: 
                    - ONLY include roles defined in the document 
                    - DO NOT invent new roles
                    - For each assigned role, provide a justification as to why the role has been selected
                    - Make the judgement based on least privilege
                    - Do not include markdown 
                    - Output valid JSON only

                    Return ONLY valid JSON in the following format: 
                    
                    [{{ 
                    "role_name": "string", 
                    "justification" : "string" 
                    }}]
                """
            }
        ],
        reasoning={
            "summary": "auto"
        },
        tools=[
            {
            "type": "file_search",
            "vector_store_ids": [
                os.environ.get("COMPANY_POLICY_VECTOR_STORE_ID")
            ]
            }
        ],
        store=True,
        include=[
            "reasoning.encrypted_content",
            "web_search_call.action.sources"
        ]
    )

    json_str = None

    for item in response.output:
        if item.type == "message":
            for content in item.content:
                if content.type == "output_text":
                    json_str = content.text
                    break

    if json_str is None:
        raise ValueError("No JSON response found")
    
    response_dict = json.loads(json_str)

    return response_dict

def get_interview_question_answer(question):
    response = client.responses.create(
            prompt={
                "id" : os.environ.get("INTERVIEW_QUESTION_PROMPT_ID"),
                "version": "2",
                "variables": {
                "question": f"{question}"
                }
            },
            input=[
                {
                "role": "user",
                "content": [
                    {
                    "type": "input_text",
                    "text": "Please answer the question asked based on the rules in the developer message and the uploaded file."
                    }
                ]
                }
            ],
            reasoning={
                "summary": "auto"
            },
            tools=[
                {
                "type": "file_search",
                "vector_store_ids": [
                    os.environ.get("INTERVIEW_QUESTION_POLICY_VECTOR_STORE_ID")
                ]
                }
            ],
            store=True,
            include=[
                "reasoning.encrypted_content",
                "web_search_call.action.sources"
            ]
    )

    # ---- Extract text safely ----
    try:
        output = response.output

        if not output or not isinstance(output, list):
            raise ValueError("Invalid response: missing output")

        # Find first text block
        text_parts = []

        for item in output:
            content = getattr(item, "content", None)
            if not content:
                continue

            for c in content:
                text = getattr(c, "text", None)
                if isinstance(text, str):
                    text_parts.append(text)

        if not text_parts:
            raise ValueError("Invalid response: no text content found")

        result = "\n".join(text_parts).strip()

        # Final validation
        if not isinstance(result, str):
            raise TypeError("Model output is not a string")

        if result == "":
            raise ValueError("Model returned empty string")

        return result

    except Exception as e:
        raise RuntimeError(f"Failed to parse AI response: {str(e)}")


def main():
    #Testing
    #Load the question answer sets
    # file_path = PROJECT_ROOT / "testdata" / "question_answer_sets.json"
    
    # with file_path.open("r", encoding="utf-8") as f:
    #     question_answer_sets = json.load(f)
    # role_assignment_response = get_role_assignments(question_answer_sets[0])
    #print("AI Role Selection Response", role_assignment_response)

    #TEST INTERVIEW QUESTION
    try:
        response = get_interview_question_answer("What were you doing 14 years ago?")
        print("The response is", response)
    except Exception as e:
        print("An error occurred getting the response to the interview question.", e)


if __name__ == "__main__":
    main()
