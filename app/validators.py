# Copyright (c) 2026 Wilkend. All rights reserved.
# Hantalk - proprietary software. See LICENSE at the repository root.
# Unauthorized copying, modification, or redistribution is prohibited.

import re

# Intentionally loose. Strict RFC 5322 regexes reject valid addresses
# and can't prove a mailbox exists anyway — only a confirmation email can.
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[A-Za-z]{2,}$")

# Anything a person might type between the digits of a phone number.
PHONE_NOISE = re.compile(r"[\s\-().]")
PHONE_RE = re.compile(r"^\+?\d{7,15}$")     # E.164 up to 15 digits

# Starts with a letter, then letters/digits/./_ — 3 to 20 characters total.
USERNAME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9._]{2,19}$")

MIN_NAME = 2
MIN_PASSWORD = 8

EMAIL = "email"
PHONE = "phone"
USERNAME = "username"


# ── Recognize an identifier ─────────────────────────────────

def identifier_kind(value: str) -> str:
    """What kind of identifier is this? See the module docstring for the order."""
    value = value.strip()
    if "@" in value:
        return EMAIL
    digits = PHONE_NOISE.sub("", value)
    if digits and re.fullmatch(r"\+?\d+", digits):
        return PHONE
    return USERNAME


def normalize_identifier(value: str) -> str:
    """The form we send to the backend — not the form the person typed."""
    value = value.strip()
    kind = identifier_kind(value)
    if kind == EMAIL:
        return value.lower()
    if kind == PHONE:
        return PHONE_NOISE.sub("", value)
    return value.lower()


def identifier_error(value: str) -> str | None:
    """Validate a login identifier — email, phone, OR username."""
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
    """Same thing, BUT without username — for /register and /forgot.

    We can't send a reset link to a username: there has to be a
    mailbox or a phone number behind it.
    """
    value = value.strip()
    if identifier_kind(value) == EMAIL:
        return None if EMAIL_RE.match(value) else "Enter a valid email address"
    if PHONE_RE.match(PHONE_NOISE.sub("", value)):
        return None
    return "Enter a valid email or phone number"


# ── Other fields ────────────────────────────────────────────

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
