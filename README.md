# Python Telegram AI Bot

This Telegram bot is a consultant for home internet plans.

It uses the YandexGPT language model, accessed via an API.

The bot is written in Python and uses the `python-telegram-bot` library to work with the Telegram API.

## Installation Instructions

### 1. Download and unzip the project files, then open the folder in VS Code.

Or use the console to clone the repository:
```
git clone https://github.com/davismiler/telegram-ai-bot.git
cd telegram-ai-bot
```

### 2. Create a virtual environment
A virtual environment helps isolate project dependencies. ```bash
python -m venv venv
```
Activation:
- On Windows:
```bash
venv\Scripts\activate
```
- On macOS/Linux:
```bash
source venv/bin/activate
```

## 3. Install dependencies
You can immediately check the `requirements.txt` file when creating a virtual environment in VS Code.
Or install all the necessary libraries via the terminal:
```bash
pip install -r requirements.txt
```

## 4. Setting Environment Variables
Create a .env file in the project's root folder and add your keys there:
```
TELEGRAM_BOT_TOKEN=your_bot_token
YA_API_KEY=your_yandex_api_key
YA_FOLDER_ID=your_yandex_console_directory
```
- TELEGRAM_BOT_TOKEN — Get it from @BotFather on Telegram.
- YA_API_KEY — Get it from the service used for AI (e.g., YandexGPT).
- YA_FOLDER_ID — Copy it from the Yandex console.

## 5. Launching the Bot
Run the bot with the command:
```bash
python bot.py
```
If everything is configured correctly, the bot will start working and receiving messages in Telegram.

## 6. Contributing Changes and Helping the Project
- If you'd like to contribute, create an issue or submit a pull request.
- If you have any questions, please post them in the "Questions for the Teacher" thread in the Telegram channel.
- If you need more detail on a specific step (for example, obtaining a token or working with AI), please let me know, and I'll add more details!