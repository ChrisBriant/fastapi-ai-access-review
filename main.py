from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import dotenv



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