from typing import List

from pydantic import BaseModel


class AllQuestionSchema(BaseModel):
    id: int
    title: str
    description: str
    price: float
    rating: float

    class Config:
        orm_mode = True


class ShortQuestionSchema(BaseModel):
    id: int
    title: str
    short_description: str
    price: float
    rating: float

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
