# Copyright (c) 2026 Wilkend. All rights reserved.
# Hantalk - proprietary software. See LICENSE at the repository root.
# Unauthorized copying, modification, or redistribution is prohibited.

import datetime

import flet as ft

from app import theme
from app.screen import safe_top
from services import settings_service as settings

APP_VERSION = "1.0.0"

# ══════════════════════════════════════════════
# Tèks — yon sèl kote pou tradiksyon pita
# ══════════════════════════════════════════════

L = {
    "title": "Settings",

    "sec_profile": "PROFILE",
    "sec_learning": "LEARNING",
    "sec_notifications": "NOTIFICATIONS",
    "sec_appearance": "APPEARANCE",
    "sec_account": "ACCOUNT",

    "edit_profile": "Edit profile",

    "phonetic": "Phonetic systems",
    "phonetic_sub": "Shown under every line of a lesson",
    "phonetic_min": "Keep at least one phonetic system on",

    "audio_speed": "Audio speed",
    "audio_speed_sub": "How fast dialogue lines are read",

    "goal": "Daily goal",

    "notify_daily": "Daily reminder",
    "notify_time": "Reminder time",
    "notify_streak": "Streak reminder",
    "notify_streak_sub": "Warn me when my streak is about to end",
    "notify_weekly": "Weekly summary",

    "theme": "Theme",
    "theme_sub": "Dark palette is not built yet — the choice is saved",
    "zh_size": "Character size",
    "zh_size_sub": "Size of Chinese characters in lessons",
    "sound": "Sound effects",

    "name": "Name",
    "email": "Email",
    "password": "Change password",

    "log_out": "Log out",
    "reset": "Reset settings",

    "logout_title": "Log out?",
    "logout_body": "Your progress is saved on this device. It will be here "
                   "when you log back in.",
    "logout_ok": "Log out",

    "reset_title": "Reset settings?",
    "reset_body": "Every setting on this screen goes back to its starting "
                  "value. Your lessons and streak are not touched.",
    "reset_ok": "Reset settings",
    "reset_done": "Settings are back to their starting values.",

    "cancel": "Cancel",
    "not_built": "That screen is not built yet.",
    "save_failed": "That setting did not save. Check your connection and "
                   "try again.",
    "notify_blocked": "Notifications are turned off for Hantalk",
    "notify_blocked_action": "Open system settings",
}

LEGAL_LINKS = (
    ("Terms", "/legal/terms"),
    ("Privacy", "/legal/privacy"),
    ("Acknowledgements", "/legal/acknowledgements"),
)

NOT_BUILT_ROUTES = frozenset({
    "/account/password",
    "/legal/terms",
    "/legal/privacy",
    "/legal/acknowledgements",
})

PHONETIC_LABELS = (
    ("phonetic_hanzi", "漢字"),
    ("phonetic_bopomofo", "ㄅㄆㄇ"),
    ("phonetic_tongyong", "Tongyong"),
    ("phonetic_pinyin", "Pinyin"),
)

GOAL_CHOICES = (
    (5, "Casual"),
    (10, "Regular"),
    (15, "Serious"),
    (20, "Intense"),
)

THEME_CHOICES = (("light", "Light"), ("dark", "Dark"), ("system", "System"))
SPEED_CHOICES = (("normal", "Normal"), ("slow", "Slow"))

TAP_MIN = 44  


def _mounted(control) -> bool:

    try:
        return control.page is not None
    except RuntimeError:
        return False


def _update(*controls) -> None:
   
    for control in controls:
        if _mounted(control):
            control.update()

def _section_label(text: str) -> ft.Control:
    return ft.Container(
        padding=ft.Padding.only(left=4, bottom=8, top=22),
        content=ft.Text(
            text,
            size=theme.SIZE_LABEL,
            weight=ft.FontWeight.W_600,
            color=theme.TEXT_MUTED,
        ),
    )


def _card(rows: list[ft.Control]) -> ft.Control:
    stacked: list[ft.Control] = []
    for i, row in enumerate(rows):
        if i:
            stacked.append(
                ft.Container(
                    height=1,
                    bgcolor=theme.DIVIDER,
                    margin=ft.Margin.only(left=16),
                )
            )
        stacked.append(row)

    return ft.Container(
        bgcolor=theme.SURFACE,
        border=ft.Border.all(1, theme.OUTLINE),
        border_radius=theme.RADIUS_LG,
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,  
        content=ft.Column(spacing=0, controls=stacked),
    )


