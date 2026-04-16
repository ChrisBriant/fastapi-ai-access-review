from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import dotenv
from services.auth import get_api_key
from data.schemas import UserAnswerListSchema, AiResponseSchema
from services.ai_prompts import get_role_assignments



# #LOAD ENVIRONMENT
dotenv_file = ".env"
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React app origin
    allow_credentials=True,                   # must be True for cookies
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/test", response_model = str)
async def test():
    return "Hello - This is a test"


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