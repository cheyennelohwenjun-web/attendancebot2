from datetime import datetime, timedelta

from google.oauth2 import service_account
from googleapiclient.discovery import build

from config import GOOGLE_CALENDAR_ID


# Google Calendar permission
SCOPES = [
    "https://www.googleapis.com/auth/calendar.readonly"
]


# Connect to Google Calendar
credentials = service_account.Credentials.from_service_account_file(
    "credentials.json",
    scopes=SCOPES
)

calendar_service = build(
    "calendar",
    "v3",
    credentials=credentials
)


def get_next_week():
    """
    Returns:
        next_monday
        next_sunday
    """

    today = datetime.today()

    days_until_next_monday = 7 - today.weekday()

    next_monday = today + timedelta(days=days_until_next_monday)

    next_sunday = next_monday + timedelta(days=6)

    return next_monday, next_sunday

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

    return events

if __name__ == "__main__":

    events = get_next_week_events()

    print(events)
