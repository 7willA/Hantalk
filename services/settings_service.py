# Copyright (c) 2026 Wilkend. All rights reserved.
# Hantalk - proprietary software. See LICENSE at the repository root.
# Unauthorized copying, modification, or redistribution is prohibited.

"""Settings service — user preferences, saved on the device.

Flutter counterpart: lib/services/settings_service.dart

HOW IT WORKS

  Flet 0.85 uses `ft.SharedPreferences`, which is a *Service*: it has
  to be attached to a View to stay alive (see `app/router.py`). All of
  its methods are `async`.

  But a UI can't wait for an `await` every time it needs to know
  whether Pinyin is on. So:

    - `load()`   reads disk ONCE at startup → fills `_cache`
    - `get()`    reads `_cache` — SYNCHRONOUS, fast, no `await`
    - `set()`    writes to `_cache` RIGHT AWAY, then saves to disk after

  This way the screen responds immediately and disk catches up behind
  it. If the save fails (for example on web without permission), the
  app keeps working with the value in memory — it will never throw an
  error in the person's face.
"""

import flet as ft

# All keys share the same prefix so they don't collide with another app.
PREFIX = "hantalk."

# Source of truth for each setting: key → default value.
# The value's type defines the type that's accepted (see `_coerce`).
DEFAULTS: dict[str, object] = {
    # ── Learning ──
    "phonetic_hanzi": True,
    "phonetic_bopomofo": False,
    "phonetic_tongyong": False,
    "phonetic_pinyin": True,
    "audio_speed": "normal",        # "normal" | "slow"
    "daily_goal_min": 20,           # 5 | 10 | 15 | 20
    # ── Notifications ──
    "notify_daily": True,
    "notify_time": "20:00",
    "notify_streak": True,
    "notify_weekly": False,
    # ── Appearance ──
    "theme_mode": "light",          # "light" | "dark" | "system"
    "zh_text_scale": 1.0,           # 0.8 → 1.4
    "sound_effects": True,
}

# Phonetic keys — we need them together for the "at least one on" rule.
PHONETIC_KEYS = (
    "phonetic_hanzi",
    "phonetic_bopomofo",
    "phonetic_tongyong",
    "phonetic_pinyin",
)

_prefs = ft.SharedPreferences()
_cache: dict[str, object] = dict(DEFAULTS)
_loaded = False


def service() -> ft.SharedPreferences:
    """The service for the router to attach to each View."""
    return _prefs


def _coerce(default: object, value: object) -> object | None:
    """Accept `value` only if its type matches the type of `default`.

    Watch out: in Python `bool` is a subclass of `int`, so `True` would
    pass as an `int` if we didn't check bool first.
    """
    if isinstance(default, bool):
        return value if isinstance(value, bool) else None
    if isinstance(default, int):
        return value if isinstance(value, int) and not isinstance(value, bool) else None
    if isinstance(default, float):
        return float(value) if isinstance(value, (int, float)) and not isinstance(value, bool) else None
    if isinstance(default, str):
        return value if isinstance(value, str) else None
    return None


async def load() -> dict[str, object]:
    """Read every setting from disk into `_cache`. Call it once."""
    global _loaded
    for key, default in DEFAULTS.items():
        try:
            raw = await _prefs.get(PREFIX + key)
        except Exception:
            raw = None
        clean = _coerce(default, raw) if raw is not None else None
        _cache[key] = default if clean is None else clean
    _loaded = True
    return dict(_cache)


def is_loaded() -> bool:
    return _loaded


def get(key: str) -> object:
    """Read a setting — synchronous, from memory."""
    return _cache.get(key, DEFAULTS.get(key))


def get_bool(key: str) -> bool:
    return bool(get(key))


def get_str(key: str) -> str:
    return str(get(key))


def get_int(key: str) -> int:
    return int(get(key))         # type: ignore[arg-type]


def get_float(key: str) -> float:
    return float(get(key))       # type: ignore[arg-type]


async def set(key: str, value: object) -> bool:
    """Change a setting: memory right away, disk after.

    Returns True if the save succeeded. Even if it fails, `_cache`
    already has the new value — the screen will never appear stuck.
    """
    if key not in DEFAULTS:
        raise KeyError(f"Unknown setting: {key}")
    _cache[key] = value
    try:
        return bool(await _prefs.set(PREFIX + key, value))  # type: ignore[arg-type]
    except Exception:
        return False


async def reset() -> bool:
    """Reset all settings back to their default values.

    Returns True if disk was cleared without problems. `remove()`
    returns False when the key never existed — that's NOT a failure,
    it's a setting the person never changed. Only an exception counts
    as a failure.
    """
    _cache.update(DEFAULTS)
    ok = True
    for key in DEFAULTS:
        try:
            await _prefs.remove(PREFIX + key)
        except Exception:
            ok = False
    return ok


# ── Hantalk-specific helpers ────────────────────────────────

def active_phonetic_count() -> int:
    """How many phonetic systems are currently on."""
    return sum(1 for k in PHONETIC_KEYS if get_bool(k))


def can_turn_off(key: str) -> bool:
    """A phonetic system can't be turned off if it's the last one left.

    Without this, the user could turn everything off and lessons would
    appear empty.
    """
    if key not in PHONETIC_KEYS:
        return True
    return not (get_bool(key) and active_phonetic_count() <= 1)
