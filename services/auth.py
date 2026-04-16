import os
from fastapi import HTTPException, Header
from typing import Optional




#Authorizes the user based on an API key sent in the header
def get_api_key(x_api_key: Optional[str] = Header(None)):
    auth_key_check = os.environ.get("AUTH_KEY")
    if not x_api_key or x_api_key != auth_key_check:
        raise HTTPException(status_code=401, detail="Invalid API key.")
    return x_api_key
