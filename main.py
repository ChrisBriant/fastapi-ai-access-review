from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import os
import dotenv
from services.auth import get_api_key
from data.schemas import UserAnswerListSchema, AiResponseSchema, InputQuestionSchema
from services.ai_prompts import get_role_assignments, get_interview_question_answer
from services.utils import extract_markdown
import bleach



# #LOAD ENVIRONMENT
dotenv_file = ".env"
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

app = FastAPI()

allowed_origins = ["http://localhost:5173", "http://127.0.0.1:5500", "https://aiam-certification.chrisbriant.uk"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # React app origin
    allow_credentials=True,                   # must be True for cookies
    allow_methods=["*"],
    allow_headers=["*"],
)

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter


@app.post("/get-groups", response_model = AiResponseSchema)
async def get_groups(user_answers : UserAnswerListSchema, api_key: str = Depends(get_api_key)):
    question_data = [
        {
            "id": item.id,
            "text": item.text,
            "answer": item.answer
        }
        for item in user_answers.user_answers
    ]
    ai_response = get_role_assignments(question_data)
    #ai_response = [{'role_name': 'platform_administrator', 'justification': 'Selected because the user describes organization-wide administration of the central identity platform, full user lifecycle management, group oversight, role assignment, policy creation and enforcement, approval of privileged and administrative access, daily access operations, and management of role definitions. In the documented role set, platform_administrator is the only defined role with full system access to manage users, groups, roles, policies, configurations, and settings. Narrower roles such as user_administrator, groups_administrator, policy_administrator, role_assignment_manager, and access_request_approver would still not cover role definition management or full platform administration end-to-end. Assigning this single role is therefore the least-privilege fit available within the defined roles for the responsibilities stated. '}]
    try:
        role_list = AiResponseSchema.model_validate(ai_response)
    except Exception as e:
        print("Bad response from AI", e)
        raise HTTPException(status_code=400,detail="Unable to generate role data")

    return role_list


@app.post("/ask-interview-question", response_model = str)
@limiter.limit("10/minute")
async def ask_interview_question(question : InputQuestionSchema, request : Request):
    #Check that the origin is valid
    origin = request.headers.get("origin")

    if not origin in allowed_origins:
        raise HTTPException(status_code=403,detail="Unknown Origin")
    
    cleaned_question = bleach.clean(question.question, tags=[], attributes={}, strip=True)

    try:
        ai_response = get_interview_question_answer(cleaned_question)
        # ai_response = """
        #     In my experience, I ensure an environment is up-to-date and audit ready by combining controlled deployment, monitoring, access governance, and documentation.

        #     I’ve used Terraform Infrastructure-as-Code to provision Azure environments consistently, and Azure DevOps CI/CD pipelines with approval-based workflows across development and production environments, which helps keep deployments controlled and repeatable . I also configure monitoring and alerting through Azure Log Analytics to support operational visibility and incident response .

        #     From an access and audit perspective, I’ve managed identity provisioning and permission governance in Microsoft Entra ID, performed privilege reviews and access audits across enterprise platforms, and developed PowerShell automation to streamline access reviews and compliance reporting . I’ve also produced access control documentation and implementation guidance, which is important for demonstrating how access is managed and reviewed .

        #     In addition, I’ve managed TLS certificate lifecycle activities, including issuing and renewing certificates, and I’ve previously conducted security audits and ensured compliance with IT policies  .

        # """
        #print("THIS IS THE AI RESPONSE", ai_response)
        #markdown_response = extract_markdown(ai_response)
    except Exception as e:
        print("An error occurred getting the response to the interview question.", e)
        raise HTTPException(status_code=400,detail="An error occurred getting the response to the interview question.")
    return ai_response