import asyncio
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Union

from aiogram import Bot, Dispatcher, F, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import (
    CallbackQuery,
    FSInputFile,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from dotenv import load_dotenv


# ---------- CONFIG ----------

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise SystemExit("BOT_TOKEN not found in .env")

# Verify only one token is loaded
if BOT_TOKEN.count(":") != 1:
    raise SystemExit("Invalid BOT_TOKEN format in .env")

# Log token prefix for verification
TOKEN_PREFIX = BOT_TOKEN[:5]
print(f"BOT STARTED WITH TOKEN PREFIX: {TOKEN_PREFIX}")

bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
router = Router()
dp.include_router(router)

# Paths
RESOURCES_DIR = Path(__file__).parent / "resources"
CONTRACTS_DIR = RESOURCES_DIR / "contracts"

# Checklist state storage: {user_id: {item_id: bool}}
_checklist_state: Dict[int, Dict[str, bool]] = {}

# User locks for preventing race conditions in callbacks
_user_locks: Dict[int, asyncio.Lock] = {}
_lock_manager_lock = asyncio.Lock()

# Checklist structure
CHECKLIST_ITEMS = {
    "Market & model": [
        ("market_demand", "Market demand validated"),
        ("partner_model", "Partner model selected"),
        ("unit_economics", "Unit economics calculated"),
        ("target_regions", "Target regions defined"),
    ],
    "Ops & ownership": [
        ("ops_owner", "Ops owner assigned"),
        ("partner_contact", "Partner contact established"),
        ("call_center_ready", "Call center ready"),
        ("escalation_defined", "Escalation process defined"),
    ],
    "Contracts & legal": [
        ("contract_template", "Contract template ready"),
        ("partner_alignment", "Partner alignment confirmed"),
        ("legal_approval", "Legal approval obtained"),
        ("signing_process", "Signing process tested"),
    ],
    "Lead processing & tracking": [
        ("tracker_created", "Lead tracker created"),
        ("statuses_configured", "Statuses configured"),
        ("routing_tested", "Routing flow tested"),
        ("no_duplicates", "No duplicate handling verified"),
    ],
    "Acquisition & budgets": [
        ("channels_approved", "Channels approved"),
        ("landing_validated", "Landing page validated"),
        ("whatsapp_active", "WhatsApp flow active"),
        ("budgets_approved", "Budgets approved"),
        ("tracking_checked", "Tracking verified"),
    ],
    "Reporting & monitoring": [
        ("kpi_defined", "KPIs defined"),
        ("reporting_template", "Reporting template ready"),
        ("cadence_agreed", "Reporting cadence agreed"),
        ("first_report_set", "First report scheduled"),
    ],
    "Go-live decision": [
        ("all_checks_done", "All checks completed"),
        ("launch_date_confirmed", "Launch date confirmed"),
        ("ready_to_scale", "Ready to scale"),
    ],
}


# ---------- MENU DATA MODEL ----------

@dataclass
class Link:
    """Link to external resource"""
    title: str
    url: str


@dataclass
class FileRef:
    """Reference to local file"""
    title: str
    path: Path


@dataclass
class MenuNode:
    id: str
    title: str
    text: str
    parent_id: Optional[str] = None
    children: List[tuple] = field(default_factory=list)  # (button_text, child_node_id)
    links: List[Link] = field(default_factory=list)
    files: List[FileRef] = field(default_factory=list)


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
        # NOTE: Root menu children are NOT used - build_main_menu() defines static menu
        # This is kept for reference only, but build_main_menu() is the source of truth
        children=[
            ("How it works", "what_is_coa"),
            ("🚀 Start launch", "start_launch"),
            ("💬 Communication flows", "flows"),
            ("📁 Materials & templates", "materials"),
            ("📊 Reports & KPI", "reports"),
            ("❓ FAQ", "faq"),
            ("👥 Contacts", "contacts"),
        ],
    )
)


# 0. How it works ------------------------------------------------------------

what_is_coa_text = (
    "<b>✅ How it works</b>\n\n"
    "<b>Description:</b>\n"
    "Car Owner Acquisition is a program that helps grow supply "
    "by bringing additional cars into the Yango ecosystem "
    "through individual car owners.\n\n"
    "Car owners do not drive themselves.\n"
    "Instead, they rent out their vehicles and earn regular income, "
    "while Yango partners manage drivers and daily operations.\n\n"
    "<b>How it works in practice:</b>\n\n"
    "1. We attract car owners through marketing campaigns "
    "(performance, landing pages, WhatsApp, offline channels).\n\n"
    "2. Car owners leave a lead via a landing page or WhatsApp.\n\n"
    "3. Leads are processed and qualified by local teams "
    "or a call center.\n\n"
    "4. Car owners sign a contract with a Yango partner.\n\n"
    "5. The partner assigns a driver and manages the vehicle.\n\n"
    "6. The car goes online, completes trips and generates income.\n\n"
    "7. Car owners receive regular payouts.\n\n"
    "<b>Why this program is important:</b>\n\n"
    "• Increases total car supply in the market\n"
    "• Unlocks cars from owners who don't want to drive\n"
    "• Supports faster driver onboarding\n"
    "• Enables scalable and predictable market growth\n\n"
    "<b>How car owners are usually acquired:</b>\n\n"
    "• Performance marketing (Meta, Google, TikTok)\n"
    "• Landing pages (recommended)\n"
    "• WhatsApp (early-stage or temporary)\n"
    "• Offline channels (OOH, flyers, QR codes)\n"
    "• In-app placements (where available)\n\n"
    "<b>What to do next:</b>\n\n"
    "If you are launching this stream for the first time, "
    "start with Step 1 — Market & Model.\n\n"
    "If you already have experience, "
    "you can jump directly to the relevant steps."
)

add_node(
    MenuNode(
        id="what_is_coa",
        title="How it works",
        text=what_is_coa_text,
        parent_id="root",
    )
)


# 1. Start launch -------------------------------------------------------------

add_node(
    MenuNode(
        id="start_launch",
        title="Start launch",
        text=(
            "<b>🚀 Start launch</b>\n\n"
            "This section explains what the Car Owner Acquisition stream is and how to launch it step by step.\n\n"
            "The Car Owner Acquisition program allows car owners to earn income by renting their vehicles "
            "to Yango partners, without driving themselves.\n\n"
            "This bot guides you through all key steps required to launch the stream in a new market — "
            "from market validation and operational readiness to acquisition channels, lead processing "
            "and reporting.\n\n"
            "Use the steps below in order. Each step builds on the previous one and helps ensure "
            "a smooth and scalable launch."
        ),
        parent_id="root",
        children=[
            ("Step 1 — Market & Model", "start_step_1"),
            ("Step 2 — Ops readiness", "start_step_2"),
            ("Step 3 — Acquisition channels", "start_step_3"),
            ("Step 4 — Lead processing & reporting", "start_step_4"),
            ("Step 5 — Go live checklist", "start_step_7"),
        ],
    )
)

# Step 1
add_node(
    MenuNode(
        id="start_step_1",
        title="Step 1 — Market & Model",
        text=(
            "<b>Step 1 — Market & Model</b>\n\n"
            "This step helps evaluate whether the Car Owner Acquisition stream "
            "makes sense to launch in a specific market and which model should be used.\n\n"
            "The goal of this step is to answer three key questions:\n"
            "• Is there demand from car owners to rent out their vehicles?\n"
            "• Is the local market and regulation suitable for this model?\n"
            "• Which operational setup will work best in this country?\n\n"
            "This analysis must be completed before any operational or marketing launch."
        ),
        parent_id="start_launch",
        children=[
            ("Market demand & behavior", "start_step_1_market_demand"),
            ("Unit economics & financial model", "start_step_1_financial_model"),
            ("Partner landscape", "start_step_1_partner_landscape"),
            ("Go / No-Go decision", "start_step_1_launch_decision"),
        ],
    )
)

# Step 1.1 - Market demand & behavior
add_node(
    MenuNode(
        id="start_step_1_market_demand",
        title="Market demand & behavior",
        text=(
            "<b>Market demand & behavior</b>\n\n"
            "Before launch, it is critical to understand how common it is "
            "for car owners to rent out their vehicles in the local market.\n\n"
            "<b>Key questions to analyze:</b>\n"
            "• Is car rental / car leasing common among individuals?\n"
            "• Do people already rent cars to drivers or fleets?\n"
            "• Are there informal vehicle owners or small fleet owners?\n"
            "• Is there trust in third-party vehicle management?\n\n"
            "<b>Signals that support launch:</b>\n"
            "• Existing informal rental market\n"
            "• Presence of small fleets (5–20 cars)\n"
            "• Car owners looking for passive income\n"
            "• High driver demand with low car supply\n\n"
            "<b>Red flags:</b>\n"
            "• Strong cultural resistance to renting out cars\n"
            "• Legal or insurance restrictions\n"
            "• High risk of fraud or vehicle damage"
        ),
        parent_id="start_step_1",
    )
)

