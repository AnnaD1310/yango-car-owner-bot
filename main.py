from aiogram import Bot, Dispatcher, F

from aiogram.filters import CommandStart

from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile

from aiogram.utils.keyboard import InlineKeyboardBuilder

from aiogram.enums import ParseMode

from aiogram.client.default import DefaultBotProperties

from dotenv import load_dotenv

import asyncio, os

from dataclasses import dataclass

from typing import Dict, List, Tuple



# ---------- CONFIG ----------

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    print("ОШИБКА: BOT_TOKEN не найден в .env файле!")
    exit(1)

print(f"Токен загружен: {BOT_TOKEN[:10]}...")

bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp = Dispatcher()



@dataclass

class Link:

    title: str

    url: str



# ---------- CONTENT (редактируй под себя) ----------

CONTENT: Dict[str, dict] = {

    "main": {

        "title": "Yango Car Owner Acquisition Assistant",

        "subtitle": "Select a section:",

        "menu": [

            ("🚀 Start launch", "start_launch"),

            ("📘 Materials & templates", "materials"),

            ("💬 Communication flows", "flows"),

            ("📊 Reports & KPI", "reports"),

            ("💡 FAQ", "faq:0"),

            ("👥 Contacts", "contacts"),

        ],

    },

    "start_launch": {

        "intro": (

            "We'll guide you through the launch steps:\n"

            "1) Market & model check\n"

            "2) Choose channel (Landing / WhatsApp)\n"

            "3) Lead collection (Forms → Sheets)\n"

            "4) Marketing & launch\n"

            "5) Monitoring & weekly report"

        ),

        "steps": [

            {

                "title": "Step 1 — Market & model check",

                "text": (

                    "• Review participation models (Full Management / Sub-fleet)\n"

                    "• Validate accepted models/years/mileage/insurance\n"

                    "• Collect local insights (demand, competitors, pricing)\n"

                    "• Use the Market Research template"

                ),

                "links": [

                    Link("Market Research Template (Sheet)", "https://example.com/market-template"),

                    Link("Sample market report (PDF)", "https://example.com/sample-report"),

                ],

            },

            {

                "title": "Step 2 — Choose your channel",

                "text": "Pick primary flow and mirror its steps:",

                "links": [

                    Link("Landing — Angola", "https://yango.com/en_ao/carinvest"),

                    Link("Landing — Zambia", "https://yango.com/en_zm/carinvest"),

                    Link("Landing — Cameroon", "https://yango.com/en_cm/carinvest"),

                    Link("WA flow — Miro (draft)", "https://miro.com/app/board/uXjVIMV2lOk=/"),

                ],

            },

            {

                "title": "Step 3 — Lead collection",

                "text": (

                    "Create a Google Form for leads and auto-sync to Sheets.\n"

                    "Fields: Name, WhatsApp, Email, #cars, attribution, consent."

                ),

                "links": [

                    Link("Create Google Form", "https://docs.google.com/forms"),

                    Link("Tracker example (Sheet)", "https://docs.google.com/spreadsheets/d/1WhA1pt725L9uGHG6pDDRx5iFxSz2xPRuGJJGIPsAoAA/edit"),

                ],

            },

            {

                "title": "Step 4 — Marketing & launch",

                "text": "Plan 2–4 weeks. Use existing banners, OOH, flyers, texts.",

                "links": [

                    Link("Perf banners (Figma)", "https://www.figma.com/design/GJ7bVwfVs0zjD84ZqmPohO/205-Perf-campaign_Luanda_Car-owners-acquisition?node-id=188-2"),

                    Link("OOH (Figma)", "https://www.figma.com/design/aENCAQUznQPAtuZL1bvO6H/Yango-Angola---OOH-car--moto-owners----Angola----Luanda----General?node-id=0-1"),

                    Link("Texts (Doc)", "https://docs.google.com/document/d/1FJ5qB6ytZ6GZ1Vn_7QKFjp_jOdFmAVDJV2r_L4jsDmY/edit"),

                ],

            },

            {

                "title": "Step 5 — Monitoring & weekly report",

                "text": "Track CPL, #leads, #contracts, #active cars, retention. Submit weekly.",

                "links": [

                    Link("KPI Tracker (Sheet)", "https://docs.google.com/spreadsheets/d/1G43o8VMwbvrzNniwv8fOVm1W_xOawFLbfTZusbaDtZI/edit"),

                ],

            },

        ],

    },

    "materials": {

        "blocks": [

            ("Contracts", [

                Link("Contract template (EN)", "https://example.com/contract-en"),

                Link("Contract template (PT)", "https://example.com/contract-pt"),

            ]),

            ("Trackers", [

                Link("Lead tracker (Sheet)", "https://docs.google.com/spreadsheets/d/1WhA1pt725L9uGHG6pDDRx5iFxSz2xPRuGJJGIPsAoAA/edit"),

                Link("KPI tracker (Sheet)", "https://docs.google.com/spreadsheets/d/1G43o8VMwbvrzNniwv8fOVm1W_xOawFLbfTZusbaDtZI/edit"),

            ]),

            ("Landing brief", [

                Link("Landing content template (Sheet)", "https://docs.google.com/spreadsheets/d/1IJbO26krjPKekR1aKZ4Q6SiwL45BPJiG2PsQ-jL7RFY/edit"),

                Link("Create web ticket", "https://st.yandex-team.ru/createTicket?queue=YANGOWEB&_form=false"),

            ]),

            ("Creatives", [

                Link("Performance banners (Figma)", "https://www.figma.com/design/GJ7bVwfVs0zjD84ZqmPohO/205-Perf-campaign_Luanda_Car-owners-acquisition?node-id=188-2"),

                Link("OOH (Figma)", "https://www.figma.com/design/aENCAQUznQPAtuZL1bvO6H/Yango-Angola---OOH-car--moto-owners----Angola----Luanda----General?node-id=0-1"),

                Link("Flyers (Figma)", "https://www.figma.com/design/2Dg2jkvZKmDLxFTQYYPkHK/Yango-Angola---Flyers-for-ANGOTIC-conference-in-Angola---General?node-id=12-2"),

            ]),

            ("Texts", [

                Link("Texts (Sheet)", "https://docs.google.com/spreadsheets/d/1zNS5aUVxY5StLQ0J01TVHhpuqQjoy4YVARBBmFJ2Ra8/edit"),

                Link("WA/Posts texts (Doc)", "https://docs.google.com/document/d/1FJ5qB6ytZ6GZ1Vn_7QKFjp_jOdFmAVDJV2r_L4jsDmY/edit"),

            ]),

        ]

    },

    "flows": {

        "landing": [

            "1) Ad click → Landing page",

            "2) Value prop & requirements",

            "3) Form → lead captured",

            "4) Lead to sheet, daily calls",

            "5) Office visit, docs & car check",

            "6) Contract signing",

            "7) Add car to fleet system",

        ],

        "whatsapp": [

            "1) Ad click → WA chat",

            "2) Greeting & quick questions",

            "3) Follow-up if no reply",

            "4) Create chat with partner",

            "5) Office visit, checks",

            "6) Contract signing",

            "7) Add car to fleet system",

        ],

        "links": [

            Link("Angola landing", "https://yango.com/en_ao/carinvest"),

            Link("Zambia landing", "https://yango.com/en_zm/carinvest"),

            Link("Cameroon landing", "https://yango.com/en_cm/carinvest"),

        ],

        "wa_texts": [

            "Greeting: Hi! Thanks for your interest in Yango Car Invest…",

            "Follow-up (24h): Just checking if you're still interested…",

            "Thank you: We'll review your info and contact you on WhatsApp…",

        ],

    },

    "reports": {

        "kpi": ["Leads", "% leads → contracts", "Active cars", "CPL / CPA", "Retention 2/4/8 weeks"],

        "links": [

            Link("KPI tracker (Sheet)", "https://docs.google.com/spreadsheets/d/1G43o8VMwbvrzNniwv8fOVm1W_xOawFLbfTZusbaDtZI/edit"),

            Link("Lead tracker (Sheet)", "https://docs.google.com/spreadsheets/d/1WhA1pt725L9uGHG6pDDRx5iFxSz2xPRuGJJGIPsAoAA/edit"),

        ],

    },

    "faq": {

        "items": [

            ("Eligibility — models & mileage", "Accepted small city cars 2018–2025; mileage guidance applies; insurance required."),

            ("Docs required", "Ownership proof, ID, insurance details depending on partner."),

            ("Payments", "Weekly payouts via partner; online performance tracking available."),

            ("Safety & insurance", "Responsibilities & coverage per partner policy."),

            ("Scaling 1→5 cars", "Start with 1; sub-fleet model from 3+ with more control."),

        ],

        "page_size": 3,

    },

    "contacts": {

        "people": [

            ("Marketing — Anna Dolgova", "https://t.me/your_handle_here"),

            ("Operations — Nikhar", "https://t.me/nikhar_here"),

        ]

    }

}


