#!/usr/bin/env python3
"""
Запусти этот скрипт, и он создаст страницу в Notion автоматически.
Требуется Python 3 (обычно уже установлен на Mac).

Mac/Linux:  python3 create_notion_page.py
Windows:    python create_notion_page.py
"""

import json, urllib.request, urllib.error

TOKEN = "ВСТАВЬ_СВОЙ_ТОКЕН_СЮДА"          # notion.so/my-integrations → Internal Integration Secret
PARENT_ID = "377dded983ed8087b302d3419e9a00b8"  # ID родительской страницы

# ── helpers ──────────────────────────────────────────────────────────────────

def t(content, bold=False, color="default"):
    rt = {"type": "text", "text": {"content": content}}
    ann = {}
    if bold: ann["bold"] = True
    if color != "default": ann["color"] = color
    if ann: rt["annotations"] = ann
    return rt

def b(content): return t(content, bold=True)

def para(*parts, color="default"):
    return {"object":"block","type":"paragraph",
            "paragraph":{"rich_text":list(parts),"color":color}}

def h2(*parts):
    return {"object":"block","type":"heading_2",
            "heading_2":{"rich_text":list(parts),"is_toggleable":False}}

def h3(*parts):
    return {"object":"block","type":"heading_3",
            "heading_3":{"rich_text":list(parts),"is_toggleable":False}}

def div():
    return {"object":"block","type":"divider","divider":{}}

def bul(*parts):
    return {"object":"block","type":"bulleted_list_item",
            "bulleted_list_item":{"rich_text":list(parts)}}

def num(*parts):
    return {"object":"block","type":"numbered_list_item",
            "numbered_list_item":{"rich_text":list(parts)}}

def callout(emoji, color, *parts):
    return {"object":"block","type":"callout","callout":{
        "rich_text":list(parts),
        "icon":{"type":"emoji","emoji":emoji},
        "color":color+"_background"
    }}

def quote(*parts):
    return {"object":"block","type":"quote","quote":{"rich_text":list(parts)}}

def row(*cells):
    return {"object":"block","type":"table_row",
            "table_row":{"cells":[[t(c)] for c in cells]}}

def table(rows, has_header=True):
    w = len(rows[0]) if rows else 2
    return {"object":"block","type":"table","table":{
        "table_width":w,"has_column_header":has_header,"has_row_header":False
    },"children":[row(*r) for r in rows]}

# ── blocks ────────────────────────────────────────────────────────────────────

