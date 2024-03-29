from typing import List, Optional

from pydantic import BaseModel


class AllQuestionSchema(BaseModel):
    id: int
    title: str
    description: str
    points: int
    distance: float
    time: float
    price: float
    rating: float
    image_path: str

    class Config:
        orm_mode = True


# типы данных не совпадают в function.py
class ShortQuestionSchema(BaseModel):
    id: int
    title: str
    short_description: str
    price: float
    rating: float
    image_path: str

    class Config:
        orm_mode = True


class RouteRatingCreate(BaseModel):
    question_id: int
    rating: float


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


class RouteOperationSchema(BaseModel):
    question_id: int
