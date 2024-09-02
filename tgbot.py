#!/usr/bin/env python
# pylint: disable=unused-argument

import logging
import psutil

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# change /proc location
psutil.PROCFS_PATH = r"/host-proc"


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hello there {user.mention_html()}! Use /status",
    )

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send what to do on unknown message"""
    await update.message.reply_html(
        rf"Use /status"
    )

async def status_update(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends an update of current apps running"""
    # get process_list
    process_list = [x.info for x in psutil.process_iter(attrs=['pid', 'name', 'username', 'cpu_percent'])]
    # sort it
    cpu_sorted_list = sorted(process_list, key=lambda x: x['cpu_percent'], reverse=True)
    # select top 5 items by CPU usage
    top_5 = [f"{item["name"]}\t{item["pid"]}\t{item["cpu_percent"]}\t{item["username"]}" for item in cpu_sorted_list[:5]]
    # format the output
    to_send = f"NAME\tPID\tCPU%\tUSER\n{"\n".join(top_5)}"

    await update.message.reply_markdown_v2(
        f"""```{to_send}```"""
    )

def main() -> None:
    """Import secrets"""
    with open("secrets.txt", "r") as secret:
        SECRET = secret.read().strip()

    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(SECRET).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("status", status_update))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, help))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