blocks = [
    callout("💡","blue",
        b("Коротко о позиции. "),
        t("Ты — первая точка контакта клиента с агентством. Пишешь людям в Telegram, прогреваешь и передаёшь заинтересованных на созвон. От твоей работы зависит оборот агентства в "),
        b("1 500 000 ₽ за лето"),t(".")),
    div(),

    h2(b("🏷️ Общая информация")),
    table([
        ["Параметр","Значение"],
        ["📍 Формат","Удалённо, 2–3 часа в день"],
        ["💰 Зарплата","20 000 – 110 000 ₽ / месяц"],
        ["⚡ Тип задач","Telegram-рассылки, прогрев лидов"],
        ["📅 Старт","Как можно скорее · июнь 2025"],
        ["✉️ Контакт","@Kirill_konstantinvich"],
    ]),
    div(),

    h2(b("📋 Задача")),
    para(t("Ты — первая точка контакта. Пишешь первым, прогреваешь, передаёшь тёплых лидов на созвон с операционным директором.")),
    bul(b("📲 50 ручных рассылок "),t("в Telegram по выданной базе — строго по согласованному скрипту")),
    bul(b("🔥 Прогрев входящих "),t("— выявляешь боль, задаёшь вопросы, доводишь до записи на созвон")),
    bul(b("🎯 Передача лидов "),t("— готового клиента передаёшь ОД. Продажа воронки за 150к+ — уже не твоя задача")),
    bul(b("💎 Не сливаешь ни одного ответа "),t("— каждый ответ потенциально 150 000 ₽, всё фиксируется")),
    bul(b("📊 Отчёт каждый вечер "),t("— сам, без напоминаний: отправлено / ответили / заинтересовались / на созвон")),
    quote(t("«Ты не просто рассыльщик. Ты первая точка контакта клиента с агентством. От тебя зависит, выйдем ли мы на 1 млн за лето или нет.»")),
    para(t("— Кирилл Кузнецов, основатель агентства"), color="gray"),
    div(),

    h2(b("⚙️ Как это работает")),
    para(t("Три шага — каждый день, без выходных.")),
    num(b("Рассылки. "),t("50 сообщений по базе ежедневно. Скрипт выдаётся и согласовывается с ОД. Самодеятельность — не приветствуется.")),
    num(b("Обработка входящих. "),t("Все ответы — в течение 1–2 часов. Прогрев, вопросы, довести до созвона. Тёплый лид передаёшь ОД.")),
    num(b("Отчёт каждый вечер. "),t("Отправлено / ответили / заинтересовались / на созвон. Сам, без напоминаний.")),
    callout("🕐","gray",b("Твой день: "),t("утром рассылки (~1.5 ч), днём входящие (~1 ч), вечером отчёт (5–10 мин). Всё остальное время — свободен.")),
    div(),

    h2(b("🎯 KPI и конверсия")),
    table([
        ["Уровень","Продажи / мес","Зарплата"],
        ["🟡 Минимум","3 продажи","20–30 000 ₽"],
        ["🟢 План","5 продаж","30 000 ₽ + 20 000 ₽ / доп. продажа"],
        ["🔥 Бог-продажник","6+ продаж","110 000+ ₽"],
    ]),
    h3(b("Математика конверсии")),
    table([
        ["Рассылок","Ответили ~8%","Созвоны","Продажи"],
        ["1 000","~80","~16","1 продажа"],
        ["3 000","~240","~48","3 продажи"],
        ["5 000","~400","~80","5 продаж ✓"],
    ]),
    callout("📊","yellow",b("Вывод: "),t("50 рассылок × 100 дней = 5 000 рассылок = ~5 продаж в месяц. Объём = деньги.")),
    div(),

    h2(b("💰 Зарплата — подробно")),
    para(t("Никаких серых схем. Считается прозрачно.")),
    table([
        ["Уровень","Продажи / мес","Оклад","Бонус","Итого"],
        ["🟡 Минимум","3","20–30 000 ₽","—","20–30 000 ₽"],
        ["🟢 План","5","30 000 ₽","+20 000 ₽ / продажа сверх 3","70 000 ₽"],
        ["🔥 Бог","6+","30 000 ₽","Повышенная ставка","110 000+ ₽"],
    ]),
    h3(b("Пример расчёта — 7 продаж за месяц")),
    table([
        ["Статья","Сумма"],
        ["Базовый оклад (3 продажи)","30 000 ₽"],
        ["4 доп. продажи × 20 000 ₽","80 000 ₽"],
        ["Итого за месяц","110 000 ₽"],
    ]),
    div(),

    h2(b("📏 Правила работы")),
    num(b("Отчёт каждый день "),t("— сам, в конце дня, без напоминаний")),
    num(b("Скорость ответа "),t("— все входящие в течение 1–2 часов")),
    num(b("Проблемы — сразу "),t("— блок, нет базы, не получается → пишешь ОД немедленно")),
    num(b("Скрипт согласован "),t("— самодеятельность в переписке с клиентами не приветствуется")),
    num(b("Дедлайны — свято "),t("— не переносишь без предупреждения")),
    h3(b("❌ Прощаемся, если")),
    callout("🚫","red",
        t("• Несколько раз подряд не выполняется базовый минимум (3 продажи)\n"
          "• Переносишь дедлайны и не предупреждаешь\n"
          "• Недобросовестно относишься к отчётности\n"
          "• Теряешь тёплых клиентов из-за невнимательности")),
    callout("⚠️","gray",t("Это удалённая работа — но это не значит, что правил нет. "
                           "Единственная разница с офисом: у нас высокостоящий продукт и мы работаем полностью удалённо.")),
    div(),

    h2(b("🚀 Цель на лето 2025")),
    table([
        ["Метрика","Цель"],
        ["Оборот агентства","1 500 000 ₽ за июнь–август"],
        ["Продаж","10 воронок за 3 месяца"],
        ["Рассылок","~15 000 за лето"],
    ]),
    callout("🔑","orange",
        b("Ты — ключевое звено этой системы. "),
        t("Без тебя нет рассылок → нет продаж → нет агентства. Мы растём вместе.")),
    div(),

    h2(b("✉️ Как откликнуться")),
    callout("✉️","blue",
        b("Напиши в Telegram: РАССЫЛКИ + пару слов о себе\n\n"),
        t("→ @Kirill_konstantinvich")),
    para(t("Агентство Кирилла Кузнецова · Воронки продаж от 150 000 ₽ · Удалённо"),
         color="gray"),
]

# ── API call ──────────────────────────────────────────────────────────────────

payload = {
    "parent": {"type": "page_id", "page_id": PARENT_ID},
    "icon":   {"type": "emoji", "emoji": "📲"},
    "properties": {
        "title": {"title": [{"type":"text","text":{"content":"Ассистент по рассылкам"}}]}
    },
    "children": blocks
}

data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
req = urllib.request.Request(
    "https://api.notion.com/v1/pages",
    data=data,
    headers={
        "Authorization":  f"Bearer {TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type":   "application/json",
    },
    method="POST"
)

try:
    with urllib.request.urlopen(req) as resp:
        body = json.loads(resp.read().decode("utf-8"))
    page_id = body["id"].replace("-", "")
    url = f"https://www.notion.so/{page_id}"
    print(f"\n✅ Готово! Страница создана:\n{url}\n")
except urllib.error.HTTPError as e:
    err = json.loads(e.read().decode("utf-8"))
    print(f"\n❌ Ошибка {e.code}: {err.get('message','')}")
    print("Подсказка: убедись, что интеграция подключена к родительской странице (⋯ → Add connections).")
