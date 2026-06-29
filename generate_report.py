from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.units import cm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, HRFlowable, KeepTogether)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
import os

# Register Cyrillic-compatible fonts
pdfmetrics.registerFont(TTFont('DVSans', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DVSans-Bold', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
FONT = 'DVSans'
FONT_BOLD = 'DVSans-Bold'

# Colors
DARK_BG = HexColor('#020610')
SURFACE = HexColor('#0d1829')
ACCENT = HexColor('#06b6d4')
ACCENT2 = HexColor('#0891b2')
TEXT = HexColor('#e8eaf0')
TEXT2 = HexColor('#94a3b8')
GREEN = HexColor('#10b981')
ORANGE = HexColor('#f59e0b')
RED = HexColor('#ef4444')
WHITE = HexColor('#ffffff')

OUTPUT = "/home/agent/projects/4me/bahmetev_ai_report.pdf"

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    rightMargin=1.8*cm,
    leftMargin=1.8*cm,
    topMargin=1.5*cm,
    bottomMargin=1.5*cm,
)

W, H = A4
content_width = W - 3.6*cm

styles = getSampleStyleSheet()

def style(name, **kw):
    s = ParagraphStyle(name, **kw)
    return s

S_TITLE = style('Title2', fontSize=26, leading=32, textColor=WHITE,
                fontName='DVSans-Bold', alignment=TA_CENTER, spaceAfter=4)
S_SUBTITLE = style('Sub', fontSize=13, leading=18, textColor=ACCENT,
                   fontName='DVSans', alignment=TA_CENTER, spaceAfter=20)
S_SECTION = style('Sec', fontSize=16, leading=20, textColor=ACCENT,
                  fontName='DVSans-Bold', spaceBefore=24, spaceAfter=8)
S_SUBSEC = style('Sub2', fontSize=12, leading=16, textColor=WHITE,
                 fontName='DVSans-Bold', spaceBefore=14, spaceAfter=6)
S_BODY = style('Body2', fontSize=10, leading=15, textColor=TEXT2,
               fontName='DVSans', spaceAfter=6)
S_BODY_W = style('BodyW', fontSize=10, leading=15, textColor=WHITE,
                 fontName='DVSans', spaceAfter=6)
S_BULLET = style('Bullet', fontSize=10, leading=15, textColor=TEXT2,
                 fontName='DVSans', leftIndent=12, spaceAfter=4,
                 bulletIndent=0)
S_LABEL = style('Label', fontSize=9, leading=12, textColor=ACCENT,
                fontName='DVSans-Bold', spaceAfter=2)
S_CAPTION = style('Cap', fontSize=8, leading=11, textColor=TEXT2,
                  fontName='DVSans', alignment=TA_CENTER)
S_DAY_TITLE = style('Day', fontSize=12, leading=16, textColor=WHITE,
                    fontName='DVSans-Bold', spaceAfter=4)
S_DAY_TAG = style('Tag', fontSize=9, leading=12, textColor=ACCENT,
                  fontName='DVSans-Bold', spaceAfter=6)
S_DAY_BODY = style('DBody', fontSize=9.5, leading=14, textColor=TEXT2,
                   fontName='DVSans', spaceAfter=6)
S_CTA = style('CTA', fontSize=9.5, leading=13, textColor=GREEN,
              fontName='DVSans-Bold', spaceAfter=4)

story = []

def hr(color=ACCENT, w=0.5):
    return HRFlowable(width='100%', thickness=w, color=color, spaceAfter=10, spaceBefore=4)

def cover_table():
    data = [[
        Paragraph('СТРАТЕГИЧЕСКИЙ ОТЧЁТ', S_TITLE),
    ],[
        Paragraph('@bahmetev_ai | AI для бизнеса', S_SUBTITLE),
    ],[
        Paragraph('Продвижение канала · Анализ рынка · Контент-план', S_CAPTION),
    ],[
        Paragraph('Подготовлен: 29 июня 2026 · Бахметьев.AI', S_CAPTION),
    ]]
    t = Table(data, colWidths=[content_width])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), SURFACE),
        ('TOPPADDING', (0,0), (-1,-1), 16),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 20),
        ('RIGHTPADDING', (0,0), (-1,-1), 20),
        ('ROUNDEDCORNERS', [8]),
    ]))
    return t

