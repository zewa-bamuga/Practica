from datetime import date

from pydantic import BaseModel


class ShortHistoricalEvents(BaseModel):
    id: int
    name: str
    event_date: date

    class Config:
        orm_mode = True


class HistoricalEventDetail(BaseModel):
    id: int
    name: str
    event_date: date
    event_description: str

    class Config:
        orm_mode = True
