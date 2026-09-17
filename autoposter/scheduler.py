#!/usr/bin/env python3
import os
import requests
from datetime import datetime
from posts_september import POSTS

BOT_TOKEN = os.environ.get("TG_BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("TG_BOT_TOKEN environment variable is not set")
CHANNEL = "@bahmetev_ai"
IMAGES_DIR = os.path.join(os.path.dirname(__file__), "images")

VK_TOKEN = os.environ.get("VK_TOKEN")
VK_GROUP_ID = os.environ.get("VK_GROUP_ID")
VK_API = "https://api.vk.com/method"
VK_V = "5.199"

# ── TELEGRAM ──────────────────────────────────────────────────────────────────
def send_photo(text, image_path):
    with open(image_path, "rb") as photo:
        r = requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto",
            data={"chat_id": CHANNEL, "caption": text, "parse_mode": "HTML"},
            files={"photo": photo}
        )
    return r.json()

def send_text(text):
    r = requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": CHANNEL, "text": text, "parse_mode": "HTML"}
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
    })
    return r.json()

# ── MAIN ──────────────────────────────────────────────────────────────────────
def main():
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    now_hour = now[:16]

    for i, post in enumerate(POSTS):
        if post["datetime"] == now_hour:
            image_path = os.path.join(IMAGES_DIR, f"post{i+1}.png")

            # Telegram
            if os.path.exists(image_path):
                tg_result = send_photo(post["text"], image_path)
            else:
                tg_result = send_text(post["text"])

            if tg_result.get("ok"):
                print(f"[{now}] TG: опубликован пост {i+1}")
            else:
                print(f"[{now}] TG ошибка пост {i+1}: {tg_result}")

            # VK
            vk_result = vk_post(post["text"])
            if vk_result:
                if vk_result.get("response"):
                    print(f"[{now}] VK: опубликован пост {i+1} (id={vk_result['response']['post_id']})")
                else:
                    print(f"[{now}] VK ошибка пост {i+1}: {vk_result}")

            return

    print(f"[{now}] Нет поста")

if __name__ == "__main__":
    main()
