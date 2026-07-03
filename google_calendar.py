from datetime import datetime, timedelta

from google.oauth2 import service_account
from googleapiclient.discovery import build

from config import GOOGLE_CALENDAR_ID


# -----------------------------
# Google Calendar Credentials
# -----------------------------

SCOPES = [
    "https://www.googleapis.com/auth/calendar.readonly"
]

credentials = service_account.Credentials.from_service_account_file(
    "credentials.json",
    scopes=SCOPES
)

calendar_service = build(
    "calendar",
    "v3",
    credentials=credentials
)


# -----------------------------
# Next Monday -> Sunday
# -----------------------------

def get_next_week():

    today = datetime.today()

    days_until_next_monday = 7 - today.weekday()

    if days_until_next_monday == 0:
        days_until_next_monday = 7

    next_monday = today + timedelta(days=days_until_next_monday)

    next_sunday = next_monday + timedelta(days=6)

    return next_monday, next_sunday


# -----------------------------
# Read Google Calendar
# -----------------------------

def get_next_week_events():

    next_monday, next_sunday = get_next_week()

    events_result = calendar_service.events().list(
        calendarId=GOOGLE_CALENDAR_ID,
        timeMin=next_monday.isoformat() + "Z",
        timeMax=(next_sunday + timedelta(days=1)).isoformat() + "Z",
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    events = events_result.get("items", [])

    sessions = []

    week_start = next_monday.strftime("%-d %b")
    week_end = next_sunday.strftime("%-d %b")

    for event in events:

        title = event.get("summary", "")

        start = datetime.fromisoformat(
            event["start"]["dateTime"]
        )

        sessions.append({

            "title": title,

            "day": start.strftime("%A"),

            "date": start.strftime("%d/%m/%Y"),

            "time": start.strftime("%I:%M %p"),

            "week_start": week_start,

            "week_end": week_end

        })

    return sessions


# -----------------------------
# Test
# -----------------------------

if __name__ == "__main__":

    sessions = get_next_week_events()

    print(f"\nFound {len(sessions)} session(s)\n")

    for session in sessions:

        print(session)