import json
from datetime import datetime

from sheets import update_attendance


POLL_FILE = "poll_data.json"


# -----------------------------
# Load JSON
# -----------------------------
def load_poll_data():

    try:

        with open(POLL_FILE, "r") as f:

            return json.load(f)

    except (FileNotFoundError, json.JSONDecodeError):

        return {}


# -----------------------------
# Save JSON
# -----------------------------
def save_poll_data(data):

    with open(POLL_FILE, "w") as f:

        json.dump(data, f, indent=4)


# -----------------------------
# Create New Poll
# -----------------------------
def create_poll(

    poll_id,
    question,
    sessions,
    message_id,
    chat_id,
    week_start,
    week_end,

):

    data = load_poll_data()

    options = []

    for session in sessions:

        options.append({

            "label": f"{session['day']} {session['time']}",

            "date": session["date"]

        })

    options.append({

        "label": "CMI (Please PM Captains)",

        "date": None

    })

    data[str(poll_id)] = {

        "week_start": week_start,

        "week_end": week_end,

        "question": question,

        "options": options,

        "message_id": message_id,

        "chat_id": chat_id,

        "created_at": datetime.now().isoformat(),

        "votes": {}

    }

    save_poll_data(data)


# -----------------------------
# Update Vote
# -----------------------------
def update_vote(

    poll_id,
    user_id,
    username,
    option_ids

):

    data = load_poll_data()

    poll_id = str(poll_id)

    user_id = str(user_id)

    if poll_id not in data:

        print("Unknown poll.")

        return

    options = data[poll_id]["options"]

    selected = []

    for option in option_ids:

        selected.append(options[option])

    data[poll_id]["votes"][user_id] = {

        "username": username,

        "selected": selected,

        "timestamp": datetime.now().isoformat()

    }

    save_poll_data(data)

    # ---------------------------------
    # Prepare dates for Google Sheets
    # ---------------------------------

    selected_dates = []

    for session in selected:

        if session["date"] is not None:

            selected_dates.append(session["date"])

    poll_dates = []

    for option in options:

        if option["date"] is not None:

            poll_dates.append(option["date"])

    # ---------------------------------
    # Update Google Sheet
    # ---------------------------------

    update_attendance(

        username=username,

        selected_dates=selected_dates,

        poll_dates=poll_dates

    )

    print(f"{username} attendance updated.")


# -----------------------------
# Get One Poll
# -----------------------------
def get_poll(poll_id):

    data = load_poll_data()

    return data.get(str(poll_id))


# -----------------------------
# Get All Polls
# -----------------------------
def get_all_polls():

    return load_poll_data()

def poll_exists(week_start, week_end):
    """
    Returns True if a poll for this week already exists.
    """

    data = load_poll_data()

    for poll in data.values():

        if (
            poll["week_start"] == week_start
            and poll["week_end"] == week_end
        ):
            return True

    return False