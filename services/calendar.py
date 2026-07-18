from datetime import datetime

from caldav import DAVClient

from config import settings
from models.calendar import CalendarEvent
from icalendar import Calendar


class CalendarService:
    def __init__(self) -> None:
        self._client = DAVClient(
            url=settings.caldav_url,
            username=settings.caldav_username,
            password=settings.caldav_password,
        )

        self._principal = self._client.principal()

        calendars = self._principal.calendars()

        if not calendars:
            raise RuntimeError("No calendars found.")

        # For now, just use the first calendar.
        # Later we can support multiple calendars.
        self._calendar = calendars[0]

    def get_events(
        self,
        start: datetime | None = None,
        end: datetime | None = None,
    ) -> list[CalendarEvent]:
        """
        Return all events, optionally filtered by a date range.
        """
        caldav_events = self._calendar.events()

        events = []

        for caldav_event in caldav_events:
            events.append(self._to_model(caldav_event))

        return events

    def get_event(
        self,
        event_id: str,
    ) -> CalendarEvent:
        """
        Return a single event by its UID.
        """
        raise NotImplementedError

    def create_event(
        self,
        event: CalendarEvent,
    ) -> CalendarEvent:
        """
        Create a new calendar event.
        """
        raise NotImplementedError

    def update_event(
        self,
        event: CalendarEvent,
    ) -> CalendarEvent:
        """
        Update an existing calendar event.
        """
        raise NotImplementedError

    def delete_event(
        self,
        event_id: str,
    ) -> bool:
        """
        Delete an event by its UID.
        """
        raise NotImplementedError
    
    def _to_model(self, caldav_event) -> CalendarEvent:

        calendar = Calendar.from_ical(caldav_event.data)

        for component in calendar.walk():
            if component.name != "VEVENT":
                continue

            return CalendarEvent(
                id=str(component.get("UID")),
                title=str(component.get("SUMMARY")),
                description=str(component.get("DESCRIPTION", "")),
                location=str(component.get("LOCATION", "")),
                start=component.get("DTSTART").dt,
                end=component.get("DTEND").dt,
                all_day=False,
            )

        raise ValueError("Calendar object contained no VEVENT")