def _row(title: str, trailing: ft.Control, subtitle: str | None = None,
         on_click=None) -> ft.Control:
    left: list[ft.Control] = [
        ft.Text(title, size=theme.SIZE_BODY, weight=ft.FontWeight.W_500,
                color=theme.TEXT)
    ]
    if subtitle:
        left.append(
            ft.Text(subtitle, size=theme.SIZE_SMALL, color=theme.TEXT_MUTED)
        )

    return ft.Container(
        padding=ft.Padding.symmetric(vertical=14, horizontal=16),
        on_click=on_click,
        ink=bool(on_click),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Column(spacing=2, expand=True, controls=left),
                trailing,
            ],
        ),
    )


def _stacked_row(title: str, control: ft.Control,
                 subtitle: ft.Control | str | None = None) -> ft.Control:
    """Ranje kote kontwòl la twò laj pou l chita akote tit la.

    `subtitle` ka yon `ft.Text` vivan — konsa nou ka chanje l pita san
    nou pa rekreye ranje a.
    """
    head: list[ft.Control] = [
        ft.Text(title, size=theme.SIZE_BODY, weight=ft.FontWeight.W_500,
                color=theme.TEXT)
    ]
    if isinstance(subtitle, str):
        head.append(
            ft.Text(subtitle, size=theme.SIZE_SMALL, color=theme.TEXT_MUTED)
        )
    elif subtitle is not None:
        head.append(subtitle)
    head.append(ft.Container(height=8))
    head.append(control)

    return ft.Container(
        padding=ft.Padding.symmetric(vertical=14, horizontal=16),
        content=ft.Column(spacing=2, controls=head),
    )


def _chevron() -> ft.Control:
    return ft.Icon(ft.Icons.CHEVRON_RIGHT, size=20, color=theme.TEXT_MUTED)


def _wide_button(label: str, on_click, danger: bool = False) -> ft.Control:
    color = theme.ERROR_TEXT if danger else theme.TEXT_SECONDARY
    return ft.Container(
        height=50,
        border_radius=theme.RADIUS_SM,
        border=ft.Border.all(1, theme.ERROR if danger else theme.OUTLINE),
        bgcolor=theme.SURFACE,
        alignment=ft.Alignment.CENTER,
        on_click=on_click,
        ink=True,
        content=ft.Text(label, size=theme.SIZE_SMALL,
                        weight=ft.FontWeight.W_700, color=color),
    )


class _Pill:
    

    def __init__(self, label: str, on_select, selected: bool = False,
                 enabled: bool = True, on_blocked=None):
        self._on_select = on_select
        self._on_blocked = on_blocked
        self._enabled = enabled
        self.label = ft.Text(label, size=theme.SIZE_SMALL,
                             weight=ft.FontWeight.W_600)
        self.box = ft.Container(
            height=TAP_MIN,
            padding=ft.Padding.symmetric(horizontal=16),
            border_radius=theme.RADIUS_SM,
            alignment=ft.Alignment.CENTER,
            ink=True,
            animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
            animate_opacity=150,
            on_click=self._click,
            content=self.label,
        )
        self.set_state(selected, enabled)

    def _click(self, e) -> None:
        if self._enabled:
            self._on_select()
        elif self._on_blocked:
            self._on_blocked()

    def set_state(self, selected: bool, enabled: bool = True,
                  disabled_hint: str | None = None) -> None:
        self._enabled = enabled
        self.box.bgcolor = theme.PRIMARY_CONTAINER if selected else theme.BACKGROUND
        self.box.border = ft.Border.all(
            1, theme.PRIMARY if selected else theme.OUTLINE
        )
        self.box.opacity = 1.0 if enabled else 0.45
        self.box.tooltip = None if enabled else disabled_hint
        self.label.color = (
            theme.ON_PRIMARY_DEEP if selected else theme.TEXT_SECONDARY
        )
        _update(self.box)


