import os
import openai
import pandas as pd
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Load API keys from .env file
load_dotenv()
TELEGRAM_API_KEY = os.getenv("TELEGRAM_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=OPENAI_API_KEY,
)

# Initialize global variables
user_dict = {}
CSV_FILE = "user_messages.csv"
SYSTEM_PROMPT_FILE = "system_prompt.txt"

# Initialize the CSV file
if not os.path.exists(CSV_FILE):
    df = pd.DataFrame(columns=["user_id", "user_name", "message"])
    df.to_csv(CSV_FILE, index=False)

# Function to log messages to CSV
def log_message(user_id, user_name, message):
    new_data = pd.DataFrame({"user_id": [user_id], "user_name": [user_name], "message": [message]})
    new_data.to_csv(CSV_FILE, mode='a', header=False, index=False)

# Function to read system prompt from file
def get_system_prompt():
    with open(SYSTEM_PROMPT_FILE, 'r', encoding='utf-8') as file:
        return file.read().strip()

# Function to get ChatGPT response
def get_chatgpt_response(messages):
    response = client.chat.completions.create(
        messages=messages,
        model="gpt-4o-mini",
    )
    return response.choices[0].message.content

# Start command handler
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Привет! Я помогу вам выбрать сноуборд. Как вас зовут?")

# Message handler
async def handle_message(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    user_name = update.message.from_user.first_name
    message_text = update.message.text

    # Log message to CSV
    log_message(user_id, user_name, message_text)

    # Load all messages for this user from the CSV
    df = pd.read_csv(CSV_FILE)
    user_messages = df[df['user_id'] == user_id]['message'].tolist()

    # Create messages for ChatGPT API
    chat_messages = [
        {"role": "system", "content": get_system_prompt()},
        {"role": "assistant", "content": "Привет! Меня зовут Алёша, я помогу вам выбрать сноуборд. Как вас зовут?"},
    ]

    for msg in user_messages:
        chat_messages.append({"role": "user", "content": msg})

    # Get the ChatGPT response
    response_text = get_chatgpt_response(chat_messages)

    # Check if the response contains JSON
    if "#json" in response_text:
        try:
            json_data_start = response_text.index("{")
            json_data_end = response_text.rindex("}") + 1
            json_data = response_text[json_data_start:json_data_end]
            user_dict[user_id] = eval(json_data)  # In production, use `json.loads()` instead of `eval()`
            await update.message.reply_text("Спасибо, вся необходимая информация собрана, обработка данных.")
        except (ValueError, SyntaxError):
            await update.message.reply_text("Произошла ошибка при обработке данных.")
    else:
        await update.message.reply_text(response_text)

# Main function to start the bot
def main() -> None:
    application = Application.builder().token(TELEGRAM_API_KEY).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start polling for updates
    application.run_polling()

if __name__ == '__main__':
    main()

