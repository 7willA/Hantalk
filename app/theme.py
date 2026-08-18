# Copyright (c) 2026 Wilkend. All rights reserved.
# Hantalk - proprietary software. See LICENSE at the repository root.
# Unauthorized copying, modification, or redistribution is prohibited.

import flet as ft

# ═════════════════════════════════════════════════
# 1. SCREEN-SPECIFIC PALETTES & UI PLACEMENT
# ═════════════════════════════════════════════════

# ─────────────────────────────────────
# HERO / ONBOARDING SCREEN
# ─────────────────────────────────────
HERO_BG = "#F8FAFC"             # Main screen background on first launch / welcome screens
HERO_GRADIENT_START = "#243D7D" # Navy — top/start of hero banners & CTA buttons (logo wordmark)
HERO_GRADIENT_END = "#3A8FD5"   # Blue — bottom/end of the gradient (right leg of the H)
HERO_GRADIENT_DEEP = "#18294F"  # Darker navy when tapping or holding onboarding buttons

HERO_TITLE = "#0F172A"          # Main welcome header text ("Master Mandarin Naturally") 17.06:1
HERO_SUBTITLE = "#475569"       # Onboarding description text below the main title (7.24:1)

HERO_BTN_TEXT = "#FFFFFF"       # Text inside primary onboarding buttons (10.3:1 on navy)

HERO_CARD_BG = "#FFFFFF"        # Feature preview cards on the landing/welcome screen
HERO_CARD_BORDER = "#E2E8F0"    # 1px hairline border surrounding onboarding feature cards

HERO_ACCENT_SOFT = "#DBEAFE"    # Soft blue badge backgrounds (e.g., "NEW", "POPULAR")
HERO_ACCENT_DEEP = "#172554"    # Deep navy text sitting inside soft blue badges (12.04:1)


# ─────────────────────────────────────
# HOME DASHBOARD
# ─────────────────────────────────────
HOME_BG = "#F8FAFC"             # Main dashboard page background (cool porcelain, matches logo canvas)

HOME_CARD = "#FFFFFF"           # Active lesson cards, practice tiles, and container surfaces
HOME_CARD_HOVER = "#F1F5F9"     # Background change when pressing or hovering a home card
HOME_CARD_LOCKED = "#F1F5F9"    # Background for locked/unopened future lessons
HOME_CARD_SELECTED = "#DBEAFE"  # Border/fill highlight when a user selects a lesson module

HOME_TEXT_PRIMARY = "#0F172A"   # App title ("Hantalk"), lesson headers, active text (17.06:1)
HOME_TEXT_SECONDARY = "#475569" # Subtitles, chapter descriptions ("Unit 3 • Conversational") 7.24:1
HOME_TEXT_HINT = "#64748B"      # Section titles ("PRACTICE MODES"), quiet labels, counters
                                # 4.55:1 — just clears WCAG AA. Do NOT lighten this to
                                # #94A3B8 (2.45:1); the hierarchy below HOME_TEXT_SECONDARY
                                # comes from size and weight, not from more grey.

HOME_PROGRESS_BG = "#E2E8F0"    # Unfilled background track of the main daily progress bar
HOME_PROGRESS_FILL_START = "#F39E4A" # Orange — start of the progress fill (left leg of the H)
HOME_PROGRESS_FILL_END = "#FDC534"   # Gold — end glow of the fill as lessons complete
HOME_PROGRESS_TRACK = "#CBD5E1" # Hairline outline framing progress tracks & audio sliders

HOME_STREAK = "#F97316"         # Fire ICON and bar fill only (2.3:1 — graphics, never text)
HOME_STREAK_TEXT = "#C2410C"    # The streak NUMBER next to the flame (4.95:1 — safe for text)
HOME_XP = "#F59E0B"             # Star/XP badge ICON fill only (2.05:1 — graphics, never text)
HOME_XP_TEXT = "#B45309"        # The XP NUMBER ("1,840 XP") (4.8:1 — safe for text)

HOME_BORDER = "#E2E8F0"         # Architectural 1px hairline borders for all dashboard cards
HOME_BORDER_STRONG = "#243D7D"  # High-contrast navy border for active chips and filters

HOME_NAV_BG = "#FFFFFF"         # Bottom NavigationBar surface
HOME_NAV_ACTIVE_BG = "#DBEAFE"  # Pill behind the selected nav destination
HOME_NAV_ACTIVE_FG = "#243D7D"  # Selected nav icon + label (8.44:1 on the pill)
HOME_NAV_IDLE_FG = "#64748B"    # Unselected nav icons and labels (4.55:1)


