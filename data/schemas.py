from pydantic import BaseModel, ConfigDict, computed_field, RootModel
from datetime import datetime
from typing import List, TypeVar, Optional, Generic


class UserAnswerSchema(BaseModel):
    id: str
    text : str
    answer : str

class UserAnswerListSchema(BaseModel):
    user_answers : List[UserAnswerSchema]

class RoleResponseSchema(BaseModel):
    role_name: str
    justification : str

class AiResponseSchema(RootModel[List[RoleResponseSchema]]):
    pass