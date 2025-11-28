import asyncio
import os
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from aiogram import Bot, Dispatcher, F, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    Message,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv


# ---------- CONFIG ----------

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise SystemExit("BOT_TOKEN not found in .env")

bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
router = Router()
dp.include_router(router)


# ---------- MENU DATA MODEL ----------

@dataclass
class MenuNode:
    id: str
    title: str
    text: str
    parent_id: Optional[str]
    next_id: Optional[str]
    children: List[Tuple[str, str]]  # (button_text, child_node_id)


# Root and sections ---------------------------------------------------------

MENU: Dict[str, MenuNode] = {}


def add_node(node: MenuNode) -> None:
    MENU[node.id] = node


# Root
add_node(
    MenuNode(
        id="root",
        title="Yango Car Owner Acquisition Assistant",
        text=(
            "<b>Yango Car Owner Acquisition Assistant</b>\n\n"
            "Select a section:"
        ),
        parent_id=None,
        next_id=None,
        children=[
            ("🚀 Start Country Launch", "start_launch"),
            ("📂 Templates & Materials", "templates"),
            ("🔀 Communication Flows", "flows"),
            ("📊 KPI & Reporting", "kpi"),
            ("❓ FAQ", "faq"),
            ("👥 Contacts", "contacts"),
        ],
    )
)


# 1. Start Country Launch ---------------------------------------------------

start_launch_steps_order = [
    "start_launch_step_1",
    "start_launch_step_2",
    "start_launch_step_3",
    "start_launch_step_4",
    "start_launch_step_5",
    "start_launch_step_6",
    "start_launch_step_7",
]

add_node(
    MenuNode(
        id="start_launch",
        title="Start Country Launch",
        text=(
            "<b>Start Country Launch</b>\n\n"
            "Follow these steps to launch a car-owner acquisition stream in a new country."
        ),
        parent_id="root",
        next_id=None,
        children=[
            ("Step 1 — Market & Model", "start_launch_step_1"),
            ("Step 2 — Ops Readiness", "start_launch_step_2"),
            ("Step 3 — Acquisition Channels", "start_launch_step_3"),
            ("Step 4 — Lead Processing", "start_launch_step_4"),
            ("Step 5 — Partner Activation", "start_launch_step_5"),
            ("Step 6 — Reporting & KPI", "start_launch_step_6"),
            ("Step 7 — Go Live Checklist", "start_launch_step_7"),
        ],
    )
)

# Individual steps ----------------------------------------------------------

add_node(
    MenuNode(
        id="start_launch_step_1",
        title="Step 1 — Market & Model",
        text=(
            "<b>Step 1 — Market & Model</b>\n\n"
            "<b>What to do:</b>\n"
            "• Run basic market research (size of city, car ownership, typical income).\n"
            "• Understand existing patterns: are people already renting out cars?\n"
            "• Identify potential partner profiles (small fleets, individuals, SMEs).\n"
            "• Build a financial model to estimate unit economics.\n\n"
            "<b>Use:</b>\n"
            "• Market analysis checklist\n"
            "• Financial model template\n"
            "• Examples of research from Zambia and Angola."
        ),
        parent_id="start_launch",
        next_id="start_launch_step_2",
        children=[],
    )
)

add_node(
    MenuNode(
        id="start_launch_step_2",
        title="Step 2 — Ops Readiness",
        text=(
            "<b>Step 2 — Ops Readiness</b>\n\n"
            "Before launch, make sure operations are ready:\n\n"
            "• Scouts and call-center flow defined and documented.\n"
            "• Contracts are prepared and localized.\n"
            "• Partners onboarding process is clear.\n"
            "• Lead handling script is prepared for scouts / call center."
        ),
        parent_id="start_launch",
        next_id="start_launch_step_3",
        children=[],
    )
)

