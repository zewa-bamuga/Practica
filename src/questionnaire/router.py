from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.functions import is_user_authenticated
from src.auth.models import User
from src.database import get_async_session
from src.questionnaire.functions import get_survey_questions
from src.questionnaire.models import UserResponse
from src.questionnaire.schemas import UserResponseSchema, SurveyBaseSchema

router = APIRouter(
    prefix="/Survey",
    tags=["Survey"]
)

@router.get("/questions", response_model=list[SurveyBaseSchema])
async def questions_handler(user: User = Depends(is_user_authenticated), session: AsyncSession = Depends(get_async_session)):
    return await get_survey_questions(session)

@router.post("/submit-response")
async def submit_survey_response(
    response: UserResponseSchema,
    user: User = Depends(is_user_authenticated),
    session: AsyncSession = Depends(get_async_session)
):
    try:
        async with session() as async_session:
            user_response = UserResponse(**response.dict(), user_id=user.id)
            async_session.add(user_response)
            await async_session.commit()
            return {"message": "Ответ успешно сохранен"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Произошла ошибка при сохранении ответа")