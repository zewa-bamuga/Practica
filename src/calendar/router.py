from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.functions import is_user_authenticated
from src.auth.models import User
from src.calendar.functions import get_historical_events, get_historical_event_by_id
from src.calendar.schemas import ShortHistoricalEvents, HistoricalEventDetail
from src.database import get_async_session

router = APIRouter(
    prefix="/calendar",
    tags=["Calendar"]
)


@router.get("/events", response_model=List[ShortHistoricalEvents])
async def get_short_events(user: User = Depends(is_user_authenticated),
                           session: AsyncSession = Depends(get_async_session)):
    return await get_historical_events(session)


@router.get("/events/{event_id}", response_model=HistoricalEventDetail)
async def get_event_by_id(
        event_id: int,
        user: User = Depends(is_user_authenticated),
        session: AsyncSession = Depends(get_async_session)
):
    return await get_historical_event_by_id(session, event_id)