# Step 1.2 - Unit economics & financial model
add_node(
    MenuNode(
        id="start_step_1_financial_model",
        title="Unit economics & financial model",
        text=(
            "<b>Unit economics & financial model</b>\n\n"
            "A basic unit economics model must be prepared before launch.\n\n"
            "<b>The model helps answer:</b>\n"
            "• Can car owners earn attractive weekly income?\n"
            "• Can partners operate the model profitably?\n"
            "• Are commissions, fees and costs sustainable?\n\n"
            "<b>This model should include:</b>\n"
            "• Average trips per car per day\n"
            "• Revenue per trip\n"
            "• Driver costs and partner commission\n"
            "• Owner payout\n"
            "• Platform commission\n\n"
            "<b>Unit economics template:</b>\n"
            "https://docs.google.com/spreadsheets/d/13hyO6Z6D7KxN9CH9llOW9vNhtyAMmATjcp7qklyCdb0/edit?gid=1452383912#gid=1452383912\n\n"
            "⚠ <b>NOTE</b>\n"
            "This template shows a base example only.\n"
            "Final assumptions must be validated with:\n"
            "• Local operations\n"
            "• Partner\n"
            "• Finance team (if needed)"
        ),
        parent_id="start_step_1",
        links=[
            Link("Unit economics template",
                 "https://docs.google.com/spreadsheets/d/13hyO6Z6D7KxN9CH9llOW9vNhtyAMmATjcp7qklyCdb0/edit?gid=1452383912#gid=1452383912"),
        ],
    )
)

# Step 1.3 - Partner landscape
add_node(
    MenuNode(
        id="start_step_1_partner_landscape",
        title="Partner landscape",
        text=(
            "<b>Partner landscape</b>\n\n"
            "Car Owner Acquisition requires reliable local partners "
            "who can manage vehicles and drivers on the ground.\n\n"
            "<b>Before launch, assess:</b>\n"
            "• Existing fleet partners and their size\n"
            "• Operational maturity (driver management, payouts, reporting)\n"
            "• Willingness to manage third-party vehicles\n"
            "• Contractual readiness\n\n"
            "<b>Typical partner profiles:</b>\n"
            "• Fleet owners with 10+ vehicles\n"
            "• Vehicle management companies\n"
            "• Experienced driver partners scaling into fleets"
        ),
        parent_id="start_step_1",
    )
)

# Step 1.4 - Go / No-Go decision
add_node(
    MenuNode(
        id="start_step_1_launch_decision",
        title="Go / No-Go decision",
        text=(
            "<b>Go / No-Go decision</b>\n\n"
            "After completing market and financial analysis, "
            "the local and central teams should make a clear launch decision.\n\n"
            "<b>Launch is recommended if:</b>\n"
            "• There is proven owner demand\n"
            "• Unit economics are positive\n"
            "• At least one operational partner is ready\n\n"
            "If these conditions are not met, "
            "the launch should be postponed or limited to a pilot."
        ),
        parent_id="start_step_1",
    )
)

# Step 2
add_node(
    MenuNode(
        id="start_step_2",
        title="Step 2 — Ops readiness",
        text=(
            "<b>Step 2 — Ops readiness</b>\n\n"
            "This step ensures that all operational components are ready "
            "before starting any acquisition activity.\n\n"
            "Ops readiness is critical: launching marketing without operational "
            "setup leads to lost leads, poor partner experience and weak results.\n\n"
            "This step must be completed before launching landing pages, "
            "WhatsApp flows or offline acquisition."
        ),
        parent_id="start_launch",
        children=[
            ("Local ops & ownership", "start_step_2_ops_team_setup"),
            ("Scouts / call center readiness", "start_step_2_scouts_call_center"),
            ("Contracts & legal alignment", "start_step_2_contracts_legal"),
        ],
    )
)

# Step 2.1 - Local ops & ownership
add_node(
    MenuNode(
        id="start_step_2_ops_team_setup",
        title="Local ops & ownership",
        text=(
            "<b>Local ops & ownership</b>\n\n"
            "Clear ownership on the local side is mandatory.\n\n"
            "<b>Before launch, define:</b>\n"
            "• Who owns the Car Owner stream locally\n"
            "• Who manages partners\n"
            "• Who owns the lead tracker\n"
            "• Who is responsible for reporting and follow-ups\n\n"
            "There must be a single ops owner responsible "
            "for the end-to-end flow."
        ),
        parent_id="start_step_2",
    )
)

# Step 2.2 - Scouts / call center readiness
add_node(
    MenuNode(
        id="start_step_2_scouts_call_center",
        title="Scouts / call center readiness",
        text=(
            "<b>Scouts / call center readiness</b>\n\n"
            "Leads must be contacted quickly and consistently.\n\n"
            "<b>Before launch, ensure:</b>\n"
            "• Scouts or call center are assigned\n"
            "• They are trained on the program logic\n"
            "• Lead handling scripts are approved\n"
            "• SLA for first contact is defined\n\n"
            "<b>Recommended:</b>\n"
            "• First contact within 24 hours\n"
            "• Minimum 3 contact attempts per lead\n\n"
            "<b>Example lead handling script & qualification template:</b>\n"
            "https://docs.google.com/spreadsheets/d/1Zj2345sqJvAdQ_jZ-9-RHe86y-w83bPpl6VKMLzn5Zg/edit?resourcekey=&gid=887705287#gid=887705287"
        ),
        parent_id="start_step_2",
        links=[
            Link("Lead handling script & qualification template",
                 "https://docs.google.com/spreadsheets/d/1Zj2345sqJvAdQ_jZ-9-RHe86y-w83bPpl6VKMLzn5Zg/edit?resourcekey=&gid=887705287#gid=887705287"),
        ],
    )
)

# Step 2.3 - Contracts & legal alignment
add_node(
    MenuNode(
        id="start_step_2_contracts_legal",
        title="Contracts & legal alignment",
        text=(
            "<b>Contracts & legal alignment</b>\n\n"
            "Contractual setup must be ready before onboarding car owners.\n\n"
            "<b>Ensure that:</b>\n"
            "• A local contract template exists\n"
            "• Contract terms are aligned with partner model\n"
            "• Responsibilities and payouts are clearly defined\n\n"
            "<b>Example contracts from other markets:</b>\n"
            "• Zambia (EN)\n"
            "• Angola (PT)\n"
            "• Cameroon (FR)\n\n"
            "<b>Example legal approval ticket (for reference):</b>\n"
            "https://st.yandex-team.ru/YLEGAL-16069?from=bell#692ec1649f4c341e3b94483b\n\n"
            "⚠ <b>NOTE</b>\n"
            "These contracts are examples only.\n"
            "They cannot be reused directly and must always be:\n"
            "• adapted to local legislation\n"
            "• reviewed with the partner\n"
            "• validated by the legal department"
        ),
        parent_id="start_step_2",
        links=[
            Link("Example legal approval ticket",
                 "https://st.yandex-team.ru/YLEGAL-16069?from=bell#692ec1649f4c341e3b94483b"),
        ],
        files=[
            FileRef("Contract Eng (Zambia)", CONTRACTS_DIR / "Contract Eng (Zambia).docx"),
            FileRef("Contract Portu (Angola)", CONTRACTS_DIR / "Contract Portu (Angola).pdf"),
            FileRef("Contract FR (Cameroon)", CONTRACTS_DIR / "Contract FR (Cameroon).pdf"),
        ],
    )
)

# Step 2.4 - Lead tracker setup
add_node(
    MenuNode(
        id="start_step_2_lead_tracker_setup",
        title="Lead tracker setup",
        text=(
            "<b>Lead tracker setup</b>\n\n"
            "The lead tracker is the single source of truth for all incoming leads.\n\n"
            "Each market must use a unified tracker structure to ensure comparable reporting "
            "and correct performance analysis.\n\n"
            "<b>Minimum required fields:</b>\n"
            "• Lead ID\n"
            "• Source\n"
            "• Date created\n"
            "• Contact status\n"
            "• Qualification status\n"
            "• Partner assigned\n"
            "• Contract status\n"
            "• Converted car (Yes / No)\n\n"
            "<b>Example tracker template:</b>\n"
            "https://docs.google.com/spreadsheets/d/13hyO6Z6D7KxN9CH9llOW9vNhtyAMmATjcp7qklyCdb0/edit?gid=1452383912#gid=1452383912\n\n"
            "⚠ <b>NOTE</b>\n"
            "Tracker structure can be adapted locally, but core fields must not be removed."
        ),
        parent_id="start_step_4",
        links=[
            Link("Example tracker template",
                 "https://docs.google.com/spreadsheets/d/13hyO6Z6D7KxN9CH9llOW9vNhtyAMmATjcp7qklyCdb0/edit?gid=1452383912#gid=1452383912"),
        ],
    )
)

# Step 2.5 - Go-live readiness check
add_node(
    MenuNode(
        id="start_step_2_ops_go_live_check",
        title="Go-live readiness check",
        text=(
            "<b>Go-live readiness check</b>\n\n"
            "Before starting acquisition, confirm that:\n"
            "• Ops owner is assigned\n"
            "• Partner is trained and ready\n"
            "• Contracts are approved\n"
            "• Lead tracker is live\n"
            "• Scouts / call center are active\n\n"
            "Only after this confirmation the market "
            "is ready to move to acquisition channels."
        ),
        parent_id="start_step_7",
    )
)

