import asyncio

from telegram_bot import attendance_bot


async def main():

    print("===================================")
    print("Attendance Bot Started")
    print("===================================")

    # Start Telegram bot
    await attendance_bot.start()

    print("Bot is now listening for votes...")

    # Keep running forever
    while True:

        await asyncio.sleep(1)


if __name__ == "__main__":

    asyncio.run(main())