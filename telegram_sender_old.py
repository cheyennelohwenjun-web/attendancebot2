import asyncio
from telegram import Bot
from config import BOT_TOKEN, GROUP_ID

bot = Bot(token=BOT_TOKEN)


async def send_weekly_poll(sessions):

    if len(sessions) == 0:
        print("No CCA sessions found.")
        return

    first_date = sessions[0]["date"]
    last_date = sessions[-1]["date"]

    question = f"{first_date} - {last_date} Training Week"

    options = []

    for session in sessions:
        options.append(f"{session['day']} {session['time']}")

    options.append("CMI (Please PM Captains)")

    message = await bot.send_poll(
        chat_id=GROUP_ID,
        question=question,
        options=options,
        is_anonymous=False,
        allows_multiple_answers=True
    )
    import json

    with open("poll_data.json", "r") as file:
        poll_data = json.load(file)

    poll_data[message.poll.id] = {
        "question": question,
        "options": options
    }

    with open("poll_data.json", "w") as file:
        json.dump(poll_data, file, indent=4)

    print("Poll sent!")


if __name__ == "__main__":

    test_sessions = [
        {
            "day": "Tuesday",
            "date": "7 Jul",
            "time": "7:30 PM"
        },
        {
            "day": "Thursday",
            "date": "9 Jul",
            "time": "7:30 PM"
        }
    ]

    asyncio.run(send_weekly_poll(test_sessions))