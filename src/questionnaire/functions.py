from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import Survey, User, UserResponse
from src.questionnaire.schemas import SurveyBaseSchema, UserResponseSchema


async def get_survey_questions(session: AsyncSession):
    async with session as async_session:
        query = select(Survey)
        result = await async_session.execute(query)
        surveys = result.scalars().all()
        return [SurveyBaseSchema(id=survey.id, category=survey.category) for survey in surveys]


async def process_survey_response(response: UserResponseSchema, user: User, async_session: AsyncSession):
    async with async_session as session:
        for survey_id in response.survey_id:
            existing_response = await session.execute(
                select(UserResponse)
                .filter(UserResponse.user_id == user.id)
                .filter(UserResponse.survey_id == survey_id)
            )
            if existing_response.scalar():
                raise HTTPException(status_code=400,
                                    detail=f"Пользователь уже ответил на вопросы опроса с id {survey_id}")

            result = await session.execute(
                select(Survey).filter(Survey.id == survey_id)
            )
            if not result.scalar():
                raise HTTPException(status_code=404,
                                    detail=f"Результаты запроса для опроса с id {survey_id} отсутствуют")

            survey = await async_session.get(Survey, survey_id)
            if not survey:
                raise HTTPException(status_code=404, detail=f"Указанный опрос с id {survey_id} не найден")

            user_response = UserResponse(user_id=user.id, survey_id=survey.id)
            session.add(user_response)
        await session.commit()
