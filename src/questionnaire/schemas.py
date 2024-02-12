from typing import List

from pydantic import BaseModel

class QuestionSchema(BaseModel):
    id: int
    text: str
    class Config:
        orm_mode = True

class SurveyBaseSchema(BaseModel):
    id: int
    category: str
    class Config:
        orm_mode = True

class SurveySchema(SurveyBaseSchema):
    class Config:
        orm_mode = True

class UserResponseSchema(BaseModel):
    survey_id: List[int]