CONTRACT_FILES: Dict[str, Tuple[str, str]] = {
    "en": ("Contract Template — English (Zambia)", "resources/contracts/Contract Eng (Zambia).docx"),
    "pt": ("Modelo de Contrato — Português (Angola)", "resources/contracts/Contract Portu (Angola).pdf"),
    "fr": ("Modèle de Contrat — Français (Cameroon)", "resources/contracts/Сontract FR (Cameroon).pdf"),
}


# ---------- UI HELPERS ----------

def main_menu_kb() -> InlineKeyboardMarkup:

    kb = InlineKeyboardBuilder()

    for title, cb in CONTENT["main"]["menu"]:

        kb.button(text=title, callback_data=cb)

    kb.adjust(1)  # По одной кнопке в ряд

    return kb.as_markup()



def links_kb(links: List[Link], back_cb: str) -> InlineKeyboardMarkup:

    kb = InlineKeyboardBuilder()

    for link in links:

        kb.button(text=f"🔗 {link.title}", url=link.url)

    kb.button(text="⬅️ Back", callback_data=back_cb)

    kb.adjust(1)

    return kb.as_markup()



def step_kb(step_idx: int, total: int) -> InlineKeyboardMarkup:

    kb = InlineKeyboardBuilder()

    if step_idx > 0:

        kb.button(text="⬅️ Prev", callback_data=f"launch_step:{step_idx-1}")

    if step_idx < total - 1:

        kb.button(text="Next ➡️", callback_data=f"launch_step:{step_idx+1}")

    kb.button(text="🏠 Menu", callback_data="home")

    kb.adjust(2)

    return kb.as_markup()



