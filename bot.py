#!/usr/bin/env python3
"""
Telegram Group Responder Bot

This bot replies with a configurable message whenever a user from a predefined list sends a message in a group.

Configuration is done through environment variables:
- BOT_TOKEN: the token provided by @BotFather for your bot.
- TARGET_USER_IDS: a comma-separated list of numeric Telegram user IDs to monitor.
- REPLY_MESSAGE: the message the bot should send in reply. Defaults to "Your message has been received." if not set.

To run the bot, install the python-telegram-bot library (v20+) and set the environment variables before executing this script.

Example:
```
export BOT_TOKEN=123456:ABC...
export TARGET_USER_IDS=12345,67890
export REPLY_MESSAGE="پیام شما دریافت شد"
python3 bot.py
```
"""
import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Enable logging to help with debugging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Read configuration from environment variables
token = os.getenv("BOT_TOKEN")
if not token:
    raise ValueError("BOT_TOKEN environment variable is not set.")

target_users_str = os.getenv("TARGET_USER_IDS", "")
# Parse the string into a set of integer user IDs
target_user_ids = set()
for uid in target_users_str.split(","):
    uid = uid.strip()
    if uid.isdigit():
        target_user_ids.add(int(uid))

# Default reply message
reply_message = os.getenv("REPLY_MESSAGE", "Your message has been received.")

async def reply_to_targets(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Reply to messages from target users in group chats."""
    # Ensure the update contains a message
    if update.message is None:
        return

    user = update.effective_user
    if user and user.id in target_user_ids:
        try:
            # Reply to the user's message directly
            await update.message.reply_text(reply_message)
            logger.info("Replied to user %s", user.id)
        except Exception as e:
            logger.error("Error replying to user %s: %s", user.id, e)

async def main() -> None:
    """Start the bot."""
    application = ApplicationBuilder().token(token).build()

    # Handle all text messages in group chats
    handler = MessageHandler(filters.ChatType.GROUPS & filters.TEXT, reply_to_targets)
    application.add_handler(handler)

    logger.info("Bot is starting...")
    # Run the bot until Ctrl-C is pressed
    await application.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