story.append(cover_table())
story.append(Spacer(1, 0.5*cm))

# ─── БЛОК 1: ПРОДВИЖЕНИЕ ───────────────────────────────────────────────────────
story.append(Paragraph('БЛОК 1: ПРОДВИЖЕНИЕ TELEGRAM-КАНАЛА', S_SECTION))
story.append(hr())

story.append(Paragraph('Бесплатные методы', S_SUBSEC))

free_methods = [
    ('Взаимный пиар (ВП)', 'Самый рабочий инструмент на старте. Ищи каналы в смежных нишах (бизнес-автоматизация, CRM, малый бизнес) с похожим числом подписчиков. Смотри на ER и просмотры, не на число — накрутчиков много.'),
    ('Комментинг', 'Содержательные комментарии в крупных каналах ниши: предпринимательство, маркетинг, IT, фитнес-бизнес. Медленно, но даёт качественных подписчиков.'),
    ('Telegram-папки', 'Попасть в тематическую подборку "Бизнес-боты" или "Автоматизация" — даёт органический прирост без вложений.'),
    ('Каталоги (бесплатно)', 'TGStat.ru, Tglist.ru, Telegator.ru — зарегистрировать канал и получить видимость при поиске.'),
    ('Кросс-постинг', 'Дублировать кейсы на VC.ru, Spark.ru, Habr со ссылкой на канал. Статья "Как бот увеличил продажи на X%" хорошо конвертирует.'),
]
for title, desc in free_methods:
    row = Table([[
        Paragraph(f'● {title}', S_SUBSEC),
        Paragraph(desc, S_BODY),
    ]], colWidths=[4.5*cm, content_width-4.5*cm])
    row.setStyle(TableStyle([
        ('VALIGN', (0,0),(-1,-1), 'TOP'),
        ('TOPPADDING', (0,0),(-1,-1), 0),
        ('BOTTOMPADDING', (0,0),(-1,-1), 6),
        ('LEFTPADDING', (0,0),(-1,-1), 0),
        ('RIGHTPADDING', (0,0),(-1,-1), 0),
    ]))
    story.append(row)

story.append(Spacer(1, 0.3*cm))
story.append(Paragraph('Платные методы и стоимость подписчика', S_SUBSEC))

price_data = [
    ['Метод', 'Ниша', 'Цена за подписчика'],
    ['Посевы в каналах', 'B2B / автоматизация', '450–800 ₽'],
    ['Посевы в каналах', 'Недвижимость', '210–525 ₽'],
    ['Посевы в каналах', 'Фитнес', '44–210 ₽'],
    ['Telegram Ads', 'B2B IT / автоматизация', '800–2 500 ₽'],
]
pt = Table(price_data, colWidths=[5.5*cm, 5.5*cm, 4.5*cm])
pt.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), ACCENT2),
    ('TEXTCOLOR', (0,0), (-1,0), WHITE),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,-1), 9),
    ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
    ('TEXTCOLOR', (0,1), (-1,-1), TEXT2),
    ('BACKGROUND', (0,1), (-1,1), SURFACE),
    ('BACKGROUND', (0,2), (-1,2), HexColor('#0a1520')),
    ('BACKGROUND', (0,3), (-1,3), SURFACE),
    ('BACKGROUND', (0,4), (-1,4), HexColor('#0a1520')),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [SURFACE, HexColor('#0a1520')]),
    ('GRID', (0,0), (-1,-1), 0.5, HexColor('#1e3a4a')),
    ('PADDING', (0,0), (-1,-1), 8),
    ('ALIGN', (2,0), (2,-1), 'CENTER'),
    ('FONTNAME', (2,1), (2,-1), 'Helvetica-Bold'),
    ('TEXTCOLOR', (2,1), (2,-1), GREEN),
]))
story.append(pt)
story.append(Paragraph('Бюджет на первые 1 000 подписчиков через посевы: 50 000–100 000 ₽. Telegram Ads для старта дорого — подходит при масштабировании.', S_BODY))