# Step 3
add_node(
    MenuNode(
        id="start_step_3",
        title="Step 3 — Acquisition channels",
        text=(
            "<b>Step 3 — Acquisition channels</b>\n\n"
            "The Car Owner acquisition stream uses two main channels:\n"
            "1) Landing page acquisition\n"
            "2) WhatsApp acquisition\n\n"
            "Both channels must follow a unified, consistent structure across all markets to ensure "
            "high lead quality, proper routing, and predictable conversion rates.\n\n"
            "────────────────────────────────────────────────────────────────\n"
            "<b>LANDING CHANNEL</b>\n"
            "────────────────────────────────────────────────────────────────\n\n"
            "Landing pages are one of the main acquisition channels in the Car Owner program. "
            "They must follow a unified structure across all markets to ensure consistent "
            "lead quality and correct data collection.\n\n"
            "<b>Landing templates include:</b>\n"
            "• Required sections and visual structure\n"
            "• Mandatory fields for data collection\n"
            "• Partner information blocks\n"
            "• Clear routing for incoming leads (landing → tracker → partner / call center)\n\n"
            "<b>The landing creation process always includes:</b>\n"
            "1. Filling the Landing Data Sheet\n"
            "2. Sharing brand assets (logos, visuals, colors)\n"
            "3. Providing all local text (titles, descriptions, benefits)\n"
            "4. Adding partner details if applicable\n"
            "5. Submitting a development request (ticket) to the web team — "
            "<a href=\"https://st.yandex-team.ru/YANGOWEB-484\">YANGOWEB-484</a>\n\n"
            "<b>Landing Data Sheet</b> (must be filled before development):\n"
            "https://docs.google.com/spreadsheets/d/10AaTXOAnVByDSS3FKISnkxXkqutKzbq1qkXrspyQKj0/edit?gid=288663658#gid=288663658\n\n"
            "<b>Examples of working landings:</b>\n"
            "• Zambia — https://yango.com/en_zm/carinvest/\n"
            "• Angola — https://yango.com/en_ao/carinvest/\n"
            "• Cameroon — https://yango.com/en_cm/carinvest/\n"
            "• Ethiopia — https://yango.com/en_et/carinvest/\n\n"
            "⚠ <b>NOTE</b>\n"
            "Landing content must always be validated by:\n"
            "• Local operations\n"
            "• Marketing team\n"
            "• Legal department\n"
            "especially if the landing contains any revenue claims or commitments.\n\n"
            "────────────────────────────────────────────────────────────────\n"
            "<b>WHATSAPP CHANNEL</b>\n"
            "────────────────────────────────────────────────────────────────\n\n"
            "WhatsApp is the second major acquisition channel used in markets where:\n"
            "• Landing conversion is low,\n"
            "• Internet penetration is unstable,\n"
            "• People prefer conversational onboarding.\n\n"
            "<b>WhatsApp leads typically have:</b>\n"
            "• Higher intent,\n"
            "• Better response rates,\n"
            "• Faster qualification.\n\n"
            "<b>WhatsApp flow includes:</b>\n"
            "• Auto-greeting message\n"
            "• Initial qualification questions\n"
            "• Manual follow-up by operations or a partner\n"
            "• Routing of qualified leads to a partner or a call-center agent\n\n"
            "<b>Example WhatsApp greeting message:</b>\n"
            "\"Hi! 👋 Thanks for your interest in earning with Yango.\n"
            "If you have a car, you can rent it to a Yango partner and receive weekly income — "
            "without driving yourself.\n"
            "Please send us:\n"
            "• Number of cars\n"
            "• Make/model\n"
            "• Year of manufacture\n"
            "• Mileage\n"
            "You can also read more here: https://yango.com/en_zm/carinvest/\"\n\n"
            "<b>WhatsApp scripts & qualification sheets:</b>\n"
            "https://docs.google.com/spreadsheets/d/1Zj2345sqJvAdQ_jZ-9-RHe86y-w83bPpl6VKMLzn5Zg/edit?resourcekey=&gid=887705287#gid=887705287\n\n"
            "⚠ <b>NOTE</b>\n"
            "All WhatsApp scripts must also be validated with:\n"
            "• Local operations\n"
            "• Marketing\n"
            "• Legal (if scripts mention revenue or promises)"
        ),
        parent_id="start_launch",
        links=[
            Link("Template for launch of landing",
                 "https://docs.google.com/spreadsheets/d/10AaTXOAnVByDSS3FKISnkxXkqutKzbq1qkXrspyQKj0/edit?gid=288663658#gid=288663658"),
            Link("🇿🇲 Zambia landing", "https://yango.com/en_zm/carinvest/"),
            Link("🇦🇴 Angola landing", "https://yango.com/en_ao/carinvest/"),
            Link("🇨🇲 Cameroon landing", "https://yango.com/en_cm/carinvest/"),
            Link("🇪🇹 Ethiopia landing", "https://yango.com/en_et/carinvest/"),
            Link("WhatsApp scripts & qualification sheets",
                 "https://docs.google.com/spreadsheets/d/1Zj2345sqJvAdQ_jZ-9-RHe86y-w83bPpl6VKMLzn5Zg/edit?resourcekey=&gid=887705287#gid=887705287"),
        ],
    )
)

# Step 4
add_node(
    MenuNode(
        id="start_step_4",
        title="Step 4 — Lead processing & reporting",
        text=(
            "<b>Step 4 — Lead processing & reporting</b>\n\n"
            "This step defines how incoming leads are collected, processed, tracked and reported.\n\n"
            "Correct lead processing is critical to avoid lead loss, delays and data inconsistency "
            "between marketing, operations and partners.\n\n"
            "This step must be completed before scaling acquisition channels or launching performance campaigns."
        ),
        parent_id="start_launch",
        children=[
            ("Lead intake & routing", "start_step_4_lead_intake_routing"),
            ("Lead tracker setup", "start_step_2_lead_tracker_setup"),
            ("Weekly reporting & KPI", "start_step_4_weekly_reporting_kpi"),
        ],
    )
)

# Step 4.1 - Lead intake & routing
add_node(
    MenuNode(
        id="start_step_4_lead_intake_routing",
        title="Lead intake & routing",
        text=(
            "<b>Lead intake & routing</b>\n\n"
            "All incoming leads must follow a clear and unified routing flow to ensure fast processing "
            "and correct ownership.\n\n"
            "<b>Typical lead sources:</b>\n"
            "• Landing pages\n"
            "• WhatsApp flows\n"
            "• Performance campaigns\n"
            "• Offline acquisition (OOH, scouts)\n\n"
            "<b>Standard routing flow:</b>\n"
            "Landing / Channel → Lead tracker → Call center / Partner → Contract signing\n\n"
            "<b>Ensure that:</b>\n"
            "• Each lead source is clearly labeled\n"
            "• Responsibility for first contact is defined\n"
            "• SLA for first contact is agreed with the partner"
        ),
        parent_id="start_step_4",
    )
)

# Step 4.3 - Weekly reporting & KPI
add_node(
    MenuNode(
        id="start_step_4_weekly_reporting_kpi",
        title="Weekly reporting & KPI",
        text=(
            "<b>Weekly reporting & KPI</b>\n\n"
            "Local teams are required to share weekly lead performance reports "
            "to track funnel health and partner efficiency.\n\n"
            "<b>Typical weekly report format:</b>\n\n"
            "Total leads: XXX\n"
            "Leads contacted (called): XXX\n"
            "Leads with no response: XXX\n"
            "Hot leads (interested in the program): XXX\n"
            "Leads forwarded to partner: XXX\n"
            "Leads in contract signing process: XXX\n"
            "Leads with signed contracts: XXX\n"
            "Converted cars: XXX\n\n"
            "Reports are usually shared once per week via Telegram using data from the lead tracker.\n\n"
            "<b>Ensure that:</b>\n"
            "• Reporting cadence is agreed\n"
            "• One owner is responsible for sending reports\n"
            "• Numbers are aligned with the tracker"
        ),
        parent_id="start_step_4",
    )
)

# Step 5
add_node(
    MenuNode(
        id="start_step_5",
        title="Step 5 — Partner activation",
        text=(
            "<b>Step 5 — Partner activation</b>\n\n"
            "<b>Main KPIs to track:</b>\n"
            "• CPL (Cost Per Lead)\n"
            "• CPA (Cost Per Activation)\n"
            "• Conversion rate (Leads → Contracts)\n"
            "• Retention (2/4/8 weeks)\n\n"
            "<b>Country benchmarks:</b>\n"
            "Target ranges based on Zambia, Angola, Cameroon, Ethiopia:\n"
            "• CPL: $5–15\n"
            "• CPA: $50–150\n"
            "• Conversion rate: 15–30%\n"
            "• Retention (4 weeks): 60–80%"
        ),
        parent_id="start_launch",
    )
)

# Step 6
add_node(
    MenuNode(
        id="start_step_6",
        title="Step 6 — Reporting & KPI",
        text=(
            "<b>Step 6 — Reporting & KPI</b>\n\n"
            "<b>KPI tracker:</b>\n"
            "Use the tracker below to monitor weekly performance.\n\n"
            "<b>Weekly report template:</b>\n"
            "Structure: inputs (leads, contracts, active cars, ad spend) → outputs (CPL, CPA, conversion, retention, narrative).\n\n"
            "<b>KPI definitions & formulas:</b>\n"
            "• CPL = Total ad spend / Number of leads\n"
            "• CPA = Total ad spend / Number of activated cars\n"
            "• Conversion rate = (Activated cars / Leads) × 100%\n"
            "• Retention = % of cars still active after N weeks"
        ),
        parent_id="start_launch",
        links=[
            Link("KPI tracker (Sheet)",
                 "https://docs.google.com/spreadsheets/d/1Zj2345sqJvAdQ_jZ-9-RHe86y-w83bPpl6VKMLzn5Zg/edit?resourcekey=&gid=2116500930#gid=2116500930"),
            Link("Lead tracker (Sheet)",
                 "https://docs.google.com/spreadsheets/d/1WhA1pt725L9uGHG6pDDRx5iFxSz2xPRuGJJGIPsAoAA/edit"),
        ],
    )
)

# Step 7
add_node(
    MenuNode(
        id="start_step_7",
        title="Step 5 — Go live checklist",
        text=(
            "<b>Step 5 — Go-live checklist</b>\n\n"
            "Mark each item as completed before go-live."
        ),
        parent_id="start_launch",
        children=[],  # Checklist items are handled dynamically
    )
)


# 2. Materials & templates ----------------------------------------------------

