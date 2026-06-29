from PIL import Image, ImageDraw, ImageFont
import os, math

OUT = "/home/agent/projects/4me/autoposter/images"
os.makedirs(OUT, exist_ok=True)

W, H = 1080, 1080

# Colors
BG       = (2, 6, 16)
SURFACE  = (13, 24, 41)
ACCENT   = (6, 182, 212)
ACCENT2  = (8, 145, 178)
WHITE    = (255, 255, 255)
GRAY     = (148, 163, 184)
GREEN    = (16, 185, 129)
ORANGE   = (245, 158, 11)

def get_font(size, bold=False):
    paths = [
        f'/usr/share/fonts/truetype/dejavu/DejaVuSans{"−Bold" if bold else ""}.ttf',
        f'/usr/share/fonts/truetype/dejavu/DejaVuSans{"-Bold" if bold else ""}.ttf',
    ]
    for p in paths:
        try:
            return ImageFont.truetype(p, size)
        except:
            pass
    return ImageFont.load_default()

def draw_grid(draw):
    for x in range(0, W, 80):
        draw.line([(x, 0), (x, H)], fill=(20, 40, 70), width=1)
    for y in range(0, H, 80):
        draw.line([(0, y), (W, y)], fill=(20, 40, 70), width=1)

def draw_glow(img, cx, cy, r, color, alpha=60):
    overlay = Image.new('RGBA', img.size, (0,0,0,0))
    d = ImageDraw.Draw(overlay)
    for i in range(5, 0, -1):
        a = int(alpha * i / 5)
        ri = r * i // 3
        d.ellipse([cx-ri, cy-ri, cx+ri, cy+ri], fill=(*color, a))
    img.paste(Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB'), (0,0))

def wrap_text(text, font, max_width, draw):
    words = text.split()
    lines = []
    line = []
    for word in words:
        test = ' '.join(line + [word])
        bbox = draw.textbbox((0,0), test, font=font)
        if bbox[2] > max_width and line:
            lines.append(' '.join(line))
            line = [word]
        else:
            line.append(word)
    if line:
        lines.append(' '.join(line))
    return lines

def base_image():
    img = Image.new('RGB', (W, H), BG)
    draw = ImageDraw.Draw(img)
    draw_grid(draw)
    # Corner accent lines
    for i in range(3):
        draw.line([(0, i*2), (W//3, i*2)], fill=(*ACCENT, ), width=1)
        draw.line([(W - W//3, H-1-i*2), (W, H-1-i*2)], fill=(*ACCENT,), width=1)
    return img, draw

def draw_tag(draw, x, y, text, color=ACCENT):
    font = get_font(22, bold=True)
    bbox = draw.textbbox((0,0), text, font=font)
    tw = bbox[2] - bbox[0]
    pad = 16
    draw.rounded_rectangle([x, y, x+tw+pad*2, y+36], radius=6, fill=(*color, 40), outline=color, width=1)
    draw.text((x+pad, y+7), text, font=font, fill=color)
    return y + 36 + 20

def draw_logo(draw, x=60, y=H-70):
    font = get_font(24, bold=True)
    draw.text((x, y), "Бахметьев", font=font, fill=WHITE)
    w = draw.textbbox((0,0), "Бахметьев", font=font)[2]
    draw.text((x+w, y), ".AI", font=font, fill=ACCENT)
    draw.text((x, y+28), "@bahmetev_ai", font=get_font(18), fill=GRAY)

def draw_divider(draw, x, y, width, color=ACCENT):
    draw.line([(x, y), (x+width, y)], fill=color, width=2)

POSTS_META = [
    {
        "file": "post1.png",
        "tag": "КЕЙС",
        "tag_color": GREEN,
        "headline": "Фитнес-клуб терял\n40% клиентов",
        "sub": "Вот что изменилось за месяц",
        "icon": "📈",
        "stats": ["+38%", "конверсия в визит"],
        "accent_pos": (W-150, 200),
        "accent_color": GREEN,
    },
    {
        "file": "post2.png",
        "tag": "БОЛЬ",
        "tag_color": ORANGE,
        "headline": "Риелтор тратит\n3 часа в день",
        "sub": "На вопросы, которые задают все подряд",
        "icon": "🏠",
        "stats": ["24/7", "Агентура вместо менеджера"],
        "accent_pos": (W-120, 300),
        "accent_color": ORANGE,
    },
    {
        "file": "post3.png",
        "tag": "КАК ЭТО РАБОТАЕТ",
        "tag_color": ACCENT,
        "headline": "AI-бот понимает\nсмысл, не слова",
        "sub": "Чем отличается от чат-бота из 2018-го",
        "icon": "🤖",
        "stats": ["15 сек", "время ответа"],
        "accent_pos": (W-100, 250),
        "accent_color": ACCENT,
    },
    {
        "file": "post4.png",
        "tag": "ЛИЧНОЕ",
        "tag_color": (168, 85, 247),
        "headline": "2 года объяснял\nзачем нужен AI",
        "sub": "Потом перестал объяснять — и пошли продажи",
        "icon": "💡",
        "stats": ["3 недели", "окупаемость бота"],
        "accent_pos": (W-130, 280),
        "accent_color": (168, 85, 247),
    },
    {
        "file": "post5.png",
        "tag": "ОПРОС",
        "tag_color": (244, 63, 94),
        "headline": "Что съедает\nбольше всего времени?",
        "sub": "Быстрый вопрос для владельцев бизнеса",
        "icon": "🗳",
        "stats": ["1 мин", "проголосуй"],
        "accent_pos": (W-110, 260),
        "accent_color": (244, 63, 94),
    },
    {
        "file": "post6.png",
        "tag": "ИСТОРИЯ",
        "tag_color": GREEN,
        "headline": "Диалог в\n2:47 ночи",
        "sub": "Пока владелец спал — бот сделал продажу",
        "icon": "🌙",
        "stats": ["02:47", "бот не спит"],
        "accent_pos": (W-100, 220),
        "accent_color": GREEN,
    },
    {
        "file": "post7.png",
        "tag": "ПРЕДЛОЖЕНИЕ",
        "tag_color": ORANGE,
        "headline": "Июль — окно\nвозможностей",
        "sub": "Пока конкуренты в отпуске",
        "icon": "🚀",
        "stats": ["-20%", "до 10 июля"],
        "accent_pos": (W-120, 240),
        "accent_color": ORANGE,
    },
]

for meta in POSTS_META:
    img, draw = base_image()

    # Glow accent
    ac = meta["accent_color"]
    draw_glow(img, *meta["accent_pos"], 280, ac, alpha=80)
    draw = ImageDraw.Draw(img)

    # Large icon background circle
    cx, cy = meta["accent_pos"]
    r = 120
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(*ac, 30), outline=(*ac,), width=2)
    r2 = 80
    draw.ellipse([cx-r2, cy-r2, cx+r2, cy+r2], fill=(*ac, 15), outline=(*ac, 80), width=1)
    # Inner accent shape
    draw.line([(cx-30, cy), (cx+30, cy)], fill=(*ac,), width=3)
    draw.line([(cx, cy-30), (cx, cy+30)], fill=(*ac,), width=3)

    # Tag
    y = 70
    draw_tag(draw, 60, y, meta["tag"], meta["tag_color"])
    y += 56

    # Divider
    draw_divider(draw, 60, y, 400, meta["tag_color"])
    y += 20

    # Headline
    h_font = get_font(72, bold=True)
    for line in meta["headline"].split('\n'):
        draw.text((60, y), line, font=h_font, fill=WHITE)
        bbox = draw.textbbox((0,0), line, font=h_font)
        y += bbox[3] - bbox[1] + 8
    y += 16

    # Sub
    sub_font = get_font(30)
    lines = wrap_text(meta["sub"], sub_font, W - 320, draw)
    for line in lines:
        draw.text((60, y), line, font=sub_font, fill=GRAY)
        bbox = draw.textbbox((0,0), line, font=sub_font)
        y += bbox[3] - bbox[1] + 6
    y += 40

    # Stat block
    stat_box_y = H - 220
    box_w = 380
    draw.rounded_rectangle([60, stat_box_y, 60+box_w, stat_box_y+110],
                            radius=12, fill=SURFACE, outline=(*meta["tag_color"],), width=1)
    s_font = get_font(48, bold=True)
    s_sub_font = get_font(22)
    draw.text((80, stat_box_y+12), meta["stats"][0], font=s_font, fill=meta["tag_color"])
    draw.text((80, stat_box_y+66), meta["stats"][1], font=s_sub_font, fill=GRAY)

    # Bottom line
    draw.line([(0, H-90), (W, H-90)], fill=(20, 40, 70), width=1)
    draw_logo(draw, 60, H-78)

    # Site
    site_font = get_font(20)
    draw.text((W-360, H-52), "sbabahnul-bot.github.io/4me-landing", font=site_font, fill=GRAY)

    img.save(f"{OUT}/{meta['file']}", quality=95)
    print(f"✓ {meta['file']}")

print(f"\nВсе 7 картинок сохранены в {OUT}")