def faq_page_kb(page: int) -> InlineKeyboardMarkup:

    size = CONTENT["faq"]["page_size"]

    total_items = len(CONTENT["faq"]["items"])

    total_pages = (total_items + size - 1) // size

    kb = InlineKeyboardBuilder()

    if page > 0:

        kb.button(text="⬅️ Prev", callback_data=f"faq:{page-1}")

    if page < total_pages - 1:

        kb.button(text="Next ➡️", callback_data=f"faq:{page+1}")

    kb.button(text="🏠 Menu", callback_data="home")

    kb.adjust(2)

    return kb.as_markup()


def contracts_kb() -> InlineKeyboardMarkup:

    kb = InlineKeyboardBuilder()
    for code, (title, _) in CONTRACT_FILES.items():
        kb.button(text=title, callback_data=f"contract_file:{code}")
    kb.button(text="⬅️ Back", callback_data="materials")
    kb.button(text="🏠 Menu", callback_data="home")
    kb.adjust(1)
    return kb.as_markup()



# ---------- HANDLERS ----------

@dp.message(CommandStart())

async def on_start(msg: Message):

    try:
        print(f"Received /start from user {msg.from_user.id}")

        main = CONTENT["main"]

        text = f"<b>{main['title']}</b>\n{main['subtitle']}"

        keyboard = main_menu_kb()
        print(f"Keyboard created, sending message...")

        await msg.answer(text, reply_markup=keyboard)
        
        print("Sent menu to user")
    except Exception as e:
        print(f"Error in on_start: {e}")
        import traceback
        traceback.print_exc()
        try:
            await msg.answer(f"Произошла ошибка: {str(e)}")
        except:
            pass



@dp.callback_query(F.data == "home")

async def on_home(cb: CallbackQuery):

    try:
        main = CONTENT["main"]

        text = f"<b>{main['title']}</b>\n{main['subtitle']}"

        await cb.message.edit_text(text, reply_markup=main_menu_kb())

        await cb.answer()
    except Exception as e:
        print(f"Error in on_home: {e}")
        await cb.answer("Произошла ошибка", show_alert=True)



# Start launch

@dp.callback_query(F.data == "start_launch")

async def on_start_launch(cb: CallbackQuery):

    intro = CONTENT["start_launch"]["intro"]

    await cb.message.edit_text(f"<b>Start Launch — Wizard</b>\n\n{intro}",

                               reply_markup=step_kb(0, len(CONTENT["start_launch"]["steps"])))

    await cb.answer()



@dp.callback_query(F.data.startswith("launch_step:"))

async def on_launch_step(cb: CallbackQuery):

    idx = int(cb.data.split(":")[1])

    steps = CONTENT["start_launch"]["steps"]

    idx = max(0, min(idx, len(steps)-1))

    step = steps[idx]

    text = f"<b>{step['title']}</b>\n\n{step['text']}"

    if step.get("links"):

        await cb.message.edit_text(text)

        await cb.message.edit_reply_markup(reply_markup=links_kb(step["links"], back_cb=f"launch_step:{idx}"))

    else:

        await cb.message.edit_text(text, reply_markup=step_kb(idx, len(steps)))

    await cb.answer()