add_node(
    MenuNode(
        id="materials",
        title="Materials & templates",
        text=(
            "<b>📁 Materials & templates</b>\n\n"
            "Here you can find all core templates and materials used across countries."
        ),
        parent_id="root",
        children=[
            ("Contracts", "materials_contracts"),
            ("Landing templates", "materials_landing"),
            ("Marketing materials", "materials_marketing"),
            ("Financial model templates", "materials_finmodel"),
        ],
    )
)

# Contracts
add_node(
    MenuNode(
        id="materials_contracts",
        title="Contracts",
        text=(
            "<b>Contracts</b>\n\n"
            "Below are official Yango Car Owner contract templates from different countries "
            "(Zambia, Cameroon, Angola). These files are provided as <i>examples</i> to support "
            "the preparation process.\n\n"
            "⚠ <b>IMPORTANT</b>\n"
            "These contracts CANNOT be used as-is.\n"
            "Before applying any contract in your market, you MUST:\n"
            "• Review and align the contract with your partner\n"
            "• Verify all clauses and local requirements\n"
            "• Get official approval from the Legal department\n\n"
            "These templates are only for reference to help you understand typical contract "
            "structure and required elements."
        ),
        parent_id="materials",
        files=[
            FileRef("Contract Eng (Zambia)", CONTRACTS_DIR / "Contract Eng (Zambia).docx"),
            FileRef("Contract Portu (Angola)", CONTRACTS_DIR / "Contract Portu (Angola).pdf"),
            FileRef("Contract FR (Cameroon)", CONTRACTS_DIR / "Contract FR (Cameroon).pdf"),
        ],
    )
)

# Landing templates
add_node(
    MenuNode(
        id="materials_landing",
        title="Landing templates",
        text=(
            "<b>Landing templates</b>\n\n"
            "Standard templates for creating car owner acquisition landing pages. "
            "These templates define required sections, data fields, and visual structure.\n\n"
            "<b>Template for launch of landing:</b>\n"
            "https://docs.google.com/spreadsheets/d/10AaTXOAnVByDSS3FKISnkxXkqutKzbq1qkXrspyQKj0/edit?gid=288663658#gid=288663658\n\n"
            "<b>Examples of existing landings:</b>\n"
            "• Zambia — https://yango.com/en_zm/carinvest/\n"
            "• Angola — https://yango.com/en_ao/carinvest/\n"
            "• Cameroon — https://yango.com/en_cm/carinvest/\n"
            "• Ethiopia — https://yango.com/en_et/carinvest/\n\n"
            "⚠ <b>NOTE</b>\n"
            "Landing content must always be validated by:\n"
            "• Local operations\n"
            "• Marketing team\n"
            "• Legal department (especially if text includes commitments or revenue claims)"
        ),
        parent_id="materials",
        links=[
            Link("Template for launch of landing",
                 "https://docs.google.com/spreadsheets/d/10AaTXOAnVByDSS3FKISnkxXkqutKzbq1qkXrspyQKj0/edit?gid=288663658#gid=288663658"),
            Link("🇿🇲 Zambia landing", "https://yango.com/en_zm/carinvest/"),
            Link("🇦🇴 Angola landing", "https://yango.com/en_ao/carinvest/"),
            Link("🇨🇲 Cameroon landing", "https://yango.com/en_cm/carinvest/"),
            Link("🇪🇹 Ethiopia landing", "https://yango.com/en_et/carinvest/"),
        ],
    )
)

# Marketing materials
add_node(
    MenuNode(
        id="materials_marketing",
        title="Marketing materials",
        text=(
            "<b>Marketing materials</b>\n\n"
            "This section contains all marketing creatives and resources used for promoting "
            "the Car Owner Acquisition program across different markets. These include "
            "performance banners, WhatsApp visuals, social media creatives, OOH formats, "
            "flyers, printed materials, and in-app screens.\n\n"
            "Select a category to view creatives:\n\n"
            "⚠ <b>NOTE</b>\n"
            "All creatives must be validated by the central marketing team before use to ensure:\n"
            "• correct branding\n"
            "• consistency of communication\n"
            "• compliance with local regulations"
        ),
        parent_id="materials",
        children=[
            ("📊 Performance creatives", "materials_marketing_perf"),
            ("🪧 OOH materials", "materials_marketing_ooh"),
            ("📄 Flyers & Printed materials", "materials_marketing_offline"),
            ("📱 In-app creatives", "materials_marketing_inapp"),
        ],
    )
)

# Performance creatives
add_node(
    MenuNode(
        id="materials_marketing_perf",
        title="Performance creatives",
        text=(
            "<b>Performance creatives</b>\n\n"
            "Performance banners, WhatsApp visuals, and social media creatives for all countries.\n\n"
            "Select a country or general resources:"
        ),
        parent_id="materials_marketing",
        children=[
            ("🇦🇴 Angola", "materials_marketing_perf_ao"),
            ("🇧🇼 Botswana", "materials_marketing_perf_bw"),
            ("🇿🇲 Zambia", "materials_marketing_perf_zm"),
            ("🇨🇬 Congo", "materials_marketing_perf_cg"),
            ("📦 Performance sets (Dec 2024)", "materials_marketing_perf_sets"),
            ("📚 Performance text library", "materials_marketing_perf_texts"),
        ],
    )
)

# Angola performance
add_node(
    MenuNode(
        id="materials_marketing_perf_ao",
        title="Angola – Performance creatives",
        text=(
            "<b>Angola – Performance creatives</b>\n\n"
            "Performance banners and creatives for Angola market."
        ),
        parent_id="materials_marketing_perf",
        links=[
            Link("Angola – WA & performance",
                 "https://www.figma.com/design/GJ7bVwfVs0zjD84ZqmPohO/205-Perf-campaign_Luanda_Car-owners-acquisition"),
            Link("Angola – general performance",
                 "https://www.figma.com/design/ztTECUyoC4QdQIRcwgd0st/Yango-Angola"),
        ],
    )
)

# Botswana performance
add_node(
    MenuNode(
        id="materials_marketing_perf_bw",
        title="Botswana – Performance creatives",
        text=(
            "<b>Botswana – Performance creatives</b>\n\n"
            "Performance banners and creatives for Botswana market."
        ),
        parent_id="materials_marketing_perf",
        links=[
            Link("Botswana – performance",
                 "https://www.figma.com/design/Y4AVT4J5EefTNzA1H3eZqf/Zambia?node-id=0-1&p=f&t=PFNaU7utDqCdNHXJ-0"),
        ],
    )
)

# Zambia performance
add_node(
    MenuNode(
        id="materials_marketing_perf_zm",
        title="Zambia – Performance creatives",
        text=(
            "<b>Zambia – Performance creatives</b>\n\n"
            "Performance banners and creatives for Zambia market."
        ),
        parent_id="materials_marketing_perf",
        links=[
            Link("Zambia – performance (TikTok + Instagram)",
                 "https://www.figma.com/design/Y4AVT4J5EefTNzA1H3eZqf/Zambia?node-id=3-877&p=f&t=DboudQySYWVFZzdJ-0"),
            Link("Zambia – performance ad texts",
                 "https://docs.google.com/spreadsheets/d/1oNammWtGNdpsZRogPQsjP2uk3MfehGKsd3h_Q8KmxAA/edit?gid=0#gid=0"),
        ],
    )
)

# Congo performance
add_node(
    MenuNode(
        id="materials_marketing_perf_cg",
        title="Congo – Performance creatives",
        text=(
            "<b>Congo – Performance creatives</b>\n\n"
            "Performance banners and creatives for Congo market."
        ),
        parent_id="materials_marketing_perf",
        links=[
            Link("Congo – performance banners",
                 "https://www.figma.com/design/Jj20Evm6lhysGgTsO75IXE/Congo?node-id=59-162&p=f&t=LcsAK8SsQZPPNRPk-0"),
            Link("Congo – performance texts",
                 "https://docs.google.com/spreadsheets/d/10jj31Ka67QO3AxnlWV9PPdJYZy2M-7ov7PeC21cuMpU/edit?gid=1523786630#gid=1523786630"),
        ],
    )
)

# Performance sets Dec24
add_node(
    MenuNode(
        id="materials_marketing_perf_sets",
        title="Performance sets (Dec 2024)",
        text=(
            "<b>Performance sets (Dec 2024)</b>\n\n"
            "General performance banner sets for December 2024 campaign."
        ),
        parent_id="materials_marketing_perf",
        links=[
            Link("Performance sets Dec24 (1)",
                 "https://www.figma.com/design/OYOkya1idxk8BfNyLCDjRg/CLAB-49833---YTM-Perf-Banners-Dec24"),
            Link("Performance sets Dec24 (2)",
                 "https://www.figma.com/design/OYOkya1idxk8BfNyLCDjRg/CLAB-49833---Performance-Dec24?node-id=3-2994"),
        ],
    )
)

# Performance text library
add_node(
    MenuNode(
        id="materials_marketing_perf_texts",
        title="Performance text library",
        text=(
            "<b>Performance text library</b>\n\n"
            "General performance ad texts library for all countries."
        ),
        parent_id="materials_marketing_perf",
        links=[
            Link("Performance text library",
                 "https://docs.google.com/spreadsheets/d/1zNS5aUVxY5StLQ0J01TVHhpuqQjoy4YVARBBmFJ2Ra8/edit?gid=0#gid=0"),
        ],
    )
)

# OOH materials
add_node(
    MenuNode(
        id="materials_marketing_ooh",
        title="OOH materials",
        text=(
            "<b>OOH materials</b>\n\n"
            "Outdoor advertising materials: banners for malls, billboards, and outdoor displays."
        ),
        parent_id="materials_marketing",
        children=[
            ("🏬 Malls OOH", "materials_marketing_ooh_malls"),
            ("🇦🇴 Angola OOH", "materials_marketing_ooh_ao"),
            ("🇿🇲 Zambia OOH", "materials_marketing_ooh_zm"),
        ],
    )
)

