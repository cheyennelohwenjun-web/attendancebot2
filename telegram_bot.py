import json
from datetime import datetime

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    PollAnswerHandler,
)

from attendance import (
    create_poll,
    update_vote,
)

from config import (
    BOT_TOKEN,
    GROUP_ID,
)


class AttendanceBot:

    def __init__(self):

        self.application = (
            ApplicationBuilder()
            .token(BOT_TOKEN)
            .build()
        )

        self.application.add_handler(
            PollAnswerHandler(self.receive_vote)
        )

    # -----------------------------
    # Send Weekly Poll
    # -----------------------------

    async def send_weekly_poll(self, sessions):

        if len(sessions) == 0:

            print("No CCA sessions next week.")

            return

        week_start = sessions[0]["week_start"]
        week_end = sessions[0]["week_end"]

        question = (
            f"{week_start} - {week_end} Training Week"
        )

        options = []

        for session in sessions:

            options.append(
                f"{session['day']} {session['time']}"
            )

        options.append(
            "CMI (Please PM Captains)"
        )

        message = await self.application.bot.send_poll(

            chat_id=GROUP_ID,

            question=question,

            options=options,

            allows_multiple_answers=True,

            is_anonymous=False

        )
        create_poll(

            poll_id=message.poll.id,

            question=question,

            sessions=sessions,

            message_id=message.message_id,

            chat_id=GROUP_ID,

            week_start=week_start,

            week_end=week_end,

        )
        

        print("--------------------------------")

        print("Attendance Poll Sent!")

        print("Question:", question)

        print("Poll ID:", message.poll.id)

        print("--------------------------------")

    # -----------------------------
    # Receive Vote
    # -----------------------------


    async def receive_vote(

        self,

        update: Update,

        context: ContextTypes.DEFAULT_TYPE,

    ):

        answer = update.poll_answer

        poll_id = answer.poll_id

        user = answer.user

        option_ids = answer.option_ids

        # Use Telegram username if available
        username = user.username

        if username is None:
            username = user.full_name

        print("--------------------------------")

        print("Vote Received")

        print("Username:", username)

        print("Poll:", poll_id)

        print("Selected:", option_ids)

        print("--------------------------------")

        update_vote(

            poll_id=poll_id,

            user_id=user.id,

            username=username,

            option_ids=option_ids

        )
    # -----------------------------
    # Save extra poll information
    # -----------------------------


    # -----------------------------
    # Save vote timestamp
    # -----------------------------


    # -----------------------------
    # Start Telegram
    # -----------------------------

    async def start(self):

        print("--------------------------------")
        print("Starting Attendance Bot...")
        print("--------------------------------")

        await self.application.initialize()

        await self.application.start()

        await self.application.updater.start_polling(
            allowed_updates=["poll_answer"]
        )

        print("Telegram Bot is now listening for votes.")

    # -----------------------------
    # Stop Telegram
    # -----------------------------

    async def stop(self):

        print("Stopping Telegram Bot...")

        await self.application.updater.stop()

        await self.application.stop()

        await self.application.shutdown()


attendance_bot = AttendanceBot() 