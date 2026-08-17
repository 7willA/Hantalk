# Copyright (c) 2026 Wilkend. All rights reserved.
# Hantalk - proprietary software. See LICENSE at the repository root.
# Unauthorized copying, modification, or redistribution is prohibited.

"""Settings view — ekran /settings la.

Flutter counterpart: lib/screens/settings/settings_screen.dart

DESIZYON DESIGN (soti nan analiz ekran Duolingo a)

  Nou pran nan Duolingo:
    - gwoup ranje nan yon kat awondi, ak yon liy 1px ant ranje yo
    - ti etikèt seksyon ETENN ki chita DEYÒ kat la
    - bouton dekonekte ak bòdi, plen lajè, izole anba
    - lyen legal MAJISKIL nan pye paj la

  Nou PA pran nesting lan. Duolingo voye chak ranje sou yon lòt ekran
  paske li gen plizyè santèn paramèt. Hantalk gen 13. Si nou te kopye
  sa, nou t ap gen 4 ekran ak 3 switch chak, epi 2 tap pou chanje
  vitès odyo. Donk kontwòl yo chita DIRÈKTMAN nan ranje a.

  Chevron `>` rete sèlman kote ki gen vrèman yon lòt kote pou ale.
"""

import datetime

import flet as ft

from app import theme
from services import settings_service as settings

LEGAL_LINKS = ("TÈM", "KONFIDANSYALITE", "SOU HANTALK")

PHONETIC_LABELS = (
    ("phonetic_hanzi", "漢字"),
    ("phonetic_bopomofo", "ㄅㄆㄇ"),
    ("phonetic_tongyong", "Tongyong"),
    ("phonetic_pinyin", "Pinyin"),
)

GOAL_CHOICES = (5, 10, 15, 20)
THEME_CHOICES = (("light", "Klè"), ("dark", "Fonse"), ("system", "Sistèm"))
SPEED_CHOICES = (("normal", "Normal"), ("slow", "Slow"))


# ══════════════════════════════════════════════
# Ti moso ki repete
# ══════════════════════════════════════════════

def _section_label(text: str) -> ft.Control:
    """Etikèt ETENN ki chita deyò kat la (modèl Duolingo)."""
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
    """Gwoup ranje: yon kat, yon liy 1px ant chak ranje."""
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
        content=ft.Column(spacing=0, controls=stacked),
    )


def _row(title: str, trailing: ft.Control, subtitle: str | None = None,
         on_click=None) -> ft.Control:
    """Yon ranje: tit (+ sou-tit) agoch, kontwòl la adwat."""
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
                 subtitle: str | None = None) -> ft.Control:
    """Ranje kote kontwòl la twò laj pou l chita akote tit la."""
    head: list[ft.Control] = [
        ft.Text(title, size=theme.SIZE_BODY, weight=ft.FontWeight.W_500,
                color=theme.TEXT)
    ]
    if subtitle:
        head.append(
            ft.Text(subtitle, size=theme.SIZE_SMALL, color=theme.TEXT_MUTED)
        )
    head.append(ft.Container(height=4))
    head.append(control)

    return ft.Container(
        padding=ft.Padding.symmetric(vertical=14, horizontal=16),
        content=ft.Column(spacing=2, controls=head),
    )


def _chevron() -> ft.Control:
    return ft.Icon(ft.Icons.CHEVRON_RIGHT, size=20, color=theme.TEXT_MUTED)


def _value_and_chevron(value: str) -> ft.Control:
    return ft.Row(
        spacing=6,
        tight=True,
        controls=[
            ft.Text(value, size=theme.SIZE_BODY, color=theme.TEXT_MUTED),
            _chevron(),
        ],
    )


def _pill(label: str, on: bool, on_click) -> ft.Control:
    """Ti bouton chwa (sistèm fonetik, objektif jounalye)."""
    return ft.Container(
        height=36,
        padding=ft.Padding.symmetric(horizontal=14),
        border_radius=theme.RADIUS_SM,
        alignment=ft.Alignment.CENTER,
        on_click=on_click,
        bgcolor=theme.PRIMARY_CONTAINER if on else theme.BACKGROUND,
        border=ft.Border.all(
            1, theme.PRIMARY if on else theme.OUTLINE
        ),
        content=ft.Text(
            label,
            size=theme.SIZE_SMALL,
            weight=ft.FontWeight.W_600,
            color=theme.ON_PRIMARY_DEEP if on else theme.TEXT_SECONDARY,
        ),
    )


def _segmented(choices, current: str, on_select) -> ft.Control:
    """Segmented button: yon track etenn ak yon sèl moso ki allime."""
    segs = []
    for value, label in choices:
        on = value == current
        segs.append(
            ft.Container(
                expand=True,
                height=32,
                border_radius=theme.RADIUS_XS,
                alignment=ft.Alignment.CENTER,
                bgcolor=theme.SURFACE if on else ft.Colors.TRANSPARENT,
                on_click=(lambda e, v=value: on_select(v)),
                content=ft.Text(
                    label,
                    size=theme.SIZE_SMALL,
                    weight=ft.FontWeight.W_600 if on else ft.FontWeight.W_500,
                    color=theme.PRIMARY if on else theme.TEXT_SECONDARY,
                ),
            )
        )
    return ft.Container(
        bgcolor=theme.DIVIDER,
        border_radius=theme.RADIUS_SM,
        padding=ft.Padding.all(3),
        content=ft.Row(spacing=3, controls=segs),
    )