# Malls OOH
add_node(
    MenuNode(
        id="materials_marketing_ooh_malls",
        title="Malls OOH",
        text=(
            "<b>Malls OOH</b>\n\n"
            "OOH materials for malls and shopping centers."
        ),
        parent_id="materials_marketing_ooh",
        links=[
            Link("Malls OOH",
                 "https://www.figma.com/design/ja4K9Xj44upbwwWvu9qWV9/YANGO-CARS_ADS-ON-MALLS"),
        ],
    )
)

# Angola OOH
add_node(
    MenuNode(
        id="materials_marketing_ooh_ao",
        title="Angola OOH",
        text=(
            "<b>Angola OOH</b>\n\n"
            "Outdoor advertising materials for Angola market."
        ),
        parent_id="materials_marketing_ooh",
        links=[
            Link("Angola OOH",
                 "https://www.figma.com/design/aENCAQUznQPAtuZL1bvO6H/Yango-Angola---OOH-car--moto-owners"),
        ],
    )
)

# Zambia OOH
add_node(
    MenuNode(
        id="materials_marketing_ooh_zm",
        title="Zambia OOH",
        text=(
            "<b>Zambia OOH</b>\n\n"
            "Outdoor advertising materials for Zambia market."
        ),
        parent_id="materials_marketing_ooh",
        links=[
            Link("Zambia OOH",
                 "https://www.figma.com/design/wSsZsG2se2Qe7dZRKJZMlv/YANGO-%E2%9C%95-QB-%E2%80%93-client_preview?node-id=7394-108&p=f"),
        ],
    )
)

# Flyers & Printed materials
add_node(
    MenuNode(
        id="materials_marketing_offline",
        title="Flyers & Printed materials",
        text=(
            "<b>Flyers & Printed materials</b>\n\n"
            "Flyers, printed materials, and branding assets for events and offices."
        ),
        parent_id="materials_marketing",
        links=[
            Link("Angola flyers (ANGOTIC)",
                 "https://www.figma.com/design/2Dg2jkvZKmDLxFTQYYPkHK/Yango-Angola---Flyers-for-ANGOTIC"),
            Link("Partner printed materials",
                 "https://www.figma.com/design/hkoZqep4E6021lMRNfQdPu/Yango-Angola---Partners-acquisition_Printed-materials"),
        ],
    )
)

# In-app creatives
add_node(
    MenuNode(
        id="materials_marketing_inapp",
        title="In-app creatives",
        text=(
            "<b>In-app creatives</b>\n\n"
            "Creative materials for in-app placements and notifications.\n\n"
            "Select a country:"
        ),
        parent_id="materials_marketing",
        children=[
            ("🇦🇴 Angola in-app", "materials_marketing_inapp_ao"),
            ("🇿🇲 Zambia in-app", "materials_marketing_inapp_zm"),
        ],
    )
)

# Angola in-app
add_node(
    MenuNode(
        id="materials_marketing_inapp_ao",
        title="Angola in-app",
        text=(
            "<b>Angola in-app creatives</b>\n\n"
            "In-app creative materials for Angola market."
        ),
        parent_id="materials_marketing_inapp",
        links=[
            Link("Angola in-app",
                 "https://www.figma.com/design/nGtewC8ICEim0Kxhro1UmA/Angola-2025-·-Yango"),
        ],
    )
)

# Zambia in-app
add_node(
    MenuNode(
        id="materials_marketing_inapp_zm",
        title="Zambia in-app",
        text=(
            "<b>Zambia in-app creatives</b>\n\n"
            "In-app creative materials for Zambia market."
        ),
        parent_id="materials_marketing_inapp",
        links=[
            Link("Zambia in-app",
                 "https://www.figma.com/design/1cpQG9Ty7VL9Jw9ymGK72N/Яндекс-Янго----BONOYT-4537----Yango-Zambia---Car-Owners-Zambia---inapp---Users"),
        ],
    )
)

# Financial model templates
add_node(
    MenuNode(
        id="materials_finmodel",
        title="Financial models",
        text=(
            "<b>Financial models</b>\n\n"
            "This section contains the base Unit Economics template used to estimate "
            "financial feasibility of the Car Owner Acquisition program in each country.\n\n"
            "<b>The template allows teams to calculate:</b>\n"
            "• Expected weekly revenue\n"
            "• Owner payout\n"
            "• Partner margin\n"
            "• Key operational costs (salary, fuel, maintenance, etc.)\n"
            "• Sensitivity based on utilisation levels\n\n"
            "<b>Financial model template (Unit Economics only):</b>\n"
            "https://docs.google.com/spreadsheets/d/13hyO6Z6D7KxN9CH9llOW9vNhtyAMmATjcp7qklyCdb0/edit?gid=1452383912#gid=1452383912\n\n"
            "⚠ <b>NOTE</b>\n"
            "This template currently includes ONLY unit economics.\n"
            "Additional calculation models (partner models, expanded cost structures, "
            "alternative projections) will be added later once provided.\n\n"
            "Before using the model for decision-making, please validate all assumptions with:\n"
            "• Local operations\n"
            "• Finance team\n"
            "• Legal (if numbers will be used in public/partner communication)"
        ),
        parent_id="materials",
        links=[
            Link("Financial model template (Unit Economics only)",
                 "https://docs.google.com/spreadsheets/d/13hyO6Z6D7KxN9CH9llOW9vNhtyAMmATjcp7qklyCdb0/edit?gid=1452383912#gid=1452383912"),
        ],
    )
)


# 3. Communication flows ------------------------------------------------------

add_node(
    MenuNode(
        id="flows",
        title="Communication flows",
        text=(
            "<b>✅ Communication flows</b>\n\n"
            "This section describes the two supported communication flows "
            "used in the Car Owner Acquisition stream.\n\n"
            "Each flow has different strengths and limitations.\n"
            "Local teams should choose the flow based on tracking needs, "
            "market maturity and operational readiness."
        ),
        parent_id="root",
        children=[
            ("Flow 1 — Landing page (recommended)", "flows_landing"),
            ("Flow 2 — WhatsApp", "flows_wa"),
            ("Flow selection guidance", "flows_selection"),
        ],
    )
)

# Flow 1 — Landing page
add_node(
    MenuNode(
        id="flows_landing",
        title="Landing page",
        text=(
            "<b>🔹 Flow 1 — Landing page</b>\n\n"
            "Landing pages are the primary and recommended communication flow "
            "for Car Owner Acquisition.\n\n"
            "They provide structured lead collection and full visibility "
            "across the acquisition funnel.\n\n"
            "<b>Key benefits:</b>\n"
            "• Structured lead form\n"
            "• Clear value proposition\n"
            "• Full analytics and attribution\n"
            "• Easy integration with lead trackers\n"
            "• Scalable for performance campaigns\n\n"
            "<b>Typical use cases:</b>\n"
            "• Performance marketing\n"
            "• In-app traffic\n"
            "• Offline QR codes\n\n"
            "<b>Limitations:</b>\n"
            "• Requires web team involvement\n"
            "• Setup time before launch\n\n"
            "<b>Examples of working landings:</b>\n"
            "• Zambia — https://yango.com/en_zm/carinvest/\n"
            "• Angola — https://yango.com/en_ao/carinvest/\n"
            "• Cameroon — https://yango.com/en_cm/carinvest/\n"
            "• Ethiopia — https://yango.com/en_et/carinvest/"
        ),
        parent_id="flows",
        links=[
            Link("🇿🇲 Zambia landing", "https://yango.com/en_zm/carinvest/"),
            Link("🇦🇴 Angola landing", "https://yango.com/en_ao/carinvest/"),
            Link("🇨🇲 Cameroon landing", "https://yango.com/en_cm/carinvest/"),
            Link("🇪🇹 Ethiopia landing", "https://yango.com/en_et/carinvest/"),
        ],
    )
)

# Flow 2 — WhatsApp
add_node(
    MenuNode(
        id="flows_wa",
        title="WhatsApp",
        text=(
            "<b>🔹 Flow 2 — WhatsApp</b>\n\n"
            "WhatsApp is used as a simple and fast entry point "
            "when landing pages are not available or as a temporary solution.\n\n"
            "<b>Key benefits:</b>\n"
            "• Low entry barrier for users\n"
            "• Fast setup\n"
            "• Familiar channel in many markets\n\n"
            "<b>Typical use cases:</b>\n"
            "• Early market testing\n"
            "• Offline acquisition\n"
            "• Small-scale pilots\n\n"
            "<b>Limitations:</b>\n"
            "• No built-in analytics for incoming leads\n"
            "• Traffic source attribution is not available\n"
            "• Manual lead consolidation is required\n"
            "• Limited scalability\n\n"
            "WhatsApp should be treated as a temporary or complementary flow, "
            "not a long-term replacement for landing pages."
        ),
        parent_id="flows",
    )
)

# Flow selection guidance
add_node(
    MenuNode(
        id="flows_selection",
        title="Flow selection guidance",
        text=(
            "<b>🔹 Flow selection guidance</b>\n\n"
            "<b>Recommended default setup:</b>\n"
            "Landing page.\n\n"
            "<b>WhatsApp can be used if:</b>\n"
            "• Landing page is not yet available\n"
            "• Market is in early testing phase\n"
            "• Volume is limited and manual processing is acceptable\n\n"
            "As the market scales, teams should migrate "
            "from WhatsApp to landing-based acquisition."
        ),
        parent_id="flows",
    )
)


# 4. Reports & KPI -----------------------------------------------------------