# ─────────────────────────────────────
# AI LIVE CHAT SCREEN (DARK MODE)
# ─────────────────────────────────────
# Deep NAVY, not black. Black would break the brand the moment the user
# switches from Home to this screen.
AI_BG = "#0B1220"               # Fullscreen dark background for live voice/text AI sessions

AI_BUBBLE_USER = "#1E2C48"      # Chat bubble background for the user's sent messages

AI_BUBBLE_AI_START = "#38BDF8"  # Sky — gradient start for AI responses / active speech
AI_BUBBLE_AI_END = "#1D4ED8"    # Blue — gradient end (white text on it = 6.7:1)

AI_TEXT = "#F1F5F9"             # Primary text in AI bubbles & Chinese characters (17.09:1)
AI_TEXT_MUTED = "#94A3B8"       # Pinyin, English subtitles, quiet AI text (7.3:1)

AI_GLOW_BLUE = "#38BDF8"        # Ambient glow ring around the avatar while listening (8.74:1)
AI_GLOW_WARM = "#F5B25E"        # Secondary glow while the AI is speaking (10.17:1)

AI_INPUT_BG = "#16213A"         # Text input box background at the bottom of the AI chat
AI_INPUT_BORDER = "#2C3D5F"     # 1px border framing the AI chat text box

AI_STATUS = "#99F1F5F9"         # Translucent status text ("AI is listening...")
AI_TEXT_FAINT = "#8CF1F5F9"     # Secondary translations beneath live spoken sentences
AI_PILL_BG = "#29F1F5F9"        # Background for top mode pills ("LIVE", "SCENARIO: MARKET")
AI_PILL_BORDER = "#38FFFFFF"    # Subtle border framing top AI status pills
AI_ICON_BG = "#1AF1F5F9"        # Circular background for side utility buttons near the mic
AI_AVATAR_BG = "#1E2C48"        # Background surface behind the central teacher avatar
AI_AVATAR_RING = "#5938BDF8"    # Outer pulsing ring during active conversation
AI_AVATAR_CAPTION = "#BF38BDF8" # Role badge beneath the avatar ("Native Tutor")
AI_DIVIDER = "#2C3D5F"          # Line separating chat history from the microphone area
AI_WAVE_IDLE = "#6638BDF8"      # Waveform color when the microphone is waiting / paused
AI_WAVE_ACTIVE = "#38BDF8"      # Animated waveform while the user is actively speaking
AI_LIVE = "#E6F97316"           # Orange "LIVE" pulse dot at the top of the AI screen
AI_MIC = "#243D7D"              # Main microphone button color in idle state
AI_MIC_ACTIVE = "#F97316"       # Main microphone button while recording (orange = live/hot)


# ─────────────────────────────────────
# LESSON & FLASHCARD SCREEN
# ─────────────────────────────────────
LESSON_BG = "#F8FAFC"           # Screen background for flashcards, quizzes, and exercises

LESSON_CARD = "#FFFFFF"         # Main flashcard surface showing Chinese characters / questions
LESSON_CARD_BORDER = "#E2E8F0"  # 1px border surrounding flashcards and multiple-choice options

LESSON_TEXT_MAIN = "#0F172A"    # Chinese character text and primary quiz question text (17.06:1)
LESSON_TEXT_HINT = "#64748B"    # Pinyin guide, stroke order hints, translation notes (4.55:1)

LESSON_CORRECT = "#10B981"      # Green ICON / bar / border for correct answers (2.42:1 — graphics)
LESSON_CORRECT_TEXT = "#047857" # The word "Correct!" and any green TEXT (5.24:1 — safe for text)
LESSON_WRONG = "#DC2626"        # Red ICON / bar / border for wrong answers (4.62:1)
LESSON_WRONG_TEXT = "#B91C1C"   # Error messages and any red TEXT (6.18:1 — safe for text)

LESSON_BTN_PRIMARY = "#243D7D"  # Primary "CHECK ANSWER" / "CONTINUE" action button (navy)
LESSON_BTN_TEXT = "#FFFFFF"     # Text inside the main lesson continuation buttons (10.3:1)

LESSON_TAB_ACTIVE = "#243D7D"   # Selected tab label + 3px indicator (9.85:1)
LESSON_TAB_IDLE = "#64748B"     # Unselected tab labels (4.55:1)

