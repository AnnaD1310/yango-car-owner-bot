import asyncio
import os
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

bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
router = Router()
dp.include_router(router)

# Paths
RESOURCES_DIR = Path(__file__).parent / "resources"
CONTRACTS_DIR = RESOURCES_DIR / "contracts"


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
        children=[
            ("🚀 Start launch", "start_launch"),
            ("📁 Materials & templates", "materials"),
            ("💬 Communication flows", "flows"),
            ("📊 Reports & KPI", "reports"),
            ("❓ FAQ", "faq"),
            ("👥 Contacts", "contacts"),
        ],
    )
)


# 1. Start launch -------------------------------------------------------------

add_node(
    MenuNode(
        id="start_launch",
        title="Start launch",
        text=(
            "<b>🚀 Start launch</b>\n\n"
            "Follow these steps to launch a car-owner acquisition stream in a new country."
        ),
        parent_id="root",
        children=[
            ("Step 1 — Market & Model", "start_step_1"),
            ("Step 2 — Ops readiness", "start_step_2"),
            ("Step 3 — Acquisition channels", "start_step_3"),
            ("Step 4 — Lead processing", "start_step_4"),
            ("Step 5 — Partner activation", "start_step_5"),
            ("Step 6 — Reporting & KPI", "start_step_6"),
            ("Step 7 — Go live checklist", "start_step_7"),
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
            "<b>Market analysis checklist:</b>\n"
            "• Size of city and car ownership patterns\n"
            "• Typical income levels and spending habits\n"
            "• Existing car rental patterns (if any)\n"
            "• Potential partner profiles (small fleets, individuals, SMEs)\n\n"
            "<b>Financial model template:</b>\n"
            "Build a financial model to estimate unit economics.\n\n"
            "<b>Examples of research:</b>\n"
            "See landing examples and research from existing countries."
        ),
        parent_id="start_launch",
        links=[
            Link("🇿🇲 Zambia landing", "https://yango.com/en_zm/carinvest/"),
            Link("🇦🇴 Angola landing", "https://yango.com/en_ao/carinvest/"),
            Link("🇨🇲 Cameroon landing", "https://yango.com/en_cm/carinvest/"),
            Link("🇪🇹 Ethiopia landing", "https://yango.com/en_et/carinvest/"),
            Link("Car acquisition tracker example (Sheet)",
                 "https://docs.google.com/spreadsheets/d/10AaTXOAnVByDSS3FKISnkxXkqutKzbq1qkXrspyQKj0/edit?gid=288663658#gid=288663658"),
        ],
    )
)

