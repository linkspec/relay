from datetime import datetime
from pydantic import BaseModel

class CalendarEvent(BaseModel):
    id: str | None = None

    title: str

    start: datetime

    end: datetime

    description: str | None = None

    location: str | None = None

    all_day: bool = False