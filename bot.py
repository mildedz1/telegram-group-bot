import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Configure basic logging for debugging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Read environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
TARGET_USER_IDS = os.getenv("TARGET_USER_IDS", "")
REPLY_MESSAGE = os.getenv("REPLY_MESSAGE", "پیام شما دریافت شد")  # Default Farsi reply

# Convert comma-separated IDs to a list of integers
try:
    target_ids = [int(uid.strip()) for uid in TARGET_USER_IDS.split(",") if uid.strip()]
except ValueError:
    logger.error("TARGET_USER_IDS must be a comma-separated list of integers")
    target_ids = []

async def reply_to_targets(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Reply to messages from specific target users in group chats.
    """
    user = update.effective_user
    # Ignore updates without a valid user or message
    if not user or not update.message:
        return

    if user.id in target_ids:
        try:
            # Reply directly to the user's message
            await update.message.reply_text(REPLY_MESSAGE, reply_to_message_id=update.message.message_id)
            logger.info("Replied to user %s", user.id)
        except Exception as e:
            logger.error("Error replying to user %s: %s", user.id, e)

def main() -> None:
    """Start the bot and run it using application.run_polling."""
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN environment variable not set")

    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Handle text messages in group chats
    handler = MessageHandler(filters.TEXT & filters.ChatType.GROUPS, reply_to_targets)
    application.add_handler(handler)

    # Start polling (blocking call)
    application.run_polling()

if __name__ == "__main__":
    main()