def _wide_button(label: str, on_click, danger: bool = False) -> ft.Control:
    """Bouton plen lajè ak bòdi — modèl SIGN OUT Duolingo a."""
    color = theme.ERROR_TEXT if danger else theme.TEXT_SECONDARY
    return ft.Container(
        height=50,
        border_radius=theme.RADIUS_SM,
        border=ft.Border.all(1, theme.ERROR if danger else theme.OUTLINE),
        bgcolor=theme.SURFACE,
        alignment=ft.Alignment.CENTER,
        on_click=on_click,
        content=ft.Text(label, size=theme.SIZE_SMALL,
                        weight=ft.FontWeight.W_700, color=color),
    )


# ══════════════════════════════════════════════
# Ekran an
# ══════════════════════════════════════════════

def settings_view(page: ft.Page) -> ft.View:
    body = ft.Column(
        expand=True,
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
    )

    # ── zouti ────────────────────────────────

    def save(key: str, value: object) -> None:
        """Sove yon paramèt san bloke ekran an."""
        async def run():
            await settings.set(key, value)
        page.run_task(run)

    def snack(message: str) -> None:
        page.show_dialog(
            ft.SnackBar(
                content=ft.Text(message, size=theme.SIZE_SMALL,
                                color=theme.DARK_TEXT),
                bgcolor=theme.DARK_SURFACE,
            )
        )

    def toggle(key: str) -> None:
        current = settings.get_bool(key)
        if current and not settings.can_turn_off(key):
            snack("Omwen yon sistèm fonetik dwe rete allime.")
            return
        save(key, not current)
        rebuild()
        page.update()

    def choose(key: str, value: object) -> None:
        """Pou kontwòl nou desine tèt nou (pill, segmented) — bezwen redesine."""
        save(key, value)
        rebuild()
        page.update()

    def save_only(key: str, value: object) -> None:
        """Pou kontwòl Flet ki desine pwòp eta yo (Switch).

        POUKISA nou PA redesine isit la: `rebuild()` ta detwi Switch la nan
        mitan pwòp evènman `on_change` li a epi ranplase l ak yon lòt. Sa
        se yon fason klasik pou fè Flet tonbe. Switch la deja montre nouvo
        eta li — nou jis bezwen sove l.
        """
        save(key, value)

    # ── kontwòl ki dwe SIVI (pa ranplase) ────
    #
    # Slider la ak apèsi li a viv DEYÒ `rebuild()`. Si nou te rekreye yo
    # nan chak `on_change`, Flet t ap detwi slider la pandan dwèt la
    # ap trennen sou li. Isit la nou chanje pwopriyete yo sou plas.

    _scale0 = settings.get_float("zh_text_scale")

    zh_preview = ft.Text("你好", font_family=theme.FONT_ZH_SERIF,
                         size=int(theme.SIZE_ZH * _scale0), color=theme.TEXT)
    zh_pct = ft.Text(f"{int(_scale0 * 100)}%", size=theme.SIZE_SMALL,
                     color=theme.TEXT_MUTED)

    def on_scale(e):
        value = round(float(e.control.value), 2)
        zh_preview.size = int(theme.SIZE_ZH * value)
        zh_pct.value = f"{int(value * 100)}%"
        save("zh_text_scale", value)
        page.update()

    zh_slider = ft.Slider(
        min=0.8, max=1.4, divisions=6, value=_scale0,
        active_color=theme.PRIMARY,
        inactive_color=theme.DIVIDER,
        on_change=on_scale,
    )

    # ── dyalog ───────────────────────────────

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
                        "Anile", on_click=close,
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

    def pick_time(e=None) -> None:
        raw = settings.get_str("notify_time")
        try:
            hour, minute = (int(x) for x in raw.split(":"))
        except ValueError:
            hour, minute = 20, 0

        def on_change(ev):
            value = ev.control.value
            if value is None:
                return
            save("notify_time", f"{value.hour:02d}:{value.minute:02d}")
            rebuild()
            page.update()

        page.show_dialog(
            ft.TimePicker(
                value=datetime.time(hour, minute),
                on_change=on_change,
            )
        )

    def do_reset_progress() -> None:
        async def run():
            await settings.reset()
        page.run_task(run)
        rebuild()
        page.update()
        snack("Tout pwogrè ak paramèt yo tounen nan valè pa defo.")

    async def do_logout() -> None:
        await page.push_route("/login")

    def ask_logout(e) -> None:
        confirm(
            "Dekonekte?",
            "Pwogrè ou sove sou aparèy la. W ap jwenn li lè w rekonekte.",
            "Dekonekte",
            lambda: page.run_task(do_logout),
        )

    def ask_reset(e) -> None:
        confirm(
            "Efase tout pwogrè?",
            "Tout leson, streak, XP ak paramèt ou yo ap disparèt nèt. "
            "Aksyon sa a pa ka defèt.",
            "Efase tout",
            do_reset_progress,
            danger=True,
        )

    # ── seksyon yo ───────────────────────────

    def learning_section() -> list[ft.Control]:
        chips = ft.Row(
            spacing=8,
            wrap=True,
            controls=[
                _pill(label, settings.get_bool(key),
                      (lambda e, k=key: toggle(k)))
                for key, label in PHONETIC_LABELS
            ],
        )
        goals = ft.Row(
            spacing=8,
            controls=[
                _pill(f"{m} min", settings.get_int("daily_goal_min") == m,
                      (lambda e, v=m: choose("daily_goal_min", v)))
                for m in GOAL_CHOICES
            ],
        )
        return [
            _section_label("APRANTISAJ"),
            _card([
                _stacked_row(
                    "Sistèm fonetik", chips,
                    "Sa ki parèt anba karaktè yo nan tout leson yo",
                ),
                _stacked_row(
                    "Vitès odyo",
                    _segmented(SPEED_CHOICES,
                               settings.get_str("audio_speed"),
                               lambda v: choose("audio_speed", v)),
                ),
                _stacked_row(
                    "Objektif jounalye", goals,
                    "Konbyen minit ou vle etidye chak jou",
                ),
            ]),
        ]

    def notifications_section() -> list[ft.Control]:
        def sw(key: str) -> ft.Control:
            return ft.Switch(
                value=settings.get_bool(key),
                active_color=theme.PRIMARY,
                on_change=(lambda e, k=key: save_only(k, e.control.value)),
            )

        return [
            _section_label("NOTIFIKASYON"),
            _card([
                _row("Rapèl jounalye", sw("notify_daily")),
                _row("Lè rapèl la",
                     _value_and_chevron(settings.get_str("notify_time")),
                     on_click=pick_time),
                _row("Alèt streak an danje", sw("notify_streak"),
                     "Voye yon rapèl si streak la ap kase"),
                _row("Rezime chak semèn", sw("notify_weekly")),
            ]),
        ]

    def appearance_section() -> list[ft.Control]:
        preview = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[zh_preview, zh_pct],
        )

        return [
            _section_label("APARANS"),
            _card([
                _stacked_row(
                    "Tèm",
                    _segmented(THEME_CHOICES,
                               settings.get_str("theme_mode"),
                               lambda v: choose("theme_mode", v)),
                    "Chwa a sove; palèt fonse a poko bati",
                ),
                _stacked_row(
                    "Gwosè karaktè chinwa",
                    ft.Column(spacing=0, controls=[preview, zh_slider]),
                ),
                _row("Efè son",
                     ft.Switch(
                         value=settings.get_bool("sound_effects"),
                         active_color=theme.PRIMARY,
                         on_change=lambda e: save_only("sound_effects",
                                                       e.control.value),
                     )),
            ]),
        ]

    def account_section() -> list[ft.Control]:
        return [
            _section_label("KONT"),
            _card([
                _row("Non", _value_and_chevron("Wilkend")),
                _row("Email", _value_and_chevron("wilkend9@gmail.com")),
                _row("Chanje modpas", _chevron()),
            ]),
            ft.Container(height=18),
            _wide_button("DEKONEKTE", ask_logout),
            ft.Container(height=10),
            _wide_button("EFASE TOUT PWOGRÈ", ask_reset, danger=True),
        ]

    def footer() -> ft.Control:
        return ft.Container(
            padding=ft.Padding.only(top=26, bottom=30, left=4),
            content=ft.Column(
                spacing=12,
                controls=[
                    ft.Text(label, size=theme.SIZE_LABEL,
                            weight=ft.FontWeight.W_700, color=theme.PRIMARY)
                    for label in LEGAL_LINKS
                ],
            ),
        )

    def rebuild() -> None:
        body.controls = [
            *learning_section(),
            *notifications_section(),
            *appearance_section(),
            *account_section(),
            footer(),
        ]

    rebuild()

    async def go_back(e):
        await page.push_route("/home")

    header = ft.Container(
        bgcolor=theme.SURFACE,
        border=ft.Border.only(bottom=ft.BorderSide(1, theme.OUTLINE)),
        padding=ft.Padding.only(left=8, right=20, top=14, bottom=14),
        content=ft.Row(
            spacing=4,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    padding=ft.Padding.all(8),
                    border_radius=999,
                    on_click=go_back,
                    content=ft.Icon(ft.Icons.ARROW_BACK, size=24,
                                    color=theme.TEXT),
                ),
                ft.Text("Settings", size=theme.SIZE_H2,
                        weight=ft.FontWeight.W_600, color=theme.TEXT),
            ],
        ),
    )

    return ft.View(
        route="/settings",
        padding=0,
        spacing=0,
        bgcolor=theme.BACKGROUND,
        controls=[
            header,
            ft.Container(
                expand=True,
                padding=ft.Padding.symmetric(horizontal=theme.PAD_PAGE),
                content=body,
            ),
        ],
    )