story.append(Spacer(1, 0.3*cm))
story.append(Paragraph('Контент, который растит канал', S_SUBSEC))

content_types = [
    ('🔥 Кейсы с цифрами', 'Самый виральный формат. "Фитнес-клуб: +287% продаж за 21 день". Репостят и сохраняют.'),
    ('📸 До/После', 'Скрин диалога бота vs. менеджер. Наглядно и убедительно.'),
    ('❌ Разборы ошибок', '"Почему внедрение AI-бота за 30 000 ₽ провалилось" — читают с удовольствием.'),
    ('📋 Чеклисты', '"5 вопросов перед покупкой бота" — сохраняют и пересылают.'),
    ('👤 Личные истории', 'Как строится продукт, что работает, что нет. Люди читают про людей.'),
]
for icon_title, desc in content_types:
    story.append(Paragraph(f'<b>{icon_title}</b> — {desc}', S_BODY))

story.append(Paragraph('❗ Что НЕ работает: корпоративные посты "наш бот умеет X, Y, Z". Аудитория читает про результаты, не про функции.', S_BODY_W))

# ─── БЛОК 2: АУДИТОРИЯ ────────────────────────────────────────────────────────
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph('БЛОК 2: ЦЕЛЕВАЯ АУДИТОРИЯ И РЫНОК', S_SECTION))
story.append(hr())

story.append(Paragraph('Боли и кейсы с цифрами', S_SUBSEC))

cases = [
    ('Фитнес-клуб, Москва', '+287% продаж за 21 день', '92% запросов без менеджеров, конверсия с 6% до 21%, время ответа 1.8 сек'),
    ('Фитнес-клуб, Казань', '-40% нагрузки на администраторов', 'Автоматизация ответов + онлайн-оформление + авторассылка акций'),
    ('Риелтор Алексей, Москва', '5 сделок за 3 мес. на 65 млн ₽', 'Ноль исходящих звонков на первичном этапе, время работы с клиентом -3x'),
    ('Metropolitan Estate', 'Конверсия +180%, расходы -60%, выручка ×3', 'Комплексное внедрение AI в воронку продаж'),
]
case_data = [['Клиент', 'Результат', 'Детали']] + cases
ct = Table(case_data, colWidths=[4*cm, 4.5*cm, content_width-8.5*cm])
ct.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), GREEN),
    ('TEXTCOLOR', (0,0), (-1,0), WHITE),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,-1), 8.5),
    ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
    ('TEXTCOLOR', (0,1), (-1,-1), TEXT2),
    ('TEXTCOLOR', (1,1), (1,-1), GREEN),
    ('FONTNAME', (1,1), (1,-1), 'Helvetica-Bold'),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [SURFACE, HexColor('#0a1520')]),
    ('GRID', (0,0), (-1,-1), 0.5, HexColor('#1e3a4a')),
    ('PADDING', (0,0), (-1,-1), 7),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
]))
story.append(ct)

story.append(Spacer(1, 0.4*cm))
story.append(Paragraph('Типичные возражения и контраргументы', S_SUBSEC))

objections = [
    ('"Дорого"', 'Показать ROI и кейс с конкретной окупаемостью. Средний рынок 50–150к — недообслуженная зона.'),
    ('"Боты раздражают клиентов"', '50% пользователей злятся на скриптовые боты. Показать разницу между конструктором и AI, который понимает контекст.'),
    ('"У нас специфика, не поймёт"', 'Демо + кейс из той же ниши. Лучше любых слов.'),
    ('"Пробовали — не работало"', 'Объяснить разницу: конструктор за 30к vs. AI-агент. Разные продукты.'),
    ('"Клиенты хотят живого общения"', 'Бот обрабатывает 80% рутины, освобождая менеджера для сложных случаев.'),
]
for obj, counter in objections:
    row = Table([[
        Paragraph(obj, style('Obj', fontSize=9, fontName='DVSans-Bold', textColor=ORANGE, leading=13)),
        Paragraph(counter, S_BODY),
    ]], colWidths=[3.8*cm, content_width-3.8*cm])
    row.setStyle(TableStyle([
        ('VALIGN', (0,0),(-1,-1), 'TOP'),
        ('TOPPADDING', (0,0),(-1,-1), 2),
        ('BOTTOMPADDING', (0,0),(-1,-1), 4),
        ('LEFTPADDING', (0,0),(-1,-1), 0),
        ('RIGHTPADDING', (0,0),(-1,-1), 0),
    ]))
    story.append(row)