# Dialogue bubbles — teacher speaks light, learner speaks navy
LESSON_BUBBLE_THEM = "#F1F5F9"  # Teacher / other speaker bubble fill (text = LESSON_TEXT_MAIN)
LESSON_BUBBLE_ME = "#243D7D"    # Learner bubble fill (text = WHITE)
LESSON_BUBBLE_ME_DIM = "#B9CDEB"# Pinyin line inside the navy learner bubble (5.6:1 on navy)

ON_PRIMARY_SOFT = "#FFE8F0FE"   # Secondary text inside active navy selection cards.
                                # Navy is dark enough that a blue tint still clears AA here
                                # (5.9:1) — unlike the old rose-on-crimson which capped at 4.28.
ON_PRIMARY_SOFT_DIM = "#66DBEAFE" # Gridlines/dividers inside primary active selection cards
ON_PRIMARY_FILM = "#33FFFFFF"   # Subtle white overlay on active option cards


# ─────────────────────────────────────
# PHONETIC SCREEN 
# ─────────────────────────────────────
# Each writing system gets its own hue so the eye identifies it instantly.
PH_BG = "#F8FAFC"               # Phonetic screen background
PH_CARD = "#FFFFFF"             # One card per writing system
PH_HANZI = "#0F172A"            # 漢字 — the characters themselves (17.06:1)
PH_BOPOMOFO = "#243D7D"         # ㄅㄆㄇ — navy (9.85:1)
PH_TONGYONG = "#1D4ED8"         # Tongyong Pinyin — blue (6.41:1)
PH_PINYIN = "#C2410C"           # Hanyu Pinyin — burnt orange (4.95:1)
PH_CHIP_ON = "#DBEAFE"          # Lit toggle chip background
PH_CHIP_OFF = "#F1F5F9"         # Unlit toggle chip background
PH_SLIDER_BG = "#CBD5E1"        # Audio slider inactive track
PH_SLIDER_FG = "#243D7D"        # Audio slider filled track and thumb


# ─────────────────────────────────────
# REWARD & GAMIFICATION SCREEN
# ─────────────────────────────────────

REWARD_BG = "#F8FAFC"           # Background for lesson-complete and daily-recap modals

REWARD_GOLD = "#F59E0B"         # Coin, trophy, and star icons (2.05:1 — graphics only)
REWARD_GOLD_LIGHT = "#FEF3C7"   # Background glow behind earned XP badges

REWARD_FIRE = "#F97316"         # Animated flame graphic on streak milestone popups

REWARD_RARE = "#1D4ED8"         # Level-up badge borders and rare achievement icons.
                                # The logo has no purple — blue carries "rare" instead.

REWARD_SUCCESS = "#10B981"      # Accuracy gauge fill (e.g., "98% Accuracy") — graphics only


# ─────────────────────────────────────
# GLOBAL DARK MODE OVERRIDES
# ─────────────────────────────────────
DARK_BG = "#0B1220"             # System-wide dark mode background (deep navy)
DARK_SURFACE = "#16213A"        # Cards, bottom sheets, and nav bars in dark mode
DARK_CARD = "#1E2C48"           # Elevated dark mode containers and clickable tiles

DARK_TEXT = "#F1F5F9"           # Primary headings and readable text in dark mode (17.09:1)
DARK_TEXT_MUTED = "#94A3B8"     # Secondary labels and disabled text in dark mode (7.3:1)

DARK_BORDER = "#2C3D5F"         # 1px hairline borders framing dark mode elements

DARK_ORANGE = "#F5B25E"         # Orange accent lifted for dark backgrounds (10.17:1)
DARK_BLUE = "#38BDF8"           # Blue accent lifted for dark backgrounds (8.74:1)
DARK_RED = "#FF6B5E"            # Red accent lifted for dark backgrounds


# ─────────────────────────────────────
# STANDARD NEUTRALS
# ─────────────────────────────────────
WHITE = "#FFFFFF"               # Pure white for text on navy buttons and clean surfaces
BLACK = "#000000"               # Absolute black — shadows only, never a background


