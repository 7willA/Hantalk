# Copyright (c) 2026 Wilkend. All rights reserved.
# Hantalk - proprietary software. See LICENSE at the repository root.
# Unauthorized copying, modification, or redistribution is prohibited.

"""Validators — règ ki pataje ant ekran auth yo.

POUKISA YON SÈL FICHYE

  Twa ekran mande menm bagay la: /login, /register, /forgot. Si chak
  youn gen pwòp regex li, yon jou youn ap aksepte yon nimewo telefòn
  lòt la ap rejte — epi moun nan p ap ka konekte ak kont li fèk kreye.
  Yon sèl sous verite anpeche sa.

LOGIK "EMAIL, TELEFÒN, OSWA NON ITILIZATÈ"

  Sou /login nou pa mande moun nan ki kalite idantifyan l ap tape — nou
  DEVINE l ak fòm nan:

      gen yon "@"                  → email
      chif sèlman (+ - ( ) espas)  → telefòn
      rès la                       → non itilizatè

  Lòd la enpòtan. Si nou te teste non itilizatè an premye, "0912345678"
  ta pase pou yon non itilizatè epi backend la ta chèche nan move kolòn.

  `identifier_kind()` bay kalite a, `normalize_identifier()` netwaye l
  pou backend la (email an miniskil, telefòn san espas, elatriye).
"""

import re

# Volontèman lach. Regex RFC 5322 strik yo rejte adrès ki valab epi yo
# pa ka pwouve yon bwat lèt egziste — se sèlman yon email konfimasyon.
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[A-Za-z]{2,}$")

# Tout sa yon moun ka tape ant chif yo nan yon nimewo telefòn.
PHONE_NOISE = re.compile(r"[\s\-().]")
PHONE_RE = re.compile(r"^\+?\d{7,15}$")     # E.164 rive jiska 15 chif

# Kòmanse ak yon lèt, apre sa lèt/chif/. /_ — 3 a 20 karaktè antou.
USERNAME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9._]{2,19}$")

MIN_NAME = 2
MIN_PASSWORD = 8

EMAIL = "email"
PHONE = "phone"
USERNAME = "username"


# ── Rekonèt yon idantifyan ─────────────────────────────────

def identifier_kind(value: str) -> str:
    """Ki kalite idantifyan sa a ye? Gade docstring modil la pou lòd la."""
    value = value.strip()
    if "@" in value:
        return EMAIL
    digits = PHONE_NOISE.sub("", value)
    if digits and re.fullmatch(r"\+?\d+", digits):
        return PHONE
    return USERNAME


def normalize_identifier(value: str) -> str:
    """Fòm nou voye bay backend la — pa fòm nan moun nan te tape a."""
    value = value.strip()
    kind = identifier_kind(value)
    if kind == EMAIL:
        return value.lower()
    if kind == PHONE:
        return PHONE_NOISE.sub("", value)
    return value.lower()


def identifier_error(value: str) -> str | None:
    """Valide yon idantifyan koneksyon — email, telefòn, OSWA non itilizatè."""
    value = value.strip()
    kind = identifier_kind(value)
    if kind == EMAIL:
        return None if EMAIL_RE.match(value) else "Enter a valid email address"
    if kind == PHONE:
        if PHONE_RE.match(PHONE_NOISE.sub("", value)):
            return None
        return "Phone numbers are 7–15 digits"
    if USERNAME_RE.match(value):
        return None
    return "Enter a valid email, phone number, or username"


def contact_error(value: str) -> str | None:
    """Menm bagay la, MEN san non itilizatè — pou /register ak /forgot.

    Nou pa ka voye yon lyen reyinisyalizasyon sou yon non itilizatè:
    fòk gen yon bwat lèt oswa yon nimewo dèyè l.
    """
    value = value.strip()
    if identifier_kind(value) == EMAIL:
        return None if EMAIL_RE.match(value) else "Enter a valid email address"
    if PHONE_RE.match(PHONE_NOISE.sub("", value)):
        return None
    return "Enter a valid email or phone number"


# ── Lòt chan yo ────────────────────────────────────────────

def name_error(value: str) -> str | None:
    if len(value.strip()) < MIN_NAME:
        return f"At least {MIN_NAME} characters"
    return None


def password_error(pw: str) -> str | None:
    if len(pw) < MIN_PASSWORD:
        return f"At least {MIN_PASSWORD} characters"
    if not (re.search(r"[A-Za-z]", pw) and re.search(r"\d", pw)):
        return "Mix letters and numbers"
    return None


def confirm_error(pw: str, confirm: str) -> str | None:
    if confirm != pw:
        return "Passwords do not match"
    return None


def strength(pw: str) -> tuple[int, str]:
    """Bay yon nòt 0–4 ak yon etikèt. Se yon KONSÈY, pa yon baryè.

    Sèl règ ki di yo se longè a ak melanj lèt+chif nan `password_error`.
    Vi a retounen etikèt la sèlman — se ekran an ki chwazi koulè a, pou
    modil sa a pa depann de `app.theme`.
    """
    if not pw:
        return 0, ""

    score = 0
    if len(pw) >= MIN_PASSWORD:
        score += 1
    if len(pw) >= 12:
        score += 1
    if re.search(r"[A-Za-z]", pw) and re.search(r"\d", pw):
        score += 1
    if re.search(r"[^A-Za-z0-9]", pw):
        score += 1

    return score, ("Weak", "Weak", "Fair", "Good", "Strong")[score]