add_node(
    MenuNode(
        id="start_launch_step_3",
        title="Step 3 — Acquisition Channels",
        text=(
            "<b>Step 3 — Acquisition Channels</b>\n\n"
            "Choose your primary channel and mirror existing flows.\n\n"
            "<b>Landing flow:</b>\n"
            "• Follow the standard landing structure.\n"
            "• Re-use best performing landing examples (Zambia, Angola, Cameroon, Ethiopia).\n"
            "• Align tracking with central team.\n\n"
            "<b>WhatsApp flow:</b>\n"
            "• Configure WA business account.\n"
            "• Set auto greeting message.\n"
            "• Re-use scripts for first interaction."
        ),
        parent_id="start_launch",
        next_id="start_launch_step_4",
        children=[],
    )
)

add_node(
    MenuNode(
        id="start_launch_step_4",
        title="Step 4 — Lead Processing",
        text=(
            "<b>Step 4 — Lead Processing</b>\n\n"
            "<b>What to define:</b>\n"
            "• Lead qualification rules (who is a good lead).\n"
            "• Scripts for calling and follow-up.\n"
            "• SLA: how fast you must contact each lead.\n"
            "• Examples of good and bad leads."
        ),
        parent_id="start_launch",
        next_id="start_launch_step_5",
        children=[],
    )
)

add_node(
    MenuNode(
        id="start_launch_step_5",
        title="Step 5 — Partner Activation",
        text=(
            "<b>Step 5 — Partner Activation</b>\n\n"
            "Focus on:\n\n"
            "• Partner scoring checklist.\n"
            "• Activation playbook (steps from first call to signed contract).\n"
            "• Day 1 onboarding tasks for partner and drivers."
        ),
        parent_id="start_launch",
        next_id="start_launch_step_6",
        children=[],
    )
)

add_node(
    MenuNode(
        id="start_launch_step_6",
        title="Step 6 — Reporting & KPI",
        text=(
            "<b>Step 6 — Reporting & KPI</b>\n\n"
            "Track:\n\n"
            "• Main KPIs (CPL, conversion rates, cost per activated car).\n"
            "• Country benchmarks (Zambia, Angola, Cameroon, Ethiopia).\n"
            "• Weekly performance vs target."
        ),
        parent_id="start_launch",
        next_id="start_launch_step_7",
        children=[],
    )
)

add_node(
    MenuNode(
        id="start_launch_step_7",
        title="Step 7 — Go Live Checklist",
        text=(
            "<b>Step 7 — Go Live Checklist</b>\n\n"
            "Before going live:\n\n"
            "• Final validation checklist done.\n"
            "• Launch communication plan confirmed.\n"
            "• Monitoring plan for first 14 days prepared."
        ),
        parent_id="start_launch",
        next_id=None,
        children=[],
    )
)


# 2. Templates & Materials --------------------------------------------------

add_node(
    MenuNode(
        id="templates",
        title="Templates & Materials",
        text=(
            "<b>Templates & Materials</b>\n\n"
            "Here you can find all core templates and links used across countries."
        ),
        parent_id="root",
        next_id=None,
        children=[
            ("Contracts (EN / FR / PT)", "templates_contracts"),
            ("Landing templates", "templates_landing"),
            ("WhatsApp templates", "templates_wa"),
            ("Marketing materials", "templates_marketing"),
            ("Offline materials", "templates_offline"),
            ("Financial model templates", "templates_finmodel"),
        ],
    )
)

add_node(
    MenuNode(
        id="templates_contracts",
        title="Contracts (EN / FR / PT)",
        text=(
            "<b>Contracts (EN / FR / PT)</b>\n\n"
            "Here go links to contract templates in English, French and Portuguese.\n"
            "You can attach actual links or files for each language here."
        ),
        parent_id="templates",
        next_id="templates_landing",
        children=[],
    )
)

add_node(
    MenuNode(
        id="templates_landing",
        title="Landing templates",
        text=(
            "<b>Landing templates</b>\n\n"
            "Here go links to landing content templates and example tickets for web team."
        ),
        parent_id="templates",
        next_id="templates_wa",
        children=[],
    )
)

