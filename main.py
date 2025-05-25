import requests
import time
import os

WB_TOKEN = os.getenv("WB_TOKEN")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def check_fbo_supply():
    url = "https://suppliers-api.wildberries.ru/api/v2/supplies"
    headers = {"Authorization": WB_TOKEN}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return True
    elif response.status_code == 403:
        return False
    else:
        print("⚠️ Ответ WB:", response.status_code)
        return False

def notify_telegram(message):
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(telegram_url, data={"chat_id": CHAT_ID, "text": message})

print("🔄 Запуск мониторинга WB FBO...")
notified = False

while True:
    try:
        if check_fbo_supply():
            if not notified:
                notify_telegram("🚛 WB открыл FBO поставку! Заходи и оформляй.")
                print("✅ Оповещение отправлено.")
                notified = True
                time.sleep(3600)
        else:
            print("⏳ Пока недоступно...")
            notified = False
    except Exception as e:
        print("❌ Ошибка:", e)
    time.sleep(10)
