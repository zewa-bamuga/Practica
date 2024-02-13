from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.functions import is_user_authenticated
from src.auth.models import User
from src.database import get_async_session
from src.questionnaire.schemas import ShortQuestionSchema, AllQuestionSchema
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

# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0MUBtYWlsLnJ1IiwiZXhwIjoxNzA3ODE4MzIyfQ.LFwJiOAXJndVYtUTS9LebfZ4fEnAP982OzkkHS1385Q
# 1 5 7
# 1 - 1 2 3 4 24
# 5 - 11 12
# 7 - 17 15 16