add_node(
    MenuNode(
        id="templates_wa",
        title="WhatsApp templates",
        text=(
            "<b>WhatsApp templates</b>\n\n"
            "Here go greeting texts, follow-up messages and FAQ scripts for WA flows."
        ),
        parent_id="templates",
        next_id="templates_marketing",
        children=[],
    )
)

add_node(
    MenuNode(
        id="templates_marketing",
        title="Marketing materials",
        text=(
            "<b>Marketing materials</b>\n\n"
            "Here go performance banners, OOH creatives and digital assets used across countries."
        ),
        parent_id="templates",
        next_id="templates_offline",
        children=[],
    )
)

add_node(
    MenuNode(
        id="templates_offline",
        title="Offline materials",
        text=(
            "<b>Offline materials</b>\n\n"
            "Here go flyers, printed materials and branding assets for events and offices."
        ),
        parent_id="templates",
        next_id="templates_finmodel",
        children=[],
    )
)

add_node(
    MenuNode(
        id="templates_finmodel",
        title="Financial model templates",
        text=(
            "<b>Financial model templates</b>\n\n"
            "Here go unit economics models and ROI calculators for car-owner programs."
        ),
        parent_id="templates",
        next_id=None,
        children=[],
    )
)


# 3. Communication Flows ----------------------------------------------------

add_node(
    MenuNode(
        id="flows",
        title="Communication Flows",
        text=(
            "<b>Communication Flows</b>\n\n"
            "Choose a flow to see the high-level steps and links."
        ),
        parent_id="root",
        next_id=None,
        children=[
            ("Landing flow", "flows_landing"),
            ("WhatsApp flow (ZM example)", "flows_wa_zm"),
        ],
    )
)

add_node(
    MenuNode(
        id="flows_landing",
        title="Landing flow",
        text=(
            "<b>Landing flow</b>\n\n"
            "• Ad click → landing page.\n"
            "• Landing explains value, requirements, models, earnings, trust.\n"
            "• User fills form → lead captured in Google Sheet.\n"
            "• Web team and marketing align on tracking and attribution.\n\n"
            "Add links to specific landing examples and web tickets here."
        ),
        parent_id="flows",
        next_id="flows_wa_zm",
        children=[],
    )
)

add_node(
    MenuNode(
        id="flows_wa_zm",
        title="WhatsApp flow (ZM example)",
        text=(
            "<b>WhatsApp flow (ZM example)</b>\n\n"
            "• Ad click → WA chat opens.\n"
            "• Auto-greeting explains the program and next steps.\n"
            "• Agent asks qualification questions and routes to partner.\n"
            "• Follow-up messages for inactive leads.\n\n"
            "Add links to Zambia WA flows and scripts here."
        ),
        parent_id="flows",
        next_id=None,
        children=[],
    )
)


# 4. KPI & Reporting --------------------------------------------------------

add_node(
    MenuNode(
        id="kpi",
        title="KPI & Reporting",
        text=(
            "<b>KPI & Reporting</b>\n\n"
            "Use these blocks to align metrics and reporting cadence."
        ),
        parent_id="root",
        next_id=None,
        children=[
            ("KPI definitions (formulas)", "kpi_definitions"),
            ("Country benchmarks", "kpi_benchmarks"),
            ("KPI tracker (sheet)", "kpi_tracker"),
            ("Weekly report templates", "kpi_weekly_reports"),
        ],
    )
)

add_node(
    MenuNode(
        id="kpi_definitions",
        title="KPI definitions (formulas)",
        text=(
            "<b>KPI definitions (formulas)</b>\n\n"
            "Describe how CPL, CPA, conversion rates and retention are calculated."
        ),
        parent_id="kpi",
        next_id="kpi_benchmarks",
        children=[],
    )
)

add_node(
    MenuNode(
        id="kpi_benchmarks",
        title="Country benchmarks",
        text=(
            "<b>Country benchmarks</b>\n\n"
            "Add benchmark ranges for key KPIs based on Zambia, Angola, Cameroon, Ethiopia."
        ),
        parent_id="kpi",
        next_id="kpi_tracker",
        children=[],
    )
)