# Materials

@dp.callback_query(F.data == "materials")

async def on_materials(cb: CallbackQuery):

    blocks = CONTENT["materials"]["blocks"]

    kb = InlineKeyboardBuilder()

    for i, (title, _) in enumerate(blocks):

        kb.button(text=f"📁 {title}", callback_data=f"materials_block:{i}")

    kb.button(text="🏠 Menu", callback_data="home")

    kb.adjust(1)

    await cb.message.edit_text("<b>Materials & templates</b>\nPick a category:", reply_markup=kb.as_markup())

    await cb.answer()



@dp.callback_query(F.data.startswith("materials_block:"))

async def on_materials_block(cb: CallbackQuery):

    idx = int(cb.data.split(":")[1])

    title, links = CONTENT["materials"]["blocks"][idx]

    if title == "Contracts":
        await cb.answer()
        await cb.message.answer("<b>Contracts</b>\nChoose a language:", reply_markup=contracts_kb())
        return
    else:
        await cb.message.edit_text(f"<b>{title}</b>")
        await cb.message.edit_reply_markup(reply_markup=links_kb(links, back_cb="materials"))

    await cb.answer()



# Flows

@dp.callback_query(F.data == "flows")

async def on_flows(cb: CallbackQuery):

    landing = "\n".join(f"• {s}" for s in CONTENT["flows"]["landing"])

    wa = "\n".join(f"• {s}" for s in CONTENT["flows"]["whatsapp"])

    text = f"<b>Communication flows</b>\n\n<u>Landing flow</u>\n{landing}\n\n<u>WhatsApp flow</u>\n{wa}"

    kb = InlineKeyboardBuilder()

    for link in CONTENT["flows"]["links"]:

        kb.button(text=f"🔗 {link.title}", url=link.url)

    kb.button(text="⬅️ Back", callback_data="home")

    kb.adjust(1)

    await cb.message.edit_text(text, reply_markup=kb.as_markup())

    await cb.answer()



# Reports

@dp.callback_query(F.data == "reports")

async def on_reports(cb: CallbackQuery):

    kpis = "\n".join(f"• {k}" for k in CONTENT["reports"]["kpi"])

    text = f"<b>Reports & KPI</b>\n\nTrack weekly:\n{kpis}"

    await cb.message.edit_text(text)

    await cb.message.edit_reply_markup(reply_markup=links_kb(CONTENT["reports"]["links"], back_cb="home"))

    await cb.answer()



# FAQ (pagination)

@dp.callback_query(F.data.startswith("faq:"))

async def on_faq(cb: CallbackQuery):

    page = int(cb.data.split(":")[1])

    items = CONTENT["faq"]["items"]

    size = CONTENT["faq"]["page_size"]

    start, end = page*size, min((page+1)*size, len(items))

    chunk = items[start:end]

    lines = ["<b>FAQ</b>\n"]

    for q, a in chunk:

        lines.append(f"<b>• {q}</b>\n{a}\n")

    await cb.message.edit_text("\n".join(lines).strip(), reply_markup=faq_page_kb(page))

    await cb.answer()



# Contacts

@dp.callback_query(F.data == "contacts")

async def on_contacts(cb: CallbackQuery):

    people: List[Tuple[str, str]] = CONTENT["contacts"]["people"]

    kb = InlineKeyboardBuilder()

    for name, url in people:

        kb.button(text=name, url=url)

    kb.button(text="⬅️ Back", callback_data="home")

    kb.adjust(1)

    await cb.message.edit_text("<b>Contacts</b>\nTap to open Telegram:", reply_markup=kb.as_markup())

    await cb.answer()


@dp.callback_query(F.data.startswith("contract_file:"))

async def on_contract_file(cb: CallbackQuery):

    code = cb.data.split(":")[1]

    meta = CONTRACT_FILES.get(code)

    if not meta:

        await cb.answer("File not found", show_alert=True)

        return

    title, path = meta

    try:

        document = FSInputFile(path)

    except FileNotFoundError:

        await cb.answer("Contract file is missing", show_alert=True)

        return

    await cb.message.answer_document(document, caption=title)

    await cb.answer()



# ---------- RUN ----------

async def main():

    print("Bot running with menu…")
    print("Ожидание сообщений...")

    try:
        await dp.start_polling(bot)
    except Exception as e:
        print(f'Ошибка при polling: {e}')
        import traceback
        traceback.print_exc()
        raise



if __name__ == "__main__":

    asyncio.run(main())