# ─────────────────────────────────────
# SECTION PALETTE (unit banners on the learning path)
# ─────────────────────────────────────
# Duolingo gives every unit banner its own color — that is how each unit gets
# an identity without drawing new artwork. Same idea here, but every hue is
# pulled from the logo's own two legs (cool blues, warm ambers) so the path
# never leaves the brand.
#
# The list WRAPS (see section_color below), so you can add 30 sections without
# running out of colors. Each entry is (banner, text-on-banner) and every pair
# below is >= 5:1, so section text stays readable everywhere.
SECTION_COLORS: list[tuple[str, str]] = [
    ("#243D7D", "#FFFFFF"),     # 1 — navy (koulè mak la)        9.85:1
    ("#1D4ED8", "#FFFFFF"),     # 2 — ble                        6.70:1
    ("#0369A1", "#FFFFFF"),     # 3 — ble oseyan                 5.93:1
    ("#0F766E", "#FFFFFF"),     # 4 — dlo vèt fonse              5.47:1
    ("#B45309", "#FFFFFF"),     # 5 — dore fonse                 5.02:1
    ("#C2410C", "#FFFFFF"),     # 6 — zoranj boukannen           5.18:1
]


def section_color(index: int) -> tuple[str, str]:
    """Koulè bandwòl yon seksyon: (fon, tèks).

    Endèks la anwole, donk seksyon 7 pran menm koulè ak seksyon 1.
    Konsa ajoute yon seksyon pa janm mande yon nouvo koulè.
    """
    return SECTION_COLORS[index % len(SECTION_COLORS)]


# ═════════════════════════════════════════════════
# 2. SEMANTIC MAP (MAPPING TO GLOBAL TOKENS)
# ═════════════════════════════════════════════════
# The 3,468 lines already written call the names in THIS block. Never delete
# one — change what it points to and the whole app re-themes at once.

PRIMARY = HERO_GRADIENT_START            # Main brand navy across the entire app
PRIMARY_DARK = HERO_GRADIENT_DEEP        # Pressed state for all primary buttons
PRIMARY_CONTAINER = HERO_ACCENT_SOFT     # Soft blue background fill for active selections
ON_PRIMARY_DEEP = HERO_ACCENT_DEEP       # Deep navy text over soft blue containers

ACCENT = HOME_PROGRESS_FILL_START        # Orange — energy: progress, streak, "Continue"
ACCENT_DARK = HOME_STREAK_TEXT           # Orange that is safe to use as TEXT
ACCENT_SOFT = "#FDEBD5"                  # Soft orange container fill
ACTIVE = "#1D4ED8"                       # Blue — the "currently selected" hue

BACKGROUND = HOME_BG                     # Default global app background
SURFACE = HOME_CARD                      # Default card and container background
SURFACE_VARIANT = HOME_CARD_HOVER        # Secondary elevated surface background

OUTLINE = HOME_BORDER                    # Standard 1px architectural card border
OUTLINE_STRONG = HOME_BORDER_STRONG      # Emphasized navy border for active focused items
DIVIDER = HOME_PROGRESS_BG               # Standard horizontal rule and track divider
TRACK = HOME_PROGRESS_TRACK              # Inactive track background for sliders

TEXT = HOME_TEXT_PRIMARY                 # Standard body & title text color
TEXT_SECONDARY = HOME_TEXT_SECONDARY     # Standard subtitle & metadata color
TEXT_MUTED = HOME_TEXT_HINT              # Standard caption & quiet hint color

LOCKED_BG = HOME_CARD_LOCKED             # Disabled / locked module surface fill
SELECTED_BORDER = HOME_CARD_SELECTED     # Border highlight for selected answers
PROGRESS_ACTIVE = HOME_PROGRESS_FILL_START  # Streak and momentum indicator fill

DARK_ACCENT = DARK_ORANGE                # Accent highlight in dark views
DARK_STRIPE = AI_INPUT_BORDER            # Border outline in dark views

SUCCESS = LESSON_CORRECT                 # Global green success state — ICONS / fills
SUCCESS_TEXT = LESSON_CORRECT_TEXT       # Global green success state — TEXT
ERROR = LESSON_WRONG                     # Global red error state — ICONS / fills
ERROR_TEXT = LESSON_WRONG_TEXT           # Global red error state — TEXT

XP_TEXT = HOME_XP_TEXT                   # XP counters written as text
STREAK_TEXT = HOME_STREAK_TEXT           # Streak counters written as text


# ═════════════════════════════════════════════════
# 3. GRADIENTS
# ═════════════════════════════════════════════════
# The logo is built on gradients — flat fills everywhere would lose it.

def grad_brand() -> ft.LinearGradient:
    """Navy → blue. Headers, hero cards, splash."""
    return ft.LinearGradient(
        begin=ft.Alignment.TOP_LEFT,
        end=ft.Alignment.BOTTOM_RIGHT,
        colors=[HERO_GRADIENT_START, HERO_GRADIENT_END],
    )