add_node(
    MenuNode(
        id="kpi_tracker",
        title="KPI tracker (sheet)",
        text=(
            "<b>KPI tracker (sheet)</b>\n\n"
            "Link to the main KPI tracker used by local teams and central team."
        ),
        parent_id="kpi",
        next_id="kpi_weekly_reports",
        children=[],
    )
)

add_node(
    MenuNode(
        id="kpi_weekly_reports",
        title="Weekly report templates",
        text=(
            "<b>Weekly report templates</b>\n\n"
            "Describe structure of weekly updates: inputs, outputs, and narrative."
        ),
        parent_id="kpi",
        next_id=None,
        children=[],
    )
)


# 5. FAQ --------------------------------------------------------------------

faq_text = (
    "<b>FAQ</b>\n\n"
    "<b>Q: Who is this bot for?</b>\n"
    "A: For local teams launching car owner acquisition streams.\n\n"
    "<b>Q: Which countries are covered?</b>\n"
    "A: Initially Zambia, Angola, Cameroon, Ethiopia — but structure is reusable.\n\n"
    "<b>Q: Do I need technical knowledge to use it?</b>\n"
    "A: No, the bot is designed as a guided checklist with links and templates.\n\n"
    "<b>Q: Where do I find contracts?</b>\n"
    "A: In Templates & Materials → Contracts (EN / FR / PT).\n\n"
    "<b>Q: How often should I update KPIs?</b>\n"
    "A: At least weekly, and more often during first 2–4 weeks after launch."
)

add_node(
    MenuNode(
        id="faq",
        title="FAQ",
        text=faq_text,
        parent_id="root",
        next_id=None,
        children=[],
    )
)


# 6. Contacts ---------------------------------------------------------------

contacts_text = (
    "<b>Contacts</b>\n\n"
    "For marketing questions:\n"
    "• @AnnaD1\n\n"
    "For operations questions:\n"
    "• @nikharpatel09"
)

add_node(
    MenuNode(
        id="contacts",
        title="Contacts",
        text=contacts_text,
        parent_id="root",
        next_id=None,
        children=[],
    )
)


# ---------- UI HELPERS ----------


def build_menu_keyboard(node: MenuNode) -> InlineKeyboardMarkup:
    """Build keyboard with section items (children) and nav row (Back/Home/Next)."""

    kb = InlineKeyboardBuilder()

    # Main section buttons (children)
    for text, child_id in node.children:
        kb.button(text=text, callback_data=f"menu:{child_id}")

    # If there are children, put them in rows of 1
    if node.children:
        kb.adjust(1)

    # Navigation row
    nav_kb = InlineKeyboardBuilder()

    if node.parent_id is not None:
        nav_kb.button(text="⬅ Back", callback_data=f"menu:{node.parent_id}")

    nav_kb.button(text="🏠 Home", callback_data="menu:root")

    if node.next_id is not None:
        nav_kb.button(text="➡ Next", callback_data=f"menu:{node.next_id}")

    if nav_kb.buttons:
        nav_kb.adjust(len(nav_kb.buttons))
        # Append nav buttons as last row(s)
        kb.buttons.extend(nav_kb.buttons)

    return kb.as_markup() if kb.buttons else nav_kb.as_markup()


async def show_node(message: Message, node_id: str) -> None:
    node = MENU[node_id]
    await message.answer(node.text, reply_markup=build_menu_keyboard(node))


async def edit_node(cb: CallbackQuery, node_id: str) -> None:
    node = MENU[node_id]
    await cb.message.edit_text(node.text, reply_markup=build_menu_keyboard(node))
    await cb.answer()


# ---------- HANDLERS ----------


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await show_node(message, "root")


@router.callback_query(F.data.startswith("menu:"))
async def on_menu_callback(cb: CallbackQuery) -> None:
    _, node_id = cb.data.split(":", 1)
    if node_id not in MENU:
        await cb.answer("Unknown section", show_alert=True)
        return
    await edit_node(cb, node_id)


# ---------- RUN ----------


async def main() -> None:
    print("Bot running with structured menu…")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