story.append(Spacer(1, 0.3*cm))
story.append(Paragraph('Цены на AI-ботов в РФ (2025)', S_SUBSEC))

price2_data = [
    ['Формат', 'Стоимость'],
    ['Конструктор / шаблон', '5 000–30 000 ₽'],
    ['Настройка у интегратора', 'от 50 000 ₽'],
    ['Бот под ключ с AI', '200 000–500 000 ₽'],
    ['SaaS подписка (малый бизнес)', '6 000–15 000 ₽/мес'],
    ['Корпоративное решение', 'от 1 000 000 ₽'],
]
p2t = Table(price2_data, colWidths=[8*cm, content_width-8*cm])
p2t.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), ACCENT2),
    ('TEXTCOLOR', (0,0), (-1,0), WHITE),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,-1), 9),
    ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
    ('TEXTCOLOR', (0,1), (-1,-1), TEXT2),
    ('TEXTCOLOR', (1,3), (1,3), ORANGE),
    ('FONTNAME', (1,3), (1,3), 'Helvetica-Bold'),
    ('BACKGROUND', (0,3), (-1,3), HexColor('#1a2e1a')),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [SURFACE, HexColor('#0a1520')]),
    ('GRID', (0,0), (-1,-1), 0.5, HexColor('#1e3a4a')),
    ('PADDING', (0,0), (-1,-1), 8),
]))
story.append(p2t)
story.append(Paragraph('Позиционирование Ники и Агентуры: между "дешёвым конструктором за 30к" и "дорогой разработкой за 500к". Средний рынок (50–150 тыс. ₽) — недообслуженная зона с понятным ROI.', S_BODY_W))

# ─── БЛОК 3: КОНТЕНТ-ПЛАН ────────────────────────────────────────────────────
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph('БЛОК 3: КОНТЕНТ-ПЛАН НА НЕДЕЛЮ', S_SECTION))
story.append(hr())
story.append(Paragraph('30 июня — 6 июля 2026 · @bahmetev_ai', S_SUBTITLE))

