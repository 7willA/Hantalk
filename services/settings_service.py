# Copyright (c) 2026 Wilkend. All rights reserved.
# Hantalk - proprietary software. See LICENSE at the repository root.
# Unauthorized copying, modification, or redistribution is prohibited.

"""Settings service — preferans itilizatè a, sove sou aparèy la.

Flutter counterpart: lib/services/settings_service.dart

KIJAN LI MACHE

  Flet 0.85 sèvi ak `ft.SharedPreferences`, ki se yon *Service*: fòk li
  atache sou yon View pou l viv (gade `app/router.py`). Metòd li yo tout
  se `async`.

  Men yon UI pa ka tann yon `await` chak fwa li bezwen konnen si Pinyin
  allime. Donk:

    - `load()`   li disk la YON SÈL fwa nan demaraj → ranpli `_cache`
    - `get()`    li `_cache` la — SINKWÒN, rapid, san `await`
    - `set()`    ekri nan `_cache` LA MENM, epi sove sou disk apre

  Konsa ekran an reponn imedyatman epi disk la swiv dèyè. Si sovgad la
  echwe (pa egzanp sou web san pèmisyon), app la kontinye mache ak
  valè ki nan memwa a — li p ap janm krache yon erè nan figi moun nan.
"""

import flet as ft

# Tout kle yo gen menm prefiks la pou yo pa antre nan wout lòt app.
PREFIX = "hantalk."

# Sous verite a pou chak paramèt: kle → valè pa defo.
# Tip valè a defini tip ki aksepte a (gade `_coerce`).
DEFAULTS: dict[str, object] = {
    # ── Aprantisaj ──
    "phonetic_hanzi": True,
    "phonetic_bopomofo": False,
    "phonetic_tongyong": False,
    "phonetic_pinyin": True,
    "audio_speed": "normal",        # "normal" | "slow"
    "daily_goal_min": 20,           # 5 | 10 | 15 | 20
    # ── Notifikasyon ──
    "notify_daily": True,
    "notify_time": "20:00",
    "notify_streak": True,
    "notify_weekly": False,
    # ── Aparans ──
    "theme_mode": "light",          # "light" | "dark" | "system"
    "zh_text_scale": 1.0,           # 0.8 → 1.4
    "sound_effects": True,
}

# Kle fonetik yo — nou bezwen yo ansanm pou règ "omwen youn allime" a.
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
    """Sèvis la pou router a atache sou chak View."""
    return _prefs


def _coerce(default: object, value: object) -> object | None:
    """Aksepte `value` sèlman si tip li matche ak tip `default` la.

    Atansyon: an Python `bool` se yon sou-klas `int`, donk `True` ta pase
    pou yon `int` si nou pa teste bool an premye.
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
    """Li tout paramèt yo sou disk la nan `_cache`. Rele l yon fwa."""
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
    """Li yon paramèt — sinkwòn, soti nan memwa."""
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
    """Chanje yon paramèt: memwa touswit, disk apre.

    Retounen True si sovgad la reyisi. Menm si li echwe, `_cache` la
    deja gen nouvo valè a — ekran an p ap janm parèt bloke.
    """
    if key not in DEFAULTS:
        raise KeyError(f"Paramèt enkoni: {key}")
    _cache[key] = value
    try:
        return bool(await _prefs.set(PREFIX + key, value))  # type: ignore[arg-type]
    except Exception:
        return False


async def reset() -> bool:
    """Retounen tout paramèt yo nan valè pa defo.

    Retounen True si disk la vide san pwoblèm. `remove()` bay False lè kle
    a pa t janm egziste — sa se PA yon echèk, se yon paramèt moun nan pa t
    janm chanje. Se sèlman yon eksepsyon ki konte kòm echèk.
    """
    _cache.update(DEFAULTS)
    ok = True
    for key in DEFAULTS:
        try:
            await _prefs.remove(PREFIX + key)
        except Exception:
            ok = False
    return ok


# ── Èd espesifik ak Hantalk ────────────────────────────────

def active_phonetic_count() -> int:
    """Konbyen sistèm fonetik ki allime kounye a."""
    return sum(1 for k in PHONETIC_KEYS if get_bool(k))


def can_turn_off(key: str) -> bool:
    """Yon sistèm fonetik pa ka etenn si se dènye a ki rete.

    San sa itilizatè a ta ka etenn tout bagay epi leson yo ta parèt vid.
    """
    if key not in PHONETIC_KEYS:
        return True
    return not (get_bool(key) and active_phonetic_count() <= 1)
