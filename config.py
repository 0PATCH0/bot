import json
import os
from typing import Dict, Any, Optional

CONFIG_FILE = "config.json"

def load_config() -> Optional[Dict[str, Any]]:
    """
    Завантажує налаштування з файлу config.json. Якщо файл не існує, створює новий зі стандартними значеннями.

    Returns:
        Optional[Dict[str, Any]]: Словник з налаштуваннями або None, якщо сталася помилка.
    """
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                config = json.load(f)
            if "voice_roles" not in config:
                config["voice_roles"] = {}
                save_config(config)  # Зберігаємо оновлений конфіг
            return config

        # Якщо файл не існує, створюємо його зі стандартними значеннями
        default_config = {
            "telegram_webhook": {},
            "voice_roles": {}
        }
        save_config(default_config)
        return default_config
    except Exception as e:
        print(f"Помилка при завантаженні конфігурації: {e}")
        return None

def save_config(config: Dict[str, Any]) -> None:
    """
    Зберігає налаштування у файл config.json.

    Args:
        config (Dict[str, Any]): Словник з налаштуваннями для збереження.
    """
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)
    except Exception as e:
        print(f"Помилка при збереженні конфігурації: {e}")

# Токен бота (використовуємо змінну середовища для безпеки)
TOKEN = ("MTMzNDMxNzEzODgyNzI4NDYwMQ.GqRA7P.h3feXFlAeaY44Ne60A-8iCjXXCNih7RwrC_c3w")
if not TOKEN:
    raise ValueError("Токен бота не знайдено. Будь ласка, встановіть змінну середовища DISCORD_BOT_TOKEN.")