def grad_energy() -> ft.LinearGradient:
    """Orange → gold. Progress bars, streak, XP."""
    return ft.LinearGradient(
        begin=ft.Alignment.CENTER_LEFT,
        end=ft.Alignment.CENTER_RIGHT,
        colors=[HOME_PROGRESS_FILL_START, HOME_PROGRESS_FILL_END],
    )


def grad_ai() -> ft.LinearGradient:
    """Sky → blue. AI bubbles and the avatar halo."""
    return ft.LinearGradient(
        begin=ft.Alignment.TOP_LEFT,
        end=ft.Alignment.BOTTOM_RIGHT,
        colors=[AI_BUBBLE_AI_START, AI_BUBBLE_AI_END],
    )


# ═════════════════════════════════════════════════
# 4. TYPOGRAPHY & SPACING TOKENS
# ═════════════════════════════════════════════════

FONTS = {
    "NotoSans": "fonts/NotoSans-Regular.ttf",
    "NotoSansTC": "fonts/NotoSansTC-Regular.ttf",
    "NotoSerifTC": "fonts/NotoSerifTC-Medium.ttf",
}

FONT_UI = "NotoSans"            # Primary font for standard app navigation & English text
FONT_ZH = "NotoSansTC"          # Sans-serif Chinese font for clean UI readability
FONT_ZH_SERIF = "NotoSerifTC"   # Editorial serif Chinese font for large character display

# Corner Radius Tokens (component roundness)
RADIUS_XS = 6    # Tiny chips, badges, and status pills
RADIUS_SM = 8    # Action buttons and small input fields
RADIUS_MD = 12   # Standard lesson cards and practice tiles
RADIUS_LG = 16   # Hero progress cards and bottom sheets
RADIUS_XL = 24   # Fullscreen popups and modal dialogues — same squircle feel as the app icon

PAD_PAGE = 20    # Outer page padding (left/right screen margin)

GAP_SM = 8       # Tight spacing between connected labels
GAP_MD = 12      # Standard spacing between distinct components and cards
GAP_LG = 18      # Generous spacing between main page sections

# Typography Sizes
SIZE_DISPLAY = 96 # Massively scaled single Chinese character practice focus
SIZE_HERO = 46    # Onboarding hero banners and major achievement numbers
SIZE_TITLE = 26   # Screen titles and section headers
SIZE_ZH = 24      # Standard Chinese character reading size
SIZE_H2 = 19      # Card titles ("Intermediate Mandarin")
SIZE_H3 = 16      # Subheaders and option title text
SIZE_BODY = 14    # Regular reading text and descriptions
SIZE_SMALL = 12   # Secondary card details ("120 words due")
SIZE_LABEL = 11   # Uppercase tracking sub-labels ("PRACTICE MODES")
SIZE_TINY = 10    # Micro-labels, badge counts, and tiny indicators


# ═════════════════════════════════════════════════
# 5. FLET THEME INITIALIZATION
# ═════════════════════════════════════════════════

def apply_theme(page: ft.Page) -> None:
    """Applies global design theme and window parameters to Flet."""

    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = BACKGROUND           # Sets global window canvas background
    page.padding = 0                    # Edge-to-edge layouts

    page.window.width = 390             # Design viewport width from the UI handoff
    page.window.height = 844            # Design viewport height

    page.fonts = FONTS

    # NOTE: ft.ColorScheme in Flet 0.85 has NO `background` field — passing one
    # raises TypeError. The canvas color lives on page.bgcolor above.
    page.theme = ft.Theme(
        font_family=FONT_UI,
        color_scheme=ft.ColorScheme(
            primary=PRIMARY,
            on_primary=WHITE,
            primary_container=PRIMARY_CONTAINER,
            on_primary_container=ON_PRIMARY_DEEP,
            # Orange is the brand's secondary. on_secondary is near-black because
            # white on #F39E4A is only 2.1:1 — unreadable.
            secondary=ACCENT,
            on_secondary=TEXT,
            secondary_container=ACCENT_SOFT,
            on_secondary_container=ACCENT_DARK,
            tertiary=ACTIVE,
            on_tertiary=WHITE,
            surface=SURFACE,
            on_surface=TEXT,
            on_surface_variant=TEXT_SECONDARY,
            outline=OUTLINE,
            outline_variant=DIVIDER,
            # Flet paints error MESSAGES (TextField helper text) with this,
            # so it must be the text-safe red, not the vivid one.
            error=ERROR_TEXT,
            on_error=WHITE,
        ),
    )
