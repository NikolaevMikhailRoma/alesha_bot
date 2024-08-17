# Snowboard Selection Assistant Bot

This project is a Telegram bot designed to help users choose a snowboard based on their preferences and specifications. The bot interacts with users, collects relevant information, and provides personalized recommendations.

## Features

- **User Interaction:** The bot guides users through a series of questions to gather details like name, height, weight, riding level, gender, style, camber, and optional parameters like price, brand, and design preferences.
- **Data Logging:** All interactions are logged into a CSV file (`user_messages.csv`) using a pipe (`|`) as the delimiter to avoid conflicts with common text characters.
- **Data Storage:** User data is stored in a JSON file (`user_data.json`), which is updated whenever new information is collected.
- **AI Interaction:** The bot uses OpenAI's ChatGPT to generate responses and gather user information.

## Setup

### Prerequisites

- Python 3.7+
- A Telegram account and a bot token from BotFather
- OpenAI API key
- `pipenv` or `virtualenv` for managing the environment

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/snowboard-selection-bot.git
   cd snowboard-selection-bot
   ```

2. **Create and activate a virtual environment:**

   Using `pipenv`:
   ```bash
   pipenv install
   pipenv shell
   ```

   Using `virtualenv`:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file in the project root and add your API keys:**

   ```
   TELEGRAM_API_KEY=your-telegram-bot-api-key
   OPENAI_API_KEY=your-openai-api-key
   ```

5. **Prepare the system prompt:**

   Create a `system_prompt.txt` file in the project root and include the following system prompt:

   ```
   Your name is Assistant Alyosha; you only speak Russian; you can speak more informally and flirt a little; your goal is to help a person choose a snowboard: for this you need to get information from the user, after you have collected all the necessary information, you should form a JSON file with this information with the tag #json; you should not make up information about the user on your own.
   ```

6. **Initialize the CSV and JSON files:**

   The code will automatically create and initialize `user_messages.csv` and `user_data.json` if they don't already exist.

## Running the Bot

1. **Start the bot:**

   ```bash
   python main.py
   ```

2. **Interact with the bot:**

   - Open Telegram and find your bot using the bot's username.
   - Type `/start` to begin the interaction.
   - The bot will ask you questions to gather information and provide recommendations.

## Project Structure

- `main.py`: The main script to run the bot.
- `user_messages.csv`: Logs of user and bot messages.
- `user_data.json`: JSON file storing user preferences and selections.
- `system_prompt.txt`: The system prompt that guides the bot's behavior.
- `README.md`: This file.

## Contributing

Feel free to submit issues or pull requests if you have suggestions or improvements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

This `README.md` file provides an overview of the project, setup instructions, and details on how to run the bot. Adjust the repository URL and any other details as needed for your specific project.