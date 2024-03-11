from typing import Optional

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import HistoricalEvent
from src.calendarr.schemas import ShortHistoricalEvents, HistoricalEventDetail


async def get_historical_events(session: AsyncSession):
    async with session as async_session:
        query = select(HistoricalEvent)
        events = await async_session.execute(query)
        return [ShortHistoricalEvents(id=historical_events.id, name=historical_events.name,
                                      event_date=historical_events.event_date) for historical_events in
                events.scalars().all()]


async def get_historical_event_by_id(session: AsyncSession, event_id: int) -> HistoricalEvent:
    async with session as async_session:
        try:
            query = select(HistoricalEvent).filter(HistoricalEvent.id == event_id)
            event = await async_session.execute(query)
            event_detail = event.scalars().first()
            if not event_detail:
                raise HTTPException(status_code=404, detail="Event not found")
            return event_detail
        except Exception as e:
            raise HTTPException(status_code=500, detail="Internal Server Error")