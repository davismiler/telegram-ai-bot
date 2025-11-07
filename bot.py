"""
A Telegram bot that responds to user messages.

First, several handler functions are defined.
Then, these functions are registered in the application.
After that, the bot starts running and continues until you stop it manually (Ctrl-C in the terminal).
"""

import logging
from logging.handlers import RotatingFileHandler
import os

# --- Logging configuration: file + console output ---
log_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log_dir = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "bot.log")

file_handler = RotatingFileHandler(
    log_file, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
)
file_handler.setFormatter(log_formatter)
file_handler.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(log_formatter)
stream_handler.setLevel(logging.INFO)

root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
# Remove any existing handlers to avoid duplicate logs on reimport
if root_logger.handlers:
    root_logger.handlers.clear()
root_logger.addHandler(file_handler)
root_logger.addHandler(stream_handler)

logger = logging.getLogger(__name__)

# Disable propagation so messages don’t go to root logger again
logger.propagate = False

# Reduce verbosity from httpx logs
logging.getLogger("httpx").setLevel(logging.WARNING)


from telegram import ForceReply, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from model import chat_with_llm

import dotenv

# --- Load environment variables from .env file ---
try:
    env = dotenv.dotenv_values(".env")
    TELEGRAM_BOT_TOKEN = env["TELEGRAM_BOT_TOKEN"]
except FileNotFoundError:
    raise FileNotFoundError("The .env file was not found. Make sure it exists in the project root directory.")
except KeyError as e:
    raise KeyError(f"Environment variable {str(e)} not found in .env file. Please check its contents.")


# --- Command and message handler definitions ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler for the /start command. Sends a welcome message when the bot starts."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Main handler for processing user text messages using the AI model."""
    user_message = update.message.text
    user = update.effective_user.first_name
    user_message = f"{user_message}. Username: {user}"

    # Retrieve message history from context.chat_data
    history = context.chat_data.get("history", [])
    logger.debug(f"History: {history}")

    # Send the current user message and chat history to the LLM service
    llm_response = chat_with_llm(user_message, history=history)
    context.chat_data["history"] = history  # Save updated history
    await update.message.reply_text(llm_response)


def main() -> None:
    """Main function to initialize and run the Telegram bot application."""
    # Create the main Telegram bot application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Message handler for all non-command text messages
    chat_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, chat)

    # Register handlers
    # Command: /start
    application.add_handler(CommandHandler("start", start))
    # All other text messages handled by chat_handler
    application.add_handler(chat_handler)

    # Run the bot in polling mode
    # The bot will continue running until manually stopped (Ctrl-C or a system signal)
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