add_node(
    MenuNode(
        id="reports",
        title="Reports & KPI",
        text=(
            "<b>📊 Reports & KPI</b>\n\n"
            "Use these blocks to align metrics and reporting cadence."
        ),
        parent_id="root",
        children=[
            ("KPI definitions and formulas", "reports_definitions"),
            ("Country benchmarks", "reports_benchmarks"),
            ("KPI tracker", "reports_tracker"),
            ("Weekly reports", "reports_weekly"),
        ],
    )
)
# KPI definitions
add_node(
    MenuNode(
        id="reports_definitions",
        title="KPI definitions and formulas",
        text=(
            "<b>KPI definitions and formulas</b>\n\n"
            "<b>CPL (Cost Per Lead):</b>\n"
            "Total ad spend / Number of leads\n\n"
            "<b>CPA (Cost Per Activation):</b>\n"
            "Total ad spend / Number of activated cars\n\n"
            "<b>Conversion rate:</b>\n"
            "(Activated cars / Leads) × 100%\n\n"
            "<b>Retention (2/4/8 weeks):</b>\n"
            "% of cars still active after N weeks"
        ),
        parent_id="reports",
        links=[
            Link("KPI tracker (Sheet)",
                 "https://docs.google.com/spreadsheets/d/1Zj2345sqJvAdQ_jZ-9-RHe86y-w83bPpl6VKMLzn5Zg/edit?resourcekey=&gid=2116500930#gid=2116500930"),
        ],
    )
)

# Country benchmarks
add_node(
    MenuNode(
        id="reports_benchmarks",
        title="Country benchmarks",
        text=(
            "<b>Country benchmarks</b>\n\n"
            "Country benchmarks provide a reference view of Car Owner Acquisition "
            "performance across different markets.\n\n"
            "Benchmarks help answer:\n"
            "• whether a market is performing within a healthy range\n"
            "• how results compare to other countries\n"
            "• where deeper investigation or optimisation is needed\n\n"
            "Benchmarks are based on historical performance across markets "
            "and should be used as directional guidance, not strict targets.\n\n"
            "<b>Indicative benchmark ranges:</b>\n\n"
            "• <b>Cost per lead (CPL):</b>\n"
            "  ~$5 – $15\n\n"
            "• <b>Lead → contract conversion:</b>\n"
            "  ~5% – 15%\n\n"
            "• <b>Contract → car activation conversion:</b>\n"
            "  ~60% – 85%\n\n"
            "• <b>Time to first contact:</b>\n"
            "  < 24 hours (recommended)\n\n"
            "• <b>Cars activated per week (early stage markets):</b>\n"
            "  ~10 – 40 cars\n\n"
            "• <b>Cars activated per week (scaled markets):</b>\n"
            "  40+ cars\n\n"
            "These ranges may vary depending on:\n"
            "• market maturity\n"
            "• acquisition channel mix\n"
            "• partner setup\n"
            "• operational capacity\n\n"
            "<b>Country benchmark tracker:</b>\n"
            "https://docs.google.com/spreadsheets/d/1iUXvp8b2mjpwrAM3bOq1WbRCSLONJIIUIGS6Hs4ogJI/edit?gid=2140084982#gid=2140084982\n\n"
            "⚠ <b>NOTE</b>\n"
            "Benchmarks should always be interpreted in context.\n"
            "Markets at early launch stages may perform below benchmarks initially, "
            "while mature markets are expected to outperform them."
        ),
        parent_id="reports",
        links=[
            Link("Country benchmark tracker",
                 "https://docs.google.com/spreadsheets/d/1iUXvp8b2mjpwrAM3bOq1WbRCSLONJIIUIGS6Hs4ogJI/edit?gid=2140084982#gid=2140084982"),
        ],
    )
)

# KPI tracker
add_node(
    MenuNode(
        id="reports_tracker",
        title="KPI tracker",
        text=(
            "<b>KPI tracker</b>\n\n"
            "Main KPI tracker used by local teams and central team."
        ),
        parent_id="reports",
        links=[
            Link("KPI tracker (Sheet)",
                 "https://docs.google.com/spreadsheets/d/1Zj2345sqJvAdQ_jZ-9-RHe86y-w83bPpl6VKMLzn5Zg/edit?resourcekey=&gid=2116500930#gid=2116500930"),
            Link("Lead tracker (Sheet)",
                 "https://docs.google.com/spreadsheets/d/1WhA1pt725L9uGHG6pDDRx5iFxSz2xPRuGJJGIPsAoAA/edit"),
        ],
    )
)

# Weekly reports
add_node(
    MenuNode(
        id="reports_weekly",
        title="Weekly reports",
        text=(
            "<b>Weekly reports</b>\n\n"
            "Weekly reports are used to monitor lead quality, funnel health "
            "and operational performance on a regular basis.\n\n"
            "Local teams are expected to share a short weekly summary "
            "based on data from the lead tracker.\n\n"
            "<b>The goal of weekly reporting is to:</b>\n"
            "• quickly identify bottlenecks in the funnel\n"
            "• track lead quality and conversion dynamics\n"
            "• ensure alignment between marketing, ops and partners\n"
            "• enable fast corrective actions if needed\n\n"
            "<b>Typical weekly report metrics:</b>\n"
            "• Total leads\n"
            "• Leads contacted (called)\n"
            "• Leads with no response\n"
            "• Hot leads (interested in the program)\n"
            "• Leads forwarded to partner\n"
            "• Leads in contract signing process\n"
            "• Leads with signed contracts\n"
            "• Converted cars\n\n"
            "<b>Example weekly report format (Telegram):</b>\n\n"
            "📊 <b>Weekly Car Owner Report — Zambia</b>\n"
            "🗓 Period: Nov 1–7\n\n"
            "• Total leads: 320\n"
            "• Leads contacted: 250\n"
            "• No response: 70\n"
            "• Hot leads: 110\n"
            "• Leads forwarded to partner: 80\n"
            "• In contract signing: 45\n"
            "• Signed contracts: 32\n"
            "• Converted cars: 28\n\n"
            "Reports are usually shared once per week "
            "via Telegram / Slack / Email, depending on local setup.\n\n"
            "<b>Example weekly report template:</b>\n"
            "https://docs.google.com/spreadsheets/d/1Zj2345sqJvAdQ_jZ-9-RHe86y-w83bPpl6VKMLzn5Zg/edit?resourcekey=&gid=2116500930#gid=2116500930\n\n"
            "⚠ <b>NOTE</b>\n"
            "Weekly reports must be aligned with the lead tracker.\n"
            "Manual adjustments or estimates should be avoided."
        ),
        parent_id="reports",
        links=[
            Link("Example weekly report template",
                 "https://docs.google.com/spreadsheets/d/1Zj2345sqJvAdQ_jZ-9-RHe86y-w83bPpl6VKMLzn5Zg/edit?resourcekey=&gid=2116500930#gid=2116500930"),
        ],
    )
)


# 5. FAQ ---------------------------------------------------------------------

faq_text = (
    "<b>✅ FAQ</b>\n\n"
    "This section answers the most common questions "
    "about launching and operating the Car Owner Acquisition stream.\n\n"
    "If your question is not covered here, "
    "please contact the project leads.\n\n"
    "<b>❓ What is the Car Owner Acquisition program?</b>\n"
    "The Car Owner Acquisition program allows car owners "
    "to rent out their vehicles to Yango partners "
    "and earn regular income without driving themselves.\n\n"
    "Local partners manage drivers and operations, "
    "while Yango supports demand, platform access and tooling.\n\n"
    "<b>❓ When should a market launch this stream?</b>\n"
    "The stream should be launched only after:\n"
    "• Market demand is validated\n"
    "• Unit economics are positive\n"
    "• Operational readiness is confirmed\n"
    "• A partner is ready to manage vehicles\n\n"
    "Launching too early may lead to poor lead quality "
    "and low conversion.\n\n"
    "<b>❓ What is the recommended acquisition flow?</b>\n"
    "The recommended default setup is:\n"
    "Landing page → Lead tracker → Call center / scouts → Partner\n\n"
    "WhatsApp can be used as a temporary or early-stage solution, "
    "but it is not recommended for scaling.\n\n"
    "<b>❓ Why is WhatsApp not recommended as a long-term solution?</b>\n"
    "WhatsApp has important limitations:\n"
    "• No built-in analytics for incoming leads\n"
    "• No traffic source attribution\n"
    "• Manual lead consolidation\n"
    "• Limited scalability\n\n"
    "As volumes grow, landing-based acquisition "
    "provides much better control and visibility.\n\n"
    "<b>❓ Who owns lead processing and reporting?</b>\n"
    "Lead processing is usually owned by local operations "
    "or an assigned call center.\n\n"
    "Reporting must be based on the lead tracker "
    "and shared on a weekly basis with the central team.\n\n"
    "<b>❓ Can we reuse contracts from other countries?</b>\n"
    "No.\n\n"
    "Contracts from other markets are provided "
    "for reference only.\n\n"
    "Each contract must be:\n"
    "• adapted to local legislation\n"
    "• aligned with the partner\n"
    "• approved by the legal department\n\n"
    "<b>❓ How do we know if a market is performing well?</b>\n"
    "Performance should be evaluated using:\n"
    "• Weekly reports\n"
    "• Country benchmarks\n"
    "• Conversion rates across the funnel\n\n"
    "Benchmarks provide directional guidance, "
    "not strict targets.\n\n"
    "<b>❓ Who should we contact if we have questions?</b>\n"
    "For marketing and launch-related questions:\n"
    "@AnnaD1 — Marketing lead\n\n"
    "For operational questions:\n"
    "@nikharpatel09 — Ops lead"
)

add_node(
    MenuNode(
        id="faq",
        title="FAQ",
        text=faq_text,
        parent_id="root",
    )
)


# 6. Contacts ----------------------------------------------------------------

