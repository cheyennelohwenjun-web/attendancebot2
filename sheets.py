import gspread
from google.oauth2.service_account import Credentials

from config import GOOGLE_SHEET_ID


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets"
]

credentials = Credentials.from_service_account_file(
    "credentials.json",
    scopes=SCOPES
)

client = gspread.authorize(credentials)

spreadsheet = client.open_by_key(GOOGLE_SHEET_ID)

worksheet = spreadsheet.worksheet("attendance")


def ensure_date_columns(poll_dates):
    """
    Ensures every poll date exists in Row 1.
    Returns a dictionary:
        {
            "07/07/2026": 2,
            "09/07/2026": 3
        }
    """

    headers = worksheet.row_values(1)

    # If sheet is completely empty
    if len(headers) == 0:
        worksheet.update_cell(1, 1, "Username")
        headers = worksheet.row_values(1)

    date_columns = {}

    for date in poll_dates:

        headers = worksheet.row_values(1)

        if date in headers:

            date_columns[date] = headers.index(date) + 1

        else:

            new_col = len(headers) + 1

            worksheet.update_cell(1, new_col, date)

            date_columns[date] = new_col

    return date_columns


def ensure_user(username):
    """
    Finds the user's row.
    If not found, creates a new row.
    """

    usernames = worksheet.col_values(1)

    for i, value in enumerate(usernames, start=1):

        if value == username:
            return i

    row = len(usernames) + 1

    worksheet.update_cell(row, 1, username)

    return row


def update_attendance(username, selected_dates, poll_dates):
    """
    username:
        Telegram username

    selected_dates:
        Dates user selected

    poll_dates:
        ALL dates that appeared in this week's poll
    """

    date_columns = ensure_date_columns(poll_dates)

    row = ensure_user(username)

    for date in poll_dates:

        col = date_columns[date]

        if date in selected_dates:
            worksheet.update_cell(row, col, 1)
        else:
            worksheet.update_cell(row, col, 0)


if __name__ == "__main__":

    print("Testing Google Sheets...")

    update_attendance(

        username="itzscheyenne",

        selected_dates=["07/07/2026"],

        poll_dates=[
            "07/07/2026",
            "09/07/2026"
        ]

    )

    print("Success!")