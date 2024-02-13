from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.functions import is_user_authenticated
from src.auth.models import User
from src.database import get_async_session
from src.questionnaire.functions import get_survey_questions, process_survey_response
from src.questionnaire.schemas import UserResponseSchema, SurveyBaseSchema

router = APIRouter(
    prefix="/survey",
    tags=["Survey"]
)


@router.get("/questions", response_model=list[SurveyBaseSchema])
async def questions_handler(user: User = Depends(is_user_authenticated),
                            session: AsyncSession = Depends(get_async_session)):
    return await get_survey_questions(session)


@router.post("/submit-response")
async def submit_survey_response(response: UserResponseSchema, user: User = Depends(is_user_authenticated),
                                 async_session: AsyncSession = Depends(get_async_session)):
    await process_survey_response(response, user, async_session)
    return {"message": "Ответы успешно сохранены"}