# Step 2
add_node(
    MenuNode(
        id="start_step_2",
        title="Step 2 — Ops readiness",
        text=(
            "<b>Step 2 — Ops readiness</b>\n\n"
            "<b>Scouts & call center readiness checklist:</b>\n"
            "• Scouts and call-center flow defined and documented\n"
            "• Lead handling script prepared for scouts / call center\n\n"
            "<b>Contracts required:</b>\n"
            "Contracts are prepared and localized (see Materials & templates → Contracts).\n\n"
            "<b>Partner onboarding process:</b>\n"
            "Clear process for onboarding partners.\n\n"
            "<b>Lead handling steps:</b>\n"
            "Define who calls, when, how many attempts.\n\n"
            "<b>Landing structure template:</b>\n"
            "Use landing content template for web team."
        ),
        parent_id="start_launch",
        links=[
            Link("Example web ticket (YANGOWEB-439)", "https://st.yandex-team.ru/YANGOWEB-439"),
            Link("Lead tracker (Sheet)",
                 "https://docs.google.com/spreadsheets/d/1WhA1pt725L9uGHG6pDDRx5iFxSz2xPRuGJJGIPsAoAA/edit"),
            Link("KPI tracker (Sheet)",
                 "https://docs.google.com/spreadsheets/d/1G43o8VMwbvrzNniwv8fOVm1W_xOawFLbfTZusbaDtZI/edit"),
        ],
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
        title="Step 4 — Lead processing",
        text=(
            "<b>Step 4 — Lead processing</b>\n\n"
            "<b>Lead qualification rules:</b>\n"
            "Define who is a good lead (car model, year, mileage, ownership).\n\n"
            "<b>Scripts for calls:</b>\n"
            "Use scripts for calling and follow-up from the table below.\n\n"
            "<b>Examples of contacted leads:</b>\n"
            "Track examples of good and bad leads.\n\n"
            "<b>Lead response SLA:</b>\n"
            "Define how fast you must contact each lead (e.g., within 24 hours)."
        ),
        parent_id="start_launch",
        links=[
            Link("Lead handling scripts (Sheet)",
                 "https://docs.google.com/spreadsheets/d/1Zj2345sqJvAdQ_jZ-9-RHe86y-w83bPpl6VKMLzn5Zg/edit?resourcekey=&gid=887705287#gid=887705287"),
            Link("Lead tracker (Sheet)",
                 "https://docs.google.com/spreadsheets/d/1WhA1pt725L9uGHG6pDDRx5iFxSz2xPRuGJJGIPsAoAA/edit"),
        ],
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
        title="Step 7 — Go live checklist",
        text=(
            "<b>Step 7 — Go live checklist</b>\n\n"
            "<b>Last validation checklist:</b>\n"
            "• All operations ready (scouts, call center, contracts)\n"
            "• Acquisition channels configured (landing/WA)\n"
            "• Lead processing flow tested\n"
            "• KPIs tracking set up\n\n"
            "<b>Launch communication plan:</b>\n"
            "• Marketing materials ready\n"
            "• Communication channels prepared\n"
            "• Team briefed\n\n"
            "<b>Monitoring plan for first 14 days:</b>\n"
            "• Daily check-ins\n"
            "• Weekly reports scheduled\n"
            "• Escalation process defined"
        ),
        parent_id="start_launch",
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
            FileRef("Contract FR (Cameroon)", CONTRACTS_DIR / "Сontract FR (Cameroon).pdf"),
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
            "<b>💬 Communication flows</b>\n\n"
            "Choose a flow to see the high-level steps and links."
        ),
        parent_id="root",
        children=[
            ("Landing flow", "flows_landing"),
            ("WhatsApp flow (Zambia example)", "flows_wa"),
            ("Partner onboarding flow", "flows_partner"),
        ],
    )
)