contacts_text = (
    "<b>👥 Contacts</b>\n\n"
    "<b>Marketing lead:</b>\n"
    "@AnnaD1\n\n"
    "<b>Ops lead:</b>\n"
    "@nikharpatel09"
)

add_node(
    MenuNode(
        id="contacts",
        title="Contacts",
        text=contacts_text,
        parent_id="root",
    )
)


# ---------- UI HELPERS ----------


def get_checklist_state(user_id: int) -> Dict[str, bool]:
    """Get checklist state for a user, initializing if needed."""
    if user_id not in _checklist_state:
        _checklist_state[user_id] = {}
    return _checklist_state[user_id]


def toggle_checklist_item(user_id: int, item_id: str) -> bool:
    """Toggle a checklist item and return new state."""
    state = get_checklist_state(user_id)
    current = state.get(item_id, False)
    state[item_id] = not current
    return state[item_id]


def get_checklist_progress(user_id: int) -> tuple[int, int]:
    """Get checklist progress: (completed, total)."""
    state = get_checklist_state(user_id)
    total = sum(len(items) for items in CHECKLIST_ITEMS.values())
    completed = sum(1 for items in CHECKLIST_ITEMS.values() for item_id, _ in items if state.get(item_id, False))
    return completed, total


def build_checklist_keyboard(user_id: int, node: MenuNode) -> InlineKeyboardMarkup:
    """Build keyboard for checklist node (Step 7)."""
    state = get_checklist_state(user_id)
    rows: List[List[InlineKeyboardButton]] = []
    
    # Add checklist items grouped by category
    for category, items in CHECKLIST_ITEMS.items():
        for item_id, item_text in items:
            checked = state.get(item_id, False)
            icon = "✅" if checked else "⬜"
            rows.append([InlineKeyboardButton(
                text=f"{icon} {item_text}",
                callback_data=f"toggle:{item_id}"
            )])
    
    # Navigation row
    footer_buttons: List[InlineKeyboardButton] = []
    parent_node_id = node.parent_id if node.parent_id and node.parent_id in MENU else "root"
    footer_buttons.append(InlineKeyboardButton(
        text="⬅ Back",
        callback_data=f"menu:{parent_node_id}"
    ))
    footer_buttons.append(InlineKeyboardButton(
        text="🏠 Home",
        callback_data=f"menu:root"
    ))
    rows.append(footer_buttons)
    
    return InlineKeyboardMarkup(inline_keyboard=rows)


def parse_callback(data: str) -> Optional[str]:
    """
    Parse callback data and return node_id.
    Supports formats:
    - menu:<node_id> (current format)
    - v3:<node_id> (legacy format, for compatibility)
    - v4:<node_id> (legacy format, for compatibility)
    
    Returns node_id if valid, None otherwise.
    """
    if not data:
        return None
    
    # Try to parse as menu:<node_id>
    if data.startswith("menu:"):
        try:
            _, node_id = data.split(":", 1)
            return node_id.strip()
        except ValueError:
            return None
    
    # Try to parse as v3:<node_id> or v4:<node_id> (legacy support)
    if data.startswith("v3:") or data.startswith("v4:"):
        try:
            _, node_id = data.split(":", 1)
            node_id = node_id.strip()
            # Map legacy formats to current format
            print(f"DEBUG: Legacy callback format detected: '{data}' -> node_id='{node_id}'")
            return node_id
        except ValueError:
            return None
    
    return None


def build_main_menu() -> InlineKeyboardMarkup:
    """
    Build STATIC main menu keyboard.
    This function ALWAYS returns the same buttons in the same order.
    Main menu must NEVER change dynamically.
    """
    print("DEBUG: build_main_menu() called - building STATIC main menu")
    rows: List[List[InlineKeyboardButton]] = []
    
    # STATIC main menu buttons - ALWAYS in this exact order
    main_menu_buttons = [
        ("How it works", "what_is_coa"),
        ("🚀 Start launch", "start_launch"),
        ("💬 Communication flows", "flows"),
        ("📁 Materials & templates", "materials"),
        ("📊 Reports & KPI", "reports"),
        ("❓ FAQ", "faq"),
        ("👥 Contacts", "contacts"),
    ]
    
    print(f"DEBUG: Main menu buttons: {main_menu_buttons}")
    
    # Add main menu buttons
    for text, child_id in main_menu_buttons:
        rows.append([InlineKeyboardButton(
            text=text,
            callback_data=f"menu:{child_id}"
        )])
    
    # Navigation row - Back and Home
    # In root menu, both Back and Home go to root (since root has no parent)
    footer_buttons: List[InlineKeyboardButton] = [
        InlineKeyboardButton(text="⬅ Back", callback_data="menu:root"),
        InlineKeyboardButton(text="🏠 Home", callback_data="menu:root")
    ]
    rows.append(footer_buttons)
    
    return InlineKeyboardMarkup(inline_keyboard=rows)


def build_menu_keyboard(node: MenuNode, user_id: Optional[int] = None) -> InlineKeyboardMarkup:
    """Build keyboard with section items, links, files, and nav buttons (Back/Home)."""
    
    # CRITICAL: Root node ALWAYS uses static main menu
    if node.id == "root":
        print("DEBUG: Root node detected, using build_main_menu()")
        return build_main_menu()
    
    # Special handling for checklist node
    if node.id == "start_step_7" and user_id is not None:
        return build_checklist_keyboard(user_id, node)
    
    # Use lists, not generators, to avoid TypeError
    rows: List[List[InlineKeyboardButton]] = []
    
    # Main section buttons (children) - format: menu:<node_id>
    for text, child_id in node.children:
        rows.append([InlineKeyboardButton(
            text=text, 
            callback_data=f"menu:{child_id}"
        )])
    
    # Links as buttons
    for link in node.links:
        rows.append([InlineKeyboardButton(text=f"🔗 {link.title}", url=link.url)])
    
    # Files as buttons (will be handled separately via callback)
    for file_ref in node.files:
        rows.append([InlineKeyboardButton(
            text=f"📎 {file_ref.title}",
            callback_data=f"file:{node.id}:{file_ref.title}"
        )])
    
    # Navigation row - ALWAYS Back and Home
    footer_buttons: List[InlineKeyboardButton] = []
    
    # Determine parent node for Back button
    # Back always goes to parent_id, or root if no parent
    parent_node_id = node.parent_id if node.parent_id is not None else "root"
    
    # Verify parent exists in MENU
    if parent_node_id not in MENU:
        print(f"WARNING: Parent node '{parent_node_id}' not found for node '{node.id}', falling back to root")
        parent_node_id = "root"
    
    # Back button: goes to parent (or root if no parent)
    footer_buttons.append(InlineKeyboardButton(
        text="⬅ Back",
        callback_data=f"menu:{parent_node_id}"
    ))
    
    # Home button: always goes to root
    footer_buttons.append(InlineKeyboardButton(
        text="🏠 Home",
        callback_data=f"menu:root"
    ))
    
    if footer_buttons:
        rows.append(footer_buttons)
    
    return InlineKeyboardMarkup(inline_keyboard=rows)


def get_checklist_text(user_id: int) -> str:
    """Generate checklist text with progress."""
    completed, total = get_checklist_progress(user_id)
    return (
        "<b>Step 5 — Go-live checklist</b>\n\n"
        "Mark each item as completed before go-live.\n\n"
        f"<b>Progress: {completed} / {total} completed</b>"
    )


def render_node(node_id: str, user_id: Optional[int] = None) -> tuple[str, InlineKeyboardMarkup]:
    """
    Unified function to render any node.
    Returns (text, keyboard) tuple.
    This is the SINGLE source of truth for node rendering.
    """
    # If node_id not found, fallback to root
    if node_id not in MENU:
        print(f"WARNING: node_id '{node_id}' not found in MENU, falling back to root")
        node_id = "root"
    
    node = MENU[node_id]
    
    # CRITICAL: Root node ALWAYS uses static main menu directly
    if node_id == "root":
        print("DEBUG: render_node() - Root node detected, using build_main_menu() directly")
        return (node.text, build_main_menu())
    
    # Special handling for checklist node
    if node_id == "start_step_7":
        if user_id is None:
            raise ValueError("user_id is required for checklist node")
        text = get_checklist_text(user_id)
        keyboard = build_menu_keyboard(node, user_id=user_id)
        return (text, keyboard)
    
    # Regular node
    text = node.text
    keyboard = build_menu_keyboard(node)
    return (text, keyboard)


async def show_node(message: Message, node_id: str) -> None:
    """
    Show a menu node by sending a new message.
    Used for /start command.
    For callbacks, use edit_node instead.
    """
    user_id = message.from_user.id if message.from_user else None
    text, keyboard = render_node(node_id, user_id=user_id)
    
    # Send new message
    await message.answer(text, reply_markup=keyboard, disable_web_page_preview=True)
    
    # Send files if any
    node = MENU[node_id] if node_id in MENU else MENU["root"]
    if node.files:
        for file_ref in node.files:
            if file_ref.path.exists():
                file = FSInputFile(file_ref.path)
                await message.answer_document(file, caption=file_ref.title)


