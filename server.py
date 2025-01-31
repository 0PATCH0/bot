from flask import Flask, request, jsonify
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import logging

# Налаштування Flask
app = Flask(__name__)

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ваш токен Telegram бота
TELEGRAM_BOT_TOKEN = 'YOUR_BOT_TOKEN'

# Створення об'єкта Application
application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

# Обробка команди /start
async def start(update: Update, context):
    """Проста команда старту для перевірки роботи."""
    await update.message.reply_text("Привіт, я твій бот!")

# Обробка всіх текстових повідомлень
async def handle_message(update: Update, context):
    text = update.message.text
    logger.info(f"Отримано повідомлення: {text}")
    await update.message.reply_text(f"Ти написав: {text}")

# Додавання обробників
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Ручка для вебхука
@app.route('/webhook', methods=['POST'])
def handle_telegram_message():
    """Обробляє вхідні повідомлення з Telegram."""
    try:
        data = request.get_json()  # Отримуємо JSON від Telegram
        logger.info(f"Отримано повідомлення з Telegram: {data}")

        # Перетворення даних в Update
        update = Update.de_json(data, application.bot)

        # Обробка повідомлення
        application.process_update(update)

        return jsonify({"status": "success"}), 200
    except Exception as e:
        logger.error(f"Помилка при обробці повідомлення: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=21009)
