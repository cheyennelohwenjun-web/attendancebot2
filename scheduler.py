from apscheduler.schedulers.blocking import BlockingScheduler

import asyncio

from google_calendar import get_next_week_events
from telegram_bot import attendance_bot
from attendance import poll_exists


scheduler = BlockingScheduler()


def weekly_attendance():

    print("===================================")
    print("Checking next week's CCA sessions...")
    print("===================================")

    sessions = get_next_week_events()

    if len(sessions) == 0:

        print("No training next week.")
        print("===================================")
        return

    week_start = sessions[0]["week_start"]
    week_end = sessions[0]["week_end"]

    if poll_exists(week_start, week_end):

        print("Poll already exists.")
        print("Skipping poll creation.")
        print("===================================")
        return

    print(f"Found {len(sessions)} session(s).")

    asyncio.run(
        attendance_bot.send_weekly_poll(sessions)
    )

    print("Poll sent successfully.")
    print("===================================")


scheduler.add_job(
    weekly_attendance,
    trigger="cron",
    day_of_week="thu",
    hour=21,
    minute=0
)


if __name__ == "__main__":

    print("Scheduler Started.")
    print("Waiting for Thursday 9:00 PM...")



    print("Test completed.")
    print()

    scheduler.start()