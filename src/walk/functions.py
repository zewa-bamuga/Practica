from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User, UserResponse, Question, RouteRating
from src.questionnaire.schemas import ShortQuestionSchema, AllQuestionSchema, RouteRatingCreate


async def update_question_ratings(async_session: AsyncSession):
    async with async_session as session:
        questions = await session.execute(select(Question))
        for question in questions.scalars().all():
            average_rating = await session.scalar(
                select(func.avg(RouteRating.rating)).filter(RouteRating.question_id == question.id)
            )
            question.rating = average_rating or 0
        await session.commit()


async def get_user_questions(user: User, async_session: AsyncSession) -> list[ShortQuestionSchema]:
    await update_question_ratings(async_session)
    async with async_session as session:
        user_responses = await session.execute(select(UserResponse).filter(UserResponse.user_id == user.id))
        survey_ids = [user_response.survey_id for user_response in user_responses.scalars().all()]
        user_questions = await session.execute(select(Question).filter(Question.survey_id.in_(survey_ids)))
        return user_questions.scalars().all()


async def get_question_by_id(question_id: int, user: User, async_session: AsyncSession) -> AllQuestionSchema:
    await update_question_ratings(async_session)
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


async def create_route_rating(route_rating_create: RouteRatingCreate, user: User, async_session: AsyncSession):
    async with async_session as session:
        existing_rating = await session.execute(
            select(RouteRating).filter(
                RouteRating.user_id == user.id,
                RouteRating.question_id == route_rating_create.question_id
            )
        )
        existing_rating = existing_rating.scalar()
        if existing_rating:
            existing_rating.rating = route_rating_create.rating
        else:
            new_rating = RouteRating(
                user_id=user.id,
                question_id=route_rating_create.question_id,
                rating=route_rating_create.rating
            )
            session.add(new_rating)
        await session.commit()
    return {"message": "Оценка успешно добавлена или обновлена"}