# Landing flow
add_node(
    MenuNode(
        id="flows_landing",
        title="Landing flow",
        text=(
            "<b>Landing flow</b>\n\n"
            "<b>Main user journey:</b>\n"
            "1. Ad click → landing page\n"
            "2. Landing explains value, requirements, models, earnings, trust\n"
            "3. User fills form → lead captured in Google Sheet\n"
            "4. Call-center / partner calls lead, qualifies and invites to office\n"
            "5. Office visit: docs & car check\n"
            "6. Contract signing\n"
            "7. Add car to fleet system / partner account"
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

# WhatsApp flow
add_node(
    MenuNode(
        id="flows_wa",
        title="WhatsApp flow (Zambia example)",
        text=(
            "<b>WhatsApp flow (Zambia example)</b>\n\n"
            "<b>Main user journey:</b>\n"
            "1. Ad click → WA chat opens\n"
            "2. Auto-greeting explains the program\n"
            "3. Agent asks qualification questions (cars, model, year, mileage)\n"
            "4. If qualified — move lead to partner / schedule meeting\n"
            "5. Office visit: docs & car check\n"
            "6. Contract signing\n"
            "7. Add car to fleet system\n\n"
            "<b>Example greeting (Zambia):</b>\n"
            "Hi! 👋 Thanks for your interest.\n\n"
            "The program is simple: if you have a car, you can rent it to a Yango partner "
            "and receive weekly income — without driving yourself.\n\n"
            "We'll ask a few quick questions to confirm your car is available and meets the requirements.\n\n"
            "You can already reply with:\n"
            "– How many cars you have\n"
            "– Make and model\n"
            "– Year of manufacture\n"
            "– Mileage\n\n"
            "You can also find more details here: https://yango.com/en_zm/carinvest/"
        ),
        parent_id="flows",
        links=[
            Link("WA scripts & questions (Sheet)",
                 "https://docs.google.com/spreadsheets/d/1Zj2345sqJvAdQ_jZ-9-RHe86y-w83bPpl6VKMLzn5Zg/edit?resourcekey=&gid=887705287#gid=887705287"),
        ],
    )
)

# Partner onboarding flow
add_node(
    MenuNode(
        id="flows_partner",
        title="Partner onboarding flow",
        text=(
            "<b>Partner onboarding flow</b>\n\n"
            "<b>Steps that partner goes through after contact:</b>\n"
            "1. Initial contact and qualification\n"
            "2. Meeting scheduled (office visit or online)\n"
            "3. Documentation review (ID, car ownership, insurance)\n"
            "4. Car inspection and validation\n"
            "5. Contract signing\n"
            "6. Onboarding to fleet system\n"
            "7. First driver assignment\n"
            "8. Day 1 support and monitoring"
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
            ("Weekly report templates", "reports_weekly"),
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
            "Target ranges based on Zambia, Angola, Cameroon, Ethiopia:\n\n"
            "• CPL: $5–15\n"
            "• CPA: $50–150\n"
            "• Conversion rate: 15–30%\n"
            "• Retention (4 weeks): 60–80%"
        ),
        parent_id="reports",
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

# Weekly report templates
add_node(
    MenuNode(
        id="reports_weekly",
        title="Weekly report templates",
        text=(
            "<b>Weekly report templates</b>\n\n"
            "<b>Structure:</b>\n\n"
            "<b>Inputs:</b>\n"
            "• Leads collected\n"
            "• Contracts signed\n"
            "• Active cars\n"
            "• Ad spend\n\n"
            "<b>Outputs:</b>\n"
            "• CPL, CPA, conversion rates\n"
            "• Retention metrics\n"
            "• Narrative: what worked, what didn't, next steps"
        ),
        parent_id="reports",
        links=[
            Link("Example weekly report (Sheet)",
                 "https://docs.google.com/spreadsheets/d/1Zj2345sqJvAdQ_jZ-9-RHe86y-w83bPpl6VKMLzn5Zg/edit?resourcekey=&gid=2116500930#gid=2116500930"),
        ],
    )
)


# 5. FAQ ---------------------------------------------------------------------

faq_text = (
    "<b>❓ FAQ</b>\n\n"
    "<b>Q: What is the program about?</b>\n"
    "A: The program helps car owners rent their vehicles to Yango partners and earn "
    "predictable weekly income without needing to drive themselves.\n\n"
    "<b>Q: Which cars are eligible?</b>\n"
    "A: Accepted city cars with relevant year and mileage; insurance required per country policy.\n\n"
    "<b>Q: How long does onboarding take?</b>\n"
    "A: Typically 1–2 weeks from initial contact to contract signing and car activation.\n\n"
    "<b>Q: Who is this bot for?</b>\n"
    "A: For local teams launching car owner acquisition streams.\n\n"
    "<b>Q: Which countries are covered?</b>\n"
    "A: Initially Zambia, Angola, Cameroon, Ethiopia — but structure is reusable.\n\n"
    "<b>Q: Where do I find contracts?</b>\n"
    "A: In Materials & templates → Contracts."
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


def build_menu_keyboard(node: MenuNode) -> InlineKeyboardMarkup:
    """Build keyboard with section items, links, files, and nav buttons (Back/Home)."""
    
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
    
    if node.parent_id is not None:
        footer_buttons.append(InlineKeyboardButton(
            text="⬅ Back",
            callback_data=f"menu:{node.parent_id}"
        ))
    
    footer_buttons.append(InlineKeyboardButton(
        text="🏠 Home",
        callback_data=f"menu:root"
    ))
    
    if footer_buttons:
        rows.append(footer_buttons)
    
    return InlineKeyboardMarkup(inline_keyboard=rows)


# Global lock to prevent duplicate renders
_rendering_lock = set()

async def render_node(
    node_id: str,
    message: Optional[Message] = None,
    callback: Optional[CallbackQuery] = None,
) -> None:
    """
    Universal function to render a menu node.
    Either sends a new message OR edits an existing one, but never both.
    """
    # Create unique lock key
    if message is not None:
        lock_key = f"msg:{message.chat.id}:{message.message_id}"
    elif callback is not None and callback.message is not None:
        lock_key = f"cb:{callback.message.chat.id}:{callback.message.message_id}:{callback.data}"
    else:
        return
    
    # Check if already rendering this exact action
    if lock_key in _rendering_lock:
        return
    
    # Lock this action
    _rendering_lock.add(lock_key)
    
    # Clean old locks (keep last 50)
    if len(_rendering_lock) > 50:
        _rendering_lock.clear()
    
    try:
        # If node_id not found, fallback to root without alerts or exceptions
        if node_id not in MENU:
            node_id = "root"
        
        node = MENU[node_id]
        text = node.text
        keyboard = build_menu_keyboard(node)
        
        # Variant 1: start command or text message - send new message
        if message is not None:
            await message.answer(text, reply_markup=keyboard)
            # Send files if any
            if node.files:
                for file_ref in node.files:
                    if file_ref.path.exists():
                        file = FSInputFile(file_ref.path)
                        await message.answer_document(file, caption=file_ref.title)
            return
        
        # Variant 2: inline button click - edit existing message
        if callback is not None:
            if callback.message is None:
                return
            try:
                await callback.message.edit_text(
                    text,
                    reply_markup=keyboard,
                    disable_web_page_preview=True
                )
            except Exception as e:
                # If edit fails (e.g., message not modified), just log it
                print(f"Edit failed (message may be unchanged): {e}")
            # Always answer callback silently (no alerts, no errors)
            try:
                await callback.answer()
            except:
                pass
            return
    finally:
        # Remove lock after a short delay
        import asyncio
        asyncio.create_task(_unlock_after_delay(lock_key))

async def _unlock_after_delay(lock_key: str):
    """Remove lock after a delay."""
    import asyncio
    await asyncio.sleep(1)
    _rendering_lock.discard(lock_key)


# ---------- HANDLERS ----------


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    """Handle /start command - show root menu."""
    await render_node("root", message=message)


# Track processed callbacks to prevent duplicates
_processed_callbacks = set()

# File callback handler must be registered BEFORE universal menu handler
@router.callback_query(F.data.startswith("file:"))
async def on_file_callback(cb: CallbackQuery) -> None:
    """Handle file download requests"""
    if cb.message is None:
        return
    
    try:
        # Parse callback data: file:node_id:file_title
        # Handle both new format (file:node_id:file_title) and old format (file:version:node_id:file_title)
        parts = cb.data.split(":", 3)
        
        if len(parts) == 3:
            # New format: file:node_id:file_title
            _, node_id, file_title = parts
        elif len(parts) == 4:
            # Old format: file:version:node_id:file_title
            _, version, node_id, file_title = parts
        else:
            await cb.answer("Invalid file request format", show_alert=True)
            return
        
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


# Universal menu callback handler - handles menu:, v1:, v2:, v3:, v4: formats
@router.callback_query()
async def on_menu_callback(cb: CallbackQuery) -> None:
    """Handle menu navigation callbacks - supports all formats: menu:, v1:, v2:, v3:, v4:"""
    if cb.message is None:
        return
    
    # Skip file callbacks - they are handled separately
    if cb.data and cb.data.startswith("file:"):
        return
    
    # Create unique identifier
    callback_id = f"{cb.message.chat.id}:{cb.message.message_id}:{cb.data}"
    
    # Check if already processed
    if callback_id in _processed_callbacks:
        # Just answer silently
        try:
            await cb.answer()
        except:
            pass
        return
    
    # Mark as processed BEFORE processing
    _processed_callbacks.add(callback_id)
    
    # Clean old entries
    if len(_processed_callbacks) > 200:
        _processed_callbacks.clear()
    
    # Parse callback data - handle all formats: menu:<node_id>, v1:<node_id>, v2:<node_id>, v3:<node_id>, v4:<node_id>
    raw = cb.data or ""
    node_id = "root"  # Default fallback
    
    try:
        if ":" in raw:
            prefix, payload = raw.split(":", 1)
            # For all our formats (menu, v1, v2, v3, v4), take the payload as node_id
            if prefix in {"menu", "v1", "v2", "v3", "v4"}:
                node_id = payload.strip()
            else:
                # Unknown prefix - use payload anyway, will fallback to root if not found
                node_id = payload.strip()
        else:
            # No colon - use raw as node_id
            node_id = raw.strip()
        
        # Block removed nodes - fallback to root
        if node_id == "materials_ops":
            node_id = "root"
        
        # If node_id not found, fallback to root (render_node will handle this)
        if node_id not in MENU:
            node_id = "root"
        
        # Render the node (will fallback to root if node_id not found)
        await render_node(node_id, callback=cb)
        
    except Exception as e:
        # On any error, just render root without alerts
        print(f"Error in callback handler: {e}")
        try:
            await render_node("root", callback=cb)
        except:
            pass


# ---------- RUN ----------


async def main() -> None:
    print("Bot running with structured menu...")
    print(f"Total menu nodes: {len(MENU)}")
    print(f"Step 3 updated: {'LANDING CHANNEL' in MENU['start_step_3'].text}")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
