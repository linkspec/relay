from datetime import datetime, timedelta, UTC
from uuid import uuid4

from caldav import DAVClient
from icalendar import Calendar, Event

from config import settings


# Connect
client = DAVClient(
    url=settings.caldav_url,
    username=settings.caldav_username,
    password=settings.caldav_password,
)

principal = client.principal()
calendar = principal.calendars()[0]

print(f"Connected to: {calendar}")


def create_event(summary: str, start: datetime, end: datetime):
    cal = Calendar()
    cal.add("prodid", "-//Relay//EN")
    cal.add("version", "2.0")

    event = Event()
    event.add("uid", str(uuid4()))
    event.add("summary", summary)
    event.add("dtstart", start)
    event.add("dtend", end)
    event.add("dtstamp", datetime.now(UTC))
    event.add("description", "Created by Relay")

    cal.add_component(event)

    calendar.save_event(cal.to_ical())

    print(f"Created: {summary}")


now = datetime.now(UTC).replace(second=0, microsecond=0)

create_event(
    "Relay Test 1",
    now + timedelta(hours=1),
    now + timedelta(hours=2),
)

create_event(
    "Relay Test 2",
    now + timedelta(days=1, hours=3),
    now + timedelta(days=1, hours=4),
)

create_event(
    "Relay Test 3",
    now + timedelta(days=2, hours=5),
    now + timedelta(days=2, hours=6),
)

print("\nEvents in calendar:\n")

for cal_event in calendar.events():

    data = Calendar.from_ical(cal_event.data)

    for component in data.walk():
        if component.name != "VEVENT":
            continue

        print("--------------------------------")
        print("Summary :", component.get("SUMMARY"))
        print("Start   :", component.get("DTSTART").dt)
        print("End     :", component.get("DTEND").dt)
        print("UID     :", component.get("UID"))