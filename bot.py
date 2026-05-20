import time
import requests
import os

TOKEN = os.getenv("BALE_TOKEN")
BASE_URL = f"https://tapi.bale.ai/bot{TOKEN}/"

def get_updates(offset=None):
    url = BASE_URL + "getUpdates"
    params = {"offset": offset}
    return requests.get(url, params=params).json()

def send_message(chat_id, text):
    url = BASE_URL + "sendMessage"
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, data=data)

def handle_update(update):
    message = update.get("message")
    if not message:
        return

    chat_id = message["chat"]["id"]
    text = message.get("text", "")
    user = message["from"]
    username = user.get("first_name", "there")

    if text == "/start":
        send_message(chat_id, f"Hey {username} 👋")

def run_bot():
    print("Bot is running...")
    offset = None

    while True:
        updates = get_updates(offset)
        if "result" in updates:
            for update in updates["result"]:
                offset = update["update_id"] + 1
                handle_update(update)

        time.sleep(1)

if __name__ == "__main__":
    run_bot()
