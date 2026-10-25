#!/usr/bin/env python3
import os
import time
import requests
from datetime import datetime
from zoneinfo import ZoneInfo

# время в постах (поле "datetime") указано по Красноярску, а сервер живёт по Москве
POST_TZ = ZoneInfo("Asia/Krasnoyarsk")
from posts_october import POSTS

def load_env(path):
    """Читает KEY=VALUE из .env рядом со скриптом; значения из файла приоритетнее окружения."""
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, _, value = line.partition("=")
                    os.environ[key.strip()] = value.strip()
    except FileNotFoundError:
        pass

load_env(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

BOT_TOKEN = os.environ.get("TG_BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("TG_BOT_TOKEN environment variable is not set")
CHANNEL = "@bahmetev_ai"
IMAGES_DIR = os.path.join(os.path.dirname(__file__), "images")

VK_TOKEN = os.environ.get("VK_TOKEN")
VK_GROUP_ID = os.environ.get("VK_GROUP_ID")
VK_API = "https://api.vk.com/method"
VK_V = "5.199"

RETRY_ATTEMPTS = 3
RETRY_PAUSE = 30  # секунд между попытками
REQUEST_TIMEOUT = 30

def with_retry(fn, *args):
    """Повторяет отправку при сетевой ошибке или ответе не ok (TG: ok, VK: response)."""
    result = None
    for attempt in range(1, RETRY_ATTEMPTS + 1):
        try:
            result = fn(*args)
            if result is None or result.get("ok") or result.get("response"):
                return result
        except (requests.RequestException, ValueError) as e:
            result = {"ok": False, "description": f"{type(e).__name__}: {e}"}
        if attempt < RETRY_ATTEMPTS:
            print(f"попытка {attempt}/{RETRY_ATTEMPTS} не удалась: {result}; повтор через {RETRY_PAUSE} с")
            time.sleep(RETRY_PAUSE)
    return result

# ── TELEGRAM ──────────────────────────────────────────────────────────────────
def send_photo(text, image_path):
    with open(image_path, "rb") as photo:
        r = requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto",
            data={"chat_id": CHANNEL, "caption": text, "parse_mode": "HTML"},
            files={"photo": photo},
            timeout=REQUEST_TIMEOUT
        )
    return r.json()

def send_text(text):
    r = requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": CHANNEL, "text": text, "parse_mode": "HTML"},
        timeout=REQUEST_TIMEOUT
    )
    return r.json()

# ── VK ────────────────────────────────────────────────────────────────────────
def vk_post(text):
    if not VK_TOKEN or not VK_GROUP_ID:
        return None
    # Убираем HTML-теги — VK их не поддерживает
    import re
    clean = re.sub(r'<[^>]+>', '', text)
    r = requests.post(f"{VK_API}/wall.post", params={
        "owner_id": f"-{VK_GROUP_ID}",
        "from_group": 1,
        "message": clean,
        "access_token": VK_TOKEN,
        "v": VK_V
    }, timeout=REQUEST_TIMEOUT)
    return r.json()

# ── MAIN ──────────────────────────────────────────────────────────────────────
def main():
    now = datetime.now(POST_TZ).strftime("%Y-%m-%d %H:%M")
    now_hour = now[:16]

    for i, post in enumerate(POSTS):
        if post["datetime"] == now_hour:
            if "{{" in post["text"]:
                print(f"[{now}] Пост {i+1} — незаполненный шаблон, пропуск")
                return
            image_path = os.path.join(IMAGES_DIR, post.get("image", f"post{i+1}.png"))

            # Telegram
            if os.path.exists(image_path):
                if len(post["text"]) <= 1024:
                    tg_result = with_retry(send_photo, post["text"], image_path)
                else:
                    # подпись к фото в Telegram — до 1024 символов
                    with_retry(send_photo, "", image_path)
                    tg_result = with_retry(send_text, post["text"])
            else:
                tg_result = with_retry(send_text, post["text"])

            if tg_result.get("ok"):
                print(f"[{now}] TG: опубликован пост {i+1}")
            else:
                print(f"[{now}] TG ошибка пост {i+1}: {tg_result}")

            # VK
            vk_result = with_retry(vk_post, post["text"])
            if vk_result:
                if vk_result.get("response"):
                    print(f"[{now}] VK: опубликован пост {i+1} (id={vk_result['response']['post_id']})")
                else:
                    print(f"[{now}] VK ошибка пост {i+1}: {vk_result}")

            return

    # сообщение «Нет поста» не пишем: cron запускает скрипт каждую минуту и лог раздувается

if __name__ == "__main__":
    main()
