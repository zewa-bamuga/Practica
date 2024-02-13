from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.functions import is_user_authenticated
from src.auth.models import User, RouteRating
from src.database import get_async_session
from src.questionnaire.schemas import ShortQuestionSchema, AllQuestionSchema, RouteRatingCreate
from src.walk.functions import get_user_questions, get_question_by_id

router = APIRouter(
    prefix="/walk",
    tags=["Walk"]
)


@router.get("/user-questions", response_model=list[ShortQuestionSchema])
async def user_questions_route(user: User = Depends(is_user_authenticated),
                               async_session: AsyncSession = Depends(get_async_session)):
    return await get_user_questions(user, async_session)


@router.get("/questions/{question_id}", response_model=AllQuestionSchema)
async def question_by_id_route(question_id: int,
                               user: User = Depends(is_user_authenticated),
                               async_session: AsyncSession = Depends(get_async_session)):
    return await get_question_by_id(question_id, user, async_session)


@router.post("/walk/route-rating")
async def create_route_rating(route_rating_create: RouteRatingCreate, user: User = Depends(is_user_authenticated),
                              async_session: AsyncSession = Depends(get_async_session)):
    async with async_session as session:
        existing_rating = await session.execute(
            select(RouteRating).filter(
                RouteRating.user_id == user.id,
                RouteRating.survey_id == route_rating_create.survey_id
            )
        )
        existing_rating = existing_rating.scalar()

        if existing_rating:
            existing_rating.rating = route_rating_create.rating
        else:
            new_rating = RouteRating(
                user_id=user.id,
                survey_id=route_rating_create.survey_id,
                rating=route_rating_create.rating
            )
            session.add(new_rating)

        await session.commit()

        return {"message": "Оценка успешно добавлена или обновлена"}


# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0MUBtYWlsLnJ1IiwiZXhwIjoxNzA3ODIxNTk0fQ.YYa6noorJLyWSEVZgwRf0BJ6CZIXLXr5Tw3laHO-a-M
# 1 5 7
# 1 - 1 2 3 4 24
# 5 - 11 12
# 7 - 17 15 16