class _Segmented:

    def __init__(self, choices, current: str, on_select):
        self._parts: dict[str, tuple[ft.Container, ft.Text]] = {}
        segments: list[ft.Control] = []

        for value, label in choices:
            text = ft.Text(label, size=theme.SIZE_SMALL)
            box = ft.Container(
                expand=True,
                height=38,
                border_radius=theme.RADIUS_XS,
                alignment=ft.Alignment.CENTER,
                animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
                on_click=(lambda e, v=value: on_select(v)),
                content=text,
            )
            self._parts[value] = (box, text)
            segments.append(box)

        self.box = ft.Container(
            bgcolor=theme.DIVIDER,
            border_radius=theme.RADIUS_SM,
            padding=ft.Padding.all(3),
            content=ft.Row(spacing=3, controls=segments),
        )
        self.select(current)

    def select(self, current: str) -> None:
        for value, (box, text) in self._parts.items():
            on = value == current
            box.bgcolor = theme.SURFACE if on else ft.Colors.TRANSPARENT
            text.color = theme.PRIMARY if on else theme.TEXT_SECONDARY
            text.weight = ft.FontWeight.W_600 if on else ft.FontWeight.W_500
        _update(self.box)


class _SwitchRow:

    def __init__(self, title: str, value: bool, on_change,
                 subtitle: str | None = None):
        self._on_change = on_change
        self.switch = ft.Switch(
            value=value,
            active_color=theme.PRIMARY,
            on_change=lambda e: self._on_change(e.control.value),
        )
        self.control = _row(title, self.switch, subtitle,
                            on_click=self._row_tapped)

    def _row_tapped(self, e) -> None:
        self.switch.value = not self.switch.value
        _update(self.switch)
        self._on_change(self.switch.value)

    def set_value(self, value: bool) -> None:
        self.switch.value = value
        _update(self.switch)


class _NavRow:

    def __init__(self, title: str, value: str | None, on_click,
                 subtitle: str | None = None):
        self._on_click = on_click
        self._enabled = True

        self.title = ft.Text(title, size=theme.SIZE_BODY,
                             weight=ft.FontWeight.W_500, color=theme.TEXT)
        left: list[ft.Control] = [self.title]
        if subtitle:
            left.append(ft.Text(subtitle, size=theme.SIZE_SMALL,
                                color=theme.TEXT_MUTED))

        self.value = ft.Text(value or "", size=theme.SIZE_BODY,
                             color=theme.TEXT_MUTED)
        trailing = ft.Row(
            spacing=6,
            tight=True,
            controls=([self.value] if value is not None else []) + [_chevron()],
        )

        self.control = ft.Container(
            padding=ft.Padding.symmetric(vertical=14, horizontal=16),
            on_click=self._click,
            ink=True,
            animate_opacity=150,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Column(spacing=2, expand=True, controls=left),
                    trailing,
                ],
            ),
        )

    def _click(self, e) -> None:
        if self._enabled:
            self._on_click()

    def set_value(self, value: str) -> None:
        self.value.value = value
        _update(self.value)

    def set_enabled(self, enabled: bool) -> None:
        """Yon ranje ki depann yon switch etenn dwe GEN LÈ etenn."""
        self._enabled = enabled
        self.control.opacity = 1.0 if enabled else 0.4
        self.control.ink = enabled
        _update(self.control)


# ══════════════════════════════════════════════
# The screen
# ══════════════════════════════════════════════

