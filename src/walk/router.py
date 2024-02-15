from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.functions import is_user_authenticated
from src.auth.models import User
from src.database import get_async_session
from src.questionnaire.schemas import ShortQuestionSchema, AllQuestionSchema, RouteRatingCreate
from src.walk.functions import get_user_questions, get_question_by_id, create_route_rating

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


@router.post("/route-rating")
async def create_route_rating_route(route_rating_create: RouteRatingCreate, user: User = Depends(is_user_authenticated),
                                    async_session: AsyncSession = Depends(get_async_session)):
    return await create_route_rating(route_rating_create, user, async_session)
