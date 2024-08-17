import os
import openai
import pandas as pd
import json
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Load API keys from .env file
load_dotenv()
TELEGRAM_API_KEY = os.getenv("TELEGRAM_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI(
    api_key=OPENAI_API_KEY,
)

# Initialize global variables
user_dict = {}
CSV_FILE = "user_messages.csv"
JSON_FILE = "user_data.json"
SYSTEM_PROMPT_FILE = "system_prompt.txt"
CSV_SEPARATOR = '|'  # Define the separator character for the CSV file

# Initialize or load the JSON file
if os.path.exists(JSON_FILE):
    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        user_dict = json.load(f)
else:
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(user_dict, f, ensure_ascii=False, indent=4)

# Initialize the CSV file with the new separator
if not os.path.exists(CSV_FILE):
    df = pd.DataFrame(columns=["user_id", "role", "message"])
    df.to_csv(CSV_FILE, index=False, sep=CSV_SEPARATOR)

# Function to log messages to CSV
def log_message(user_id, user_name, message, role="user"):
    new_data = pd.DataFrame({"user_id": [user_id],  "role": [role], "message": [message]})
    new_data.to_csv(CSV_FILE, mode='a', header=False, index=False, sep=CSV_SEPARATOR)

# Function to save user_dict to JSON file
def save_user_dict_to_json():
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(user_dict, f, ensure_ascii=False, indent=4)

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

    # Log the user's message to CSV
    log_message(user_id, user_name, message_text, role="user")

    # Load all messages for this user from the CSV
    df = pd.read_csv(CSV_FILE, sep=CSV_SEPARATOR)
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

    # Log the bot's response to CSV
    log_message(user_id, "Alyosha", response_text, role="assistant")

    # Check if the response contains JSON
    if "json" in response_text:
        try:
            json_data_start = response_text.index("{")
            json_data_end = response_text.rindex("}") + 1
            json_data = response_text[json_data_start:json_data_end]
            user_dict[user_id] = json.loads(json_data)  # Safely parse JSON data
            save_user_dict_to_json()
            await update.message.reply_text("Спасибо, вся необходимая информация собрана, обработка данных.")
        except (ValueError, json.JSONDecodeError):
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