def settings_view(page: ft.Page) -> ft.View:

    state: dict[str, object] = {
        "audio_speed": settings.get_str("audio_speed"),
        "daily_goal_min": settings.get_int("daily_goal_min"),
        "theme_mode": settings.get_str("theme_mode"),
        "notify_time": settings.get_str("notify_time"),
        "notify_daily": settings.get_bool("notify_daily"),
        "notify_streak": settings.get_bool("notify_streak"),
        "notify_weekly": settings.get_bool("notify_weekly"),
        "sound_effects": settings.get_bool("sound_effects"),
        "zh_text_scale": settings.get_float("zh_text_scale"),
    }
    for key, _ in PHONETIC_LABELS:
        state[key] = settings.get_bool(key)

    # ── zouti ────────────────────────────────

    def snack(message: str) -> None:
        page.show_dialog(
            ft.SnackBar(
                content=ft.Text(message, size=theme.SIZE_SMALL,
                                color=theme.DARK_TEXT),
                bgcolor=theme.DARK_SURFACE,
            )
        )

    def go_to(route: str) -> None:
    
        if route in NOT_BUILT_ROUTES:
            snack(L["not_built"])
            return

        async def push() -> None:
            await page.push_route(route)

        page.run_task(push)

    def save(key: str, value: object, rollback=None) -> None:
        previous = state.get(key)
        state[key] = value

        async def run():
            try:
                saved = await settings.set(key, value)
            except Exception:
                saved = False
            if saved:
                return
            state[key] = previous
            if rollback:
                rollback(previous)
            snack(L["save_failed"])

        page.run_task(run)

    # ── Profile section ──────────────────────
    def profile_card() -> ft.Control:
        
        display_name = "Wilkend"
        email = "wilkend9@gmail.com"

        avatar = ft.Container(
            width=52,
            height=52,
            border_radius=999,
            bgcolor=theme.PRIMARY_CONTAINER,
            alignment=ft.Alignment.CENTER,
            content=ft.Text(display_name[:1].upper(), size=theme.SIZE_H3,
                            weight=ft.FontWeight.W_700,
                            color=theme.ON_PRIMARY_DEEP),
        )

        return ft.Container(
            bgcolor=theme.SURFACE,
            border=ft.Border.all(1, theme.OUTLINE),
            border_radius=theme.RADIUS_LG,
            padding=ft.Padding.symmetric(vertical=14, horizontal=16),
            ink=True,
            on_click=lambda e: go_to("/profile"),
            content=ft.Row(
                spacing=14,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    avatar,
                    ft.Column(
                        spacing=2,
                        expand=True,
                        controls=[
                            ft.Text(display_name, size=theme.SIZE_H3,
                                    weight=ft.FontWeight.W_700,
                                    color=theme.TEXT),
                            ft.Text(email, size=theme.SIZE_SMALL,
                                    color=theme.TEXT_MUTED),
                        ],
                    ),
                    _chevron(),
                ],
            ),
        )

    # ── Learning section ───────────

    phonetic_pills: dict[str, _Pill] = {}

    def refresh_phonetic() -> None:
        on_count = sum(1 for key, _ in PHONETIC_LABELS if state[key])
        for key, pill in phonetic_pills.items():
            selected = bool(state[key])
            can_turn_off = not selected or on_count > 1
            pill.set_state(selected, enabled=can_turn_off,
                           disabled_hint=L["phonetic_min"])

    def toggle_phonetic(key: str) -> None:
        save(key, not state[key],
             rollback=lambda _v: refresh_phonetic())
        refresh_phonetic()

    for key, label in PHONETIC_LABELS:
        phonetic_pills[key] = _Pill(
            label,
            (lambda k=key: toggle_phonetic(k)),
            selected=bool(state[key]),
            on_blocked=lambda: snack(L["phonetic_min"]),
        )
    refresh_phonetic()

    speed = _Segmented(
        SPEED_CHOICES, str(state["audio_speed"]),
        lambda v: (save("audio_speed", v,
                        rollback=lambda old: speed.select(str(old))),
                   speed.select(v)),
    )

    goal_pills: dict[int, _Pill] = {}
    goal_caption = ft.Text(size=theme.SIZE_SMALL, color=theme.TEXT_MUTED)

    def refresh_goal() -> None:
        current = state["daily_goal_min"]
        for minutes, pill in goal_pills.items():
            pill.set_state(minutes == current)
        goal_caption.value = f"{current} minutes a day"
        _update(goal_caption)

    def choose_goal(minutes: int) -> None:
        save("daily_goal_min", minutes, rollback=lambda _v: refresh_goal())
        refresh_goal()

    for minutes, name in GOAL_CHOICES:
        goal_pills[minutes] = _Pill(name, (lambda m=minutes: choose_goal(m)))
    refresh_goal()

    learning_card = _card([
        _stacked_row(
            L["phonetic"],
            ft.Row(spacing=8, wrap=True,
                   controls=[p.box for p in phonetic_pills.values()]),
            L["phonetic_sub"],
        ),
        _stacked_row(L["audio_speed"], speed.box, L["audio_speed_sub"]),
        _stacked_row(
            L["goal"],
            ft.Row(spacing=8, wrap=True,
                   controls=[p.box for p in goal_pills.values()]),
            goal_caption,
        ),
    ])

    # ── Notification section ────────────────

    def pick_time() -> None:
        raw = str(state["notify_time"])
        try:
            hour, minute = (int(x) for x in raw.split(":"))
        except ValueError:
            hour, minute = 20, 0

        def on_change(ev):
            value = ev.control.value
            if value is None:
                return
            formatted = f"{value.hour:02d}:{value.minute:02d}"
            time_row.set_value(formatted)
            save("notify_time", formatted,
                 rollback=lambda old: time_row.set_value(str(old)))

        page.show_dialog(
            ft.TimePicker(value=datetime.time(hour, minute),
                          on_change=on_change)
        )

    time_row = _NavRow(L["notify_time"], str(state["notify_time"]), pick_time)

    def set_daily(value: bool) -> None:
        
        time_row.set_enabled(value)
        save("notify_daily", value,
             rollback=lambda old: (daily_row.set_value(bool(old)),
                                   time_row.set_enabled(bool(old))))

    daily_row = _SwitchRow(L["notify_daily"], bool(state["notify_daily"]),
                           set_daily)
    time_row.set_enabled(bool(state["notify_daily"]))

    streak_row = _SwitchRow(
        L["notify_streak"], bool(state["notify_streak"]),
        lambda v: save("notify_streak", v,
                       rollback=lambda old: streak_row.set_value(bool(old))),
        L["notify_streak_sub"],
    )
    weekly_row = _SwitchRow(
        L["notify_weekly"], bool(state["notify_weekly"]),
        lambda v: save("notify_weekly", v,
                       rollback=lambda old: weekly_row.set_value(bool(old))),
    )

    notifications_card = _card([
        daily_row.control,
        time_row.control,
        streak_row.control,
        weekly_row.control,
    ])

    # ── Appearance section ──────────

    theme_seg = _Segmented(
        THEME_CHOICES, str(state["theme_mode"]),
        lambda v: (save("theme_mode", v,
                        rollback=lambda old: theme_seg.select(str(old))),
                   theme_seg.select(v)),
    )

    scale0 = float(state["zh_text_scale"])
    zh_preview = ft.Text("你好", font_family=theme.FONT_ZH_SERIF,
                         size=int(theme.SIZE_ZH * scale0), color=theme.TEXT)
    zh_pct = ft.Text(f"{int(scale0 * 100)}%", size=theme.SIZE_SMALL,
                     color=theme.TEXT_MUTED)

    def on_scale_drag(e):
        
        value = round(float(e.control.value), 2)
        zh_preview.size = int(theme.SIZE_ZH * value)
        zh_pct.value = f"{int(value * 100)}%"
        _update(zh_preview, zh_pct)

    def set_scale(value) -> None:
        """Mete slider la ak apèsi li a sou yon valè — san ekri anyen."""
        value = float(value)
        zh_slider.value = value
        zh_preview.size = int(theme.SIZE_ZH * value)
        zh_pct.value = f"{int(value * 100)}%"
        _update(zh_slider, zh_preview, zh_pct)

    def on_scale_end(e):
        value = round(float(e.control.value), 2)
        save("zh_text_scale", value, rollback=set_scale)

    zh_slider = ft.Slider(
        min=0.8, max=1.4, divisions=6, value=scale0,
        active_color=theme.PRIMARY,
        inactive_color=theme.DIVIDER,
        on_change=on_scale_drag,
        on_change_end=on_scale_end,
    )

    sound_row = _SwitchRow(
        L["sound"], bool(state["sound_effects"]),
        lambda v: save("sound_effects", v,
                       rollback=lambda old: sound_row.set_value(bool(old))),
    )

    appearance_card = _card([
        _stacked_row(L["theme"], theme_seg.box, L["theme_sub"]),
        _stacked_row(
            L["zh_size"],
            ft.Column(spacing=0, controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[zh_preview, zh_pct],
                ),
                zh_slider,
            ]),
            L["zh_size_sub"],
        ),
        sound_row.control,
    ])

    # ── Account section ────────────────

    def confirm(title: str, message: str, action_label: str, on_confirm,
                danger: bool = False) -> None:
        def close(e=None):
            page.pop_dialog()

        def go(e):
            page.pop_dialog()
            on_confirm()

        page.show_dialog(
            ft.AlertDialog(
                modal=True,
                bgcolor=theme.SURFACE,
                shape=ft.RoundedRectangleBorder(radius=theme.RADIUS_LG),
                title=ft.Text(title, size=theme.SIZE_H3,
                              weight=ft.FontWeight.W_700, color=theme.TEXT),
                content=ft.Text(message, size=theme.SIZE_BODY,
                                color=theme.TEXT_SECONDARY),
                actions=[
                    ft.TextButton(
                        L["cancel"], on_click=close,
                        style=ft.ButtonStyle(color=theme.TEXT_SECONDARY),
                    ),
                    ft.TextButton(
                        action_label, on_click=go,
                        style=ft.ButtonStyle(
                            color=theme.ERROR_TEXT if danger else theme.PRIMARY
                        ),
                    ),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
        )

    async def do_logout() -> None:
    
        await page.push_route("/login")

    def ask_logout(e) -> None:
        confirm(L["logout_title"], L["logout_body"], L["logout_ok"],
                lambda: page.run_task(do_logout))

    def reload_state() -> None:
        
        for key in state:
            state[key] = settings.get(key)

        refresh_phonetic()
        speed.select(str(state["audio_speed"]))
        refresh_goal()
        daily_row.set_value(bool(state["notify_daily"]))
        time_row.set_value(str(state["notify_time"]))
        time_row.set_enabled(bool(state["notify_daily"]))
        streak_row.set_value(bool(state["notify_streak"]))
        weekly_row.set_value(bool(state["notify_weekly"]))
        theme_seg.select(str(state["theme_mode"]))
        set_scale(state["zh_text_scale"])
        sound_row.set_value(bool(state["sound_effects"]))

    def do_reset() -> None:
        async def run():
            try:
                ok = await settings.reset()
            except Exception:
                ok = False
            reload_state()
            snack(L["reset_done"] if ok else L["save_failed"])

        page.run_task(run)

    def ask_reset(e) -> None:
        confirm(L["reset_title"], L["reset_body"], L["reset_ok"], do_reset,
                danger=True)

    account_card = _card([
        _NavRow(L["password"], None,
                lambda: go_to("/account/password")).control,
    ])

    # ── Footer────────

    def footer() -> ft.Control:
        links = ft.Row(
            spacing=18,
            wrap=True,
            controls=[
                ft.Container(
                    on_click=(lambda e, r=route: go_to(r)),
                    padding=ft.Padding.symmetric(vertical=8),
                    content=ft.Text(label, size=theme.SIZE_LABEL,
                                    weight=ft.FontWeight.W_700,
                                    color=theme.PRIMARY),
                )
                for label, route in LEGAL_LINKS
            ],
        )
        return ft.Container(
            padding=ft.Padding.only(top=20, bottom=40, left=4),
            content=ft.Column(
                spacing=6,
                controls=[
                    links,
                    ft.Text(f"Hantalk {APP_VERSION}", size=theme.SIZE_LABEL,
                            color=theme.TEXT_MUTED),
                ],
            ),
        )

    # ── Body ──────────────

    body = ft.Column(
        expand=True,
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
        scroll_interval=80,
        controls=[
            _section_label(L["sec_profile"]),
            profile_card(),
            _section_label(L["sec_learning"]),
            learning_card,
            _section_label(L["sec_notifications"]),
            notifications_card,
            _section_label(L["sec_appearance"]),
            appearance_card,
            _section_label(L["sec_account"]),
            account_card,
            ft.Container(height=18),
            _wide_button(L["log_out"], ask_logout),
            ft.Container(height=10),
            _wide_button(L["reset"], ask_reset, danger=True),
            footer(),
        ],
    )

    # ── Header ──────

    header = ft.Container(
        bgcolor=theme.SURFACE,
        border=ft.Border.only(bottom=ft.BorderSide(1, ft.Colors.TRANSPARENT)),
        padding=ft.Padding.only(left=8, right=20, top=14, bottom=14),
        animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
        content=ft.Row(
            spacing=4,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    padding=ft.Padding.all(8),
                    border_radius=999,
                    ink=True,
                    on_click=lambda e: go_to("/home"),
                    content=ft.Icon(ft.Icons.ARROW_BACK, size=24,
                                    color=theme.TEXT),
                ),
                ft.Text(L["title"], size=theme.SIZE_H2,
                        weight=ft.FontWeight.W_600, color=theme.TEXT),
            ],
        ),
    )

    _header_lifted = False

    def on_body_scroll(e) -> None:
        """Liy anba ankadreman an parèt sèlman lè kontni an pase anba l."""
        nonlocal _header_lifted
        lifted = (e.pixels or 0) > 4
        if lifted == _header_lifted:
            return
        _header_lifted = lifted
        header.border = ft.Border.only(
            bottom=ft.BorderSide(
                1, theme.OUTLINE if lifted else ft.Colors.TRANSPARENT
            )
        )
        _update(header)

    body.on_scroll = on_body_scroll

    return ft.View(
        route="/settings",
        padding=0,
        spacing=0,
        bgcolor=theme.BACKGROUND,
        controls=[
            safe_top(header),
            ft.Container(
                expand=True,
                padding=ft.Padding.symmetric(horizontal=theme.PAD_PAGE),
                content=body,
            ),
        ],
    )