days = [
    {
        'date': '30 июня, вторник',
        'format': 'Кейс / история',
        'tag_color': GREEN,
        'title': 'Фитнес-клуб терял 40% клиентов на этапе записи. Вот что изменилось за месяц',
        'body': 'Кейс с цифрами: администраторы не успевали отвечать ночью — люди уходили к конкурентам. После подключения Ники бот стал отвечать за 15 секунд 24/7. Через месяц: конверсия из заявки в первый визит +38%. Скрин переписки бота + цитата владельца.',
        'cta': 'CTA: «Хочешь такой разбор для своего клуба? Напиши — сделаю бесплатный аудит»',
    },
    {
        'date': '1 июля, среда',
        'format': 'Боль + решение',
        'tag_color': ORANGE,
        'title': 'Риелтор тратит 3 часа в день на вопросы, которые задают все подряд',
        'body': 'Типичный день риелтора: одни и те же вопросы — "а ипотеку можно?", "какие документы?". Агентура берёт этот слой на себя: квалифицирует, отвечает на базу, назначает встречу. Риелтор получает уже "тёплого" клиента. Конкретные диалоги бота.',
        'cta': 'CTA: «Попробуй Агентуру 7 дней бесплатно — ссылка в шапке канала»',
    },
    {
        'date': '2 июля, четверг',
        'format': 'Обучающий пост',
        'tag_color': ACCENT,
        'title': 'Как AI-бот понимает что хочет клиент — и не тупит как чат-бот из 2018-го',
        'body': 'Простое объяснение без жаргона: чем AI-администратор отличается от кнопочных ботов. Старый — дерево выборов. Новый — слышит смысл. Пример: клиент пишет "хочу похудеть, есть что для начинающих?" — и как Ника это обрабатывает. Аналогия: сотрудник который никогда не устаёт.',
        'cta': 'CTA: «Если интересно как это работает под капотом — ставь 🔥»',
    },
    {
        'date': '3 июля, пятница',
        'format': 'Личный пост',
        'tag_color': HexColor('#a855f7'),
        'title': 'Я 2 года объяснял людям зачем нужен AI. Потом перестал объяснять — и пошли продажи',
        'body': 'Честная история: продавать AI малому бизнесу было тяжело — все кивали, но не платили. Переломный момент — когда перестал говорить про технологии и начал про деньги и время. "Сколько заявок ты теряешь ночью?" работает лучше чем "у нас GPT-4 под капотом".',
        'cta': 'CTA: «Что для тебя важнее — технология или результат? Пиши в комментах»',
    },
    {
        'date': '4 июля, суббота',
        'format': 'Вовлечение / опрос',
        'tag_color': HexColor('#f43f5e'),
        'title': 'Быстрый опрос для владельцев бизнеса — 1 минута',
        'body': 'Telegram-опрос: "Что сейчас отнимает больше всего времени?" — варианты: ответы на вопросы клиентов / запись и напоминания / квалификация лидов / рутина. Комментарий Сергея: "Спрашиваю, потому что строю следующий продукт. Хочу попасть точно в боль."',
        'cta': 'CTA: «Проголосуй и напиши подробнее — разберу твой случай»',
    },
    {
        'date': '5 июля, воскресенье',
        'format': 'Вирусный / развлекательный',
        'tag_color': HexColor('#10b981'),
        'title': 'Диалог, который я подслушал между Никой и клиентом фитнес-клуба в 2:47 ночи',
        'body': 'Реальная переписка: клиент пишет боту ночью "хочу на йогу, но я как бревно — это реально?" Ника отвечает с юмором и по делу, записывает на вводное. Скрин переписки + комментарий: "Пока владелец спал, бот сделал продажу." Хорошо шерится.',
        'cta': 'CTA: «Покажи это своему администратору 😄 У тебя кто отвечает в 3 ночи?»',
    },
    {
        'date': '6 июля, понедельник',
        'format': 'Продающий пост',
        'tag_color': ORANGE,
        'title': 'Июль — время настроить AI-бота, пока конкуренты в отпуске',
        'body': 'Летом трафик не падает, а скорость ответа конкурентов проседает (команды в отпусках). Это окно возможностей. Что входит в подключение: настройка под бизнес, обучение на скриптах, интеграция, поддержка 2 недели. Срок готовности: 5–7 дней.',
        'cta': 'CTA: «Заявка до 10 июля — подключу в приоритете + первый месяц -20%»',
    },
]

for day in days:
    elements = [
        Table([[
            Table([[
                Paragraph(day['date'], S_LABEL),
                Paragraph(day['title'], S_DAY_TITLE),
                Paragraph(f'▶ {day["format"]}', style('Fmt', fontSize=9, fontName='DVSans-Bold',
                    textColor=day['tag_color'], leading=12, spaceAfter=6)),
                Paragraph(day['body'], S_DAY_BODY),
                Paragraph(day['cta'], S_CTA),
            ]], colWidths=[content_width - 0.4*cm])
        ]], colWidths=[content_width])
    ]
    t = elements[0]
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), SURFACE),
        ('TOPPADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ('LEFTPADDING', (0,0), (-1,-1), 16),
        ('RIGHTPADDING', (0,0), (-1,-1), 16),
        ('LINEAFTER', (0,0), (0,-1), 3, day['tag_color']),
    ]))
    story.append(KeepTogether([t, Spacer(1, 0.25*cm)]))

# Footer note
story.append(Spacer(1, 0.5*cm))
story.append(hr(TEXT2, 0.3))
story.append(Paragraph('Бахметьев.AI · @bahmetev_ai · sbabahnul-bot.github.io/4me-landing · Отчёт подготовлен 29 июня 2026', S_CAPTION))

def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(DARK_BG)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)
    canvas.setFillColor(TEXT2)
    canvas.setFont('Helvetica', 8)
    canvas.drawRightString(W - 1.8*cm, 0.8*cm, f'стр. {doc.page}')
    canvas.restoreState()

doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print(f"PDF создан: {OUTPUT}")
