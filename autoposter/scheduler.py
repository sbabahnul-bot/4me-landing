#!/usr/bin/env python3
import os
import requests
from datetime import datetime
from posts_july import POSTS

BOT_TOKEN = os.environ.get("TG_BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("TG_BOT_TOKEN environment variable is not set")
CHANNEL = "@bahmetev_ai"
IMAGES_DIR = os.path.join(os.path.dirname(__file__), "images")

def send_photo(text, image_path):
    with open(image_path, "rb") as photo:
        r = requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto",
            data={"chat_id": CHANNEL, "caption": text},
            files={"photo": photo}
        )
    return r.json()

def send_text(text):
    r = requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": CHANNEL, "text": text}
    )
    return r.json()

def main():
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    now_hour = now[:16]

    for i, post in enumerate(POSTS):
        if post["datetime"] == now_hour:
            image_path = os.path.join(IMAGES_DIR, f"post{i+1}.png")
            if os.path.exists(image_path):
                result = send_photo(post["text"], image_path)
            else:
                result = send_text(post["text"])

            if result.get("ok"):
                print(f"[{now}] Опубликован пост {i+1}: {post['datetime']}")
            else:
                print(f"[{now}] Ошибка пост {i+1}: {result}")
            return

    print(f"[{now}] Нет поста")

if __name__ == "__main__":
    main()