async def open_node(message: Message, node_id: str, user_id: Optional[int] = None, mode: str = "edit") -> None:
    """
    Unified function to open a node.
    mode: "edit" (preferred) or "answer"
    This is the SINGLE entry point for node navigation.
    """
    # Render node using unified function
    text, keyboard = render_node(node_id, user_id=user_id)
    
    if mode == "edit":
        # Try to edit existing message
        try:
            await message.edit_text(
                text,
                reply_markup=keyboard,
                disable_web_page_preview=True
            )
        except Exception as e:
            # Handle different types of errors
            error_msg = str(e).lower()
            if "message is not modified" in error_msg or "message_not_modified" in error_msg:
                # This is OK - message content didn't change, but we still want to update keyboard
                try:
                    await message.edit_reply_markup(reply_markup=keyboard)
                except Exception as e2:
                    print(f"Failed to update keyboard: {e2}")
            else:
                # Message was deleted or can't be edited - send new one as fallback
                try:
                    await message.answer(text, reply_markup=keyboard, disable_web_page_preview=True)
                except Exception as e2:
                    print(f"Failed to send fallback message: {e2}")
    else:
        # Send new message
        await message.answer(text, reply_markup=keyboard, disable_web_page_preview=True)


async def edit_node(message: Message, node_id: str, user_id: Optional[int] = None) -> None:
    """
    Edit existing message to show a menu node.
    Used for callback queries.
    DEPRECATED: Use open_node() instead. Kept for backward compatibility.
    """
    await open_node(message, node_id, user_id=user_id, mode="edit")


# ---------- HANDLERS ----------

# Track processed messages and callbacks to prevent duplicates
_processed_messages = set()
_processed_callbacks = set()

# Get or create user lock for preventing race conditions
async def get_user_lock(user_id: int) -> asyncio.Lock:
    """Get or create a lock for a specific user."""
    async with _lock_manager_lock:
        if user_id not in _user_locks:
            _user_locks[user_id] = asyncio.Lock()
        return _user_locks[user_id]


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    """Handle /start command - show root menu."""
    # Create unique identifier for this message
    msg_id = f"{message.chat.id}:{message.message_id}"
    
    # If already processed, skip
    if msg_id in _processed_messages:
        return
    
    # Mark as processed
    _processed_messages.add(msg_id)
    
    # Clean up old entries periodically
    if len(_processed_messages) > 200:
        _processed_messages.clear()
    
    await show_node(message, "root")


# File callback handler - must be registered BEFORE menu handler
@router.callback_query(F.data.startswith("file:"))
async def on_file_callback(cb: CallbackQuery) -> None:
    """Handle file download requests"""
    if cb.message is None:
        return
    
    # Create unique identifier
    callback_id = f"{cb.message.chat.id}:{cb.message.message_id}:{cb.data}"
    
    # If already processed, skip
    if callback_id in _processed_callbacks:
        try:
            await cb.answer()
        except:
            pass
        return
    
    # Mark as processed
    _processed_callbacks.add(callback_id)
    
    # Clean up old entries periodically
    if len(_processed_callbacks) > 200:
        _processed_callbacks.clear()
    
    try:
        # Parse callback data: file:node_id:file_title
        parts = cb.data.split(":", 2)
        
        if len(parts) != 3:
            await cb.answer("Invalid file request format", show_alert=True)
            return
        
        _, node_id, file_title = parts
        node = MENU.get(node_id)
        
        if not node or not node.files:
            await cb.answer("File not found", show_alert=True)
            return
        
        # Find file by title
        file_ref = next((f for f in node.files if f.title == file_title), None)
        if not file_ref or not file_ref.path.exists():
            await cb.answer("File not found", show_alert=True)
            return
        
        file = FSInputFile(file_ref.path)
        await cb.message.answer_document(file, caption=file_title)
        await cb.answer()
        
    except Exception as e:
        print(f"Error in file callback handler: {e}")
        await cb.answer("An error occurred while loading the file", show_alert=True)


# Menu callback handler - handles menu:/v3:/v4: formats
@router.callback_query(F.data.startswith("menu:") | F.data.startswith("v3:") | F.data.startswith("v4:"))
async def on_menu_callback(cb: CallbackQuery) -> None:
    """
    Handle menu navigation callbacks.
    Supports formats: menu:<node_id>, v3:<node_id>, v4:<node_id>
    """
    if cb.message is None or cb.from_user is None:
        return
    
    user_id = cb.from_user.id
    
    # Get user lock to prevent race conditions
    user_lock = await get_user_lock(user_id)
    
    # Use lock to prevent concurrent processing
    async with user_lock:
        # Parse callback data using unified parser
        node_id = parse_callback(cb.data)
        
        if node_id is None:
            print(f"ERROR: Failed to parse callback data '{cb.data}'")
            try:
                await cb.answer("Invalid callback data", show_alert=True)
            except:
                pass
            return
        
        # If node_id not found in MENU - log error and return silently
        if node_id not in MENU:
            print(f"ERROR: Unknown section node_id='{node_id}', callback_data='{cb.data}'")
            try:
                await cb.answer()  # Close loading indicator without alert
            except:
                pass
            return
        
        # Answer callback FIRST to close loading indicator immediately
        try:
            await cb.answer()
        except Exception as e:
            print(f"WARNING: Failed to answer callback: {e}")
        
        # Then edit the message using unified function
        try:
            await open_node(cb.message, node_id, user_id=user_id, mode="edit")
        except Exception as e:
            # Log error for debugging
            print(f"ERROR opening node '{node_id}': {e}")
            import traceback
            traceback.print_exc()


@router.callback_query(F.data.startswith("toggle:"))
async def on_checklist_toggle(cb: CallbackQuery) -> None:
    """Handle checklist item toggle callbacks - format: toggle:<item_id>"""
    if cb.message is None or cb.from_user is None:
        return
    
    user_id = cb.from_user.id
    
    # Get user lock to prevent race conditions
    user_lock = await get_user_lock(user_id)
    
    # Use lock to prevent concurrent processing
    async with user_lock:
        # Parse callback data: "toggle:<item_id>"
        try:
            _, item_id = cb.data.split(":", 1)
            item_id = item_id.strip()
        except Exception as e:
            print(f"ERROR parsing toggle callback data '{cb.data}': {e}")
            try:
                await cb.answer("Invalid callback data", show_alert=True)
            except:
                pass
            return
        
        # Verify item_id exists in checklist
        item_exists = any(item_id == item_id_check for items in CHECKLIST_ITEMS.values() for item_id_check, _ in items)
        if not item_exists:
            print(f"ERROR: Unknown checklist item_id='{item_id}'")
            try:
                await cb.answer("Unknown checklist item", show_alert=True)
            except:
                pass
            return
        
        # Toggle item
        new_state = toggle_checklist_item(user_id, item_id)
        status = "checked" if new_state else "unchecked"
        print(f"DEBUG: Toggled item '{item_id}' for user {user_id}: {status}")
        
        # Answer callback immediately
        try:
            await cb.answer()
        except Exception as e:
            pass
        
        # Update message with new checklist state using unified function
        try:
            await open_node(cb.message, "start_step_7", user_id=user_id, mode="edit")
        except Exception as e:
            print(f"ERROR updating checklist message: {e}")
            import traceback
            traceback.print_exc()


# ---------- RUN ----------

# Protection against double startup
LOCK_FILE = Path(__file__).parent / ".bot.lock"


def check_single_instance() -> None:
    """Check if another instance is already running."""
    if LOCK_FILE.exists():
        # Try to read PID from lock file
        try:
            with open(LOCK_FILE, "r") as f:
                old_pid = int(f.read().strip())
            # Check if process is still running using kill -0
            try:
                # Signal 0 doesn't kill, just checks if process exists
                os.kill(old_pid, 0)
                print(f"ERROR: Another bot instance is already running (PID: {old_pid})")
                print("Please stop the existing instance or remove .bot.lock file")
                sys.exit(1)
            except ProcessLookupError:
                # Process doesn't exist, remove stale lock file
                LOCK_FILE.unlink(missing_ok=True)
            except PermissionError:
                # Process exists but we can't signal it (different user)
                print(f"WARNING: Lock file exists (PID: {old_pid}), but cannot verify")
                print("If you're sure no other instance is running, remove .bot.lock file")
        except (ValueError, FileNotFoundError):
            # Invalid lock file, remove it
            LOCK_FILE.unlink(missing_ok=True)
    
    # Create lock file with current PID
    try:
        with open(LOCK_FILE, "w") as f:
            f.write(str(os.getpid()))
    except Exception as e:
        print(f"Warning: Could not create lock file: {e}")


def cleanup_lock() -> None:
    """Remove lock file on exit."""
    try:
        LOCK_FILE.unlink(missing_ok=True)
    except Exception:
        pass


def validate_menu_structure() -> None:
    """Validate that all menu node references exist."""
    errors = []
    for node_id, node in MENU.items():
        # Check children
        for _, child_id in node.children:
            if child_id not in MENU:
                errors.append(f"Node '{node_id}' references non-existent child '{child_id}'")
        # Check parent
        if node.parent_id is not None and node.parent_id not in MENU:
            errors.append(f"Node '{node_id}' references non-existent parent '{node.parent_id}'")
    
    if errors:
        print("ERROR: Menu structure validation failed:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)


async def main() -> None:
    """Main bot function - called exactly once."""
    try:
        print("=" * 60)
        print("Bot starting...")
        print(f"Process ID (PID): {os.getpid()}")
        print(f"BOT STARTED WITH TOKEN PREFIX: {TOKEN_PREFIX}")
        print(f"Total menu nodes: {len(MENU)}")
        
        # Validate menu structure
        validate_menu_structure()
        print("Menu structure validation: OK")
        print("=" * 60)
        
        # This is the ONLY place where start_polling is called
        # drop_pending_updates=True prevents old callbacks from breaking routing
        await dp.start_polling(bot, drop_pending_updates=True)
    except Exception as e:
        print(f"ERROR in main(): {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        cleanup_lock()


if __name__ == "__main__":
    # Check for single instance before starting
    check_single_instance()
    
    # Register cleanup on exit
    import atexit
    atexit.register(cleanup_lock)
    
    # Start bot - this is the ONLY place where asyncio.run() is called
    asyncio.run(main())
