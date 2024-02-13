from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User, UserResponse, Question
from src.questionnaire.schemas import ShortQuestionSchema, AllQuestionSchema


async def get_user_questions(user: User, async_session: AsyncSession) -> list[ShortQuestionSchema]:
    async with async_session as session:
        user_responses = await session.execute(
            select(UserResponse).filter(UserResponse.user_id == user.id)
        )
        survey_ids = [user_response.survey_id for user_response in user_responses.scalars().all()]
        user_questions = await session.execute(
            select(Question).filter(Question.survey_id.in_(survey_ids))
        )
        return user_questions.scalars().all()


async def get_question_by_id(question_id: int, user: User, async_session: AsyncSession) -> AllQuestionSchema:
    async with async_session as session:
        user_response_query = select(UserResponse).filter(UserResponse.user_id == user.id)
        user_response_result = await session.execute(user_response_query)
        user_response = user_response_result.scalar()
        if not user_response:
            raise HTTPException(status_code=404, detail="Запись пользователя не найдена")

        survey_id = user_response.survey_id
        question_query = select(Question).filter(Question.id == question_id, Question.survey_id == survey_id)
        question_result = await session.execute(question_query)
        question = question_result.scalar()
        if not question:
            raise HTTPException(status_code=404, detail="Вы не выбрали категорию для этого запроса")

        return question
