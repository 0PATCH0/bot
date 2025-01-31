import requests

TELEGRAM_BOT_TOKEN = '7685675243:AAHBQziKJB1lOm8jeq-sYyET9viVUCb96gk'  # Замість 'YOUR_BOT_TOKEN' використовуйте ваш токен
WEBHOOK_URL = 'https://53ed-31-42-12-181.ngrok-free.app/webhook'  # Замість 'http://your-ngrok-url/webhook' вставте ваш ngrok URL

url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/setWebhook?url={WEBHOOK_URL}'

response = requests.get(url)
print(response.json())  # Це має підтвердити налаштування вебхука
