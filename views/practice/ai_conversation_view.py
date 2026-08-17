# Copyright (c) 2026 Wilkend. All rights reserved.
# Hantalk - proprietary software. See LICENSE at the repository root.
# Unauthorized copying, modification, or redistribution is prohibited.

"""AI conversation view — ekran 05 nan handoff la.

Tèm nwa, avatar pwofesè, badj LIVE, soutit, bouton mic.
DEMO: pa gen STT/TTS ni API. Bouton mic la jis chanje eta afichaj la.
"""

import flet as ft

from app import theme

SCENARIO = "Ordering food at a night market"
TEACHER = "Teacher Chen"

SUBS_TEACHER = {
    "label": "TEACHER SAID",
    "zh": "歡迎光臨！你想吃什麼？",
    "py": "huānyíng guānglín! nǐ xiǎng chī shénme?",
    "en": "Welcome! What would you like to eat?",
}
SUBS_USER = {
    "label": "YOU ARE SAYING",
    "zh": "我想要一份臭豆腐，謝謝。",
    "py": "wǒ xiǎng yào yí fèn chòudòufu, xièxie",
    "en": "I would like an order of stinky tofu, please.",
}


def ai_conversation_view(page: ft.Page) -> ft.View:
    state = {"mic": False}

    status = ft.Text(size=12, color=theme.AI_STATUS)
    sub_label = ft.Text(size=9, weight=ft.FontWeight.W_600,
                        color=theme.DARK_TEXT_MUTED)
    sub_zh = ft.Text(font_family=theme.FONT_ZH, size=27,
                     weight=ft.FontWeight.W_500, color=theme.DARK_TEXT)
    sub_py = ft.Text(size=14, color=theme.DARK_TEXT_MUTED)
    sub_en = ft.Text(size=13, color=theme.AI_TEXT_FAINT)
    mic_icon = ft.Icon(ft.Icons.MIC, size=40, color=theme.WHITE)
    mic_button = ft.Container(
        width=88, height=88, border_radius=999,
        alignment=ft.Alignment.CENTER,
    )
    bars = ft.Row(
        spacing=5,
        height=38,
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.END,
    )

    def rebuild():
        listening = state["mic"]
        subs = SUBS_USER if listening else SUBS_TEACHER

        status.value = ("Listening… speak now" if listening
                        else "Tap the mic to answer")
        sub_label.value = subs["label"]
        sub_zh.value = subs["zh"]
        sub_py.value = subs["py"]
        sub_en.value = subs["en"]

        mic_icon.icon = ft.Icons.STOP if listening else ft.Icons.MIC
        mic_button.bgcolor = (theme.AI_MIC_ACTIVE if listening
                              else theme.AI_MIC)
        mic_button.content = mic_icon

        heights = [10, 22, 34, 26, 34, 18, 12] if listening else [6] * 7
        bars.controls = [
            ft.Container(width=5, height=h, border_radius=3,
                         bgcolor=theme.AI_WAVE_ACTIVE if listening
                         else theme.AI_WAVE_IDLE)
            for h in heights
        ]

    def toggle_mic(e):
        state["mic"] = not state["mic"]
        rebuild()
        page.update()

    rebuild()

    async def close(e):
        await page.push_route("/home")

    def _pill(icon: str, text: str) -> ft.Control:
        return ft.Container(
            bgcolor=theme.AI_PILL_BG,
            border=ft.Border.all(1, theme.AI_PILL_BORDER),
            border_radius=20,
            padding=ft.Padding.symmetric(vertical=8, horizontal=13),
            content=ft.Row(
                spacing=7,
                tight=True,
                controls=[
                    ft.Icon(icon, size=17, color=theme.DARK_ACCENT),
                    ft.Text(text, size=12, weight=ft.FontWeight.W_500,
                            color=theme.WHITE),
                ],
            ),
        )

    def _round_icon(icon: str, on_click=None) -> ft.Control:
        return ft.Container(
            width=52, height=52, border_radius=999,
            bgcolor=theme.AI_ICON_BG,
            alignment=ft.Alignment.CENTER,
            on_click=on_click,
            content=ft.Icon(icon, size=24, color=theme.DARK_TEXT),
        )

    stage = ft.Container(
        height=534,
        bgcolor=theme.DARK_SURFACE,
        content=ft.Stack(
            expand=True,
            controls=[
                # avatar
                ft.Container(
                    alignment=ft.Alignment.CENTER,
                    content=ft.Container(
                        width=190, height=190, border_radius=999,
                        bgcolor=theme.AI_AVATAR_BG,
                        border=ft.Border.all(2, theme.AI_AVATAR_RING),
                        alignment=ft.Alignment.CENTER,
                        content=ft.Column(
                            spacing=12,
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Text("T",
                                        size=62, weight=ft.FontWeight.W_500,
                                        color=theme.DARK_ACCENT),
                                ft.Text("TEACHER AVATAR", size=9,
                                        color=theme.AI_AVATAR_CAPTION,
                                        text_align=ft.TextAlign.CENTER),
                            ],
                        ),
                    ),
                ),
                # top bar
                ft.Container(
                    top=18, left=16, right=16,
                    content=ft.Row(
                        spacing=8,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Container(
                                padding=ft.Padding.all(6),
                                border_radius=999,
                                on_click=close,
                                content=ft.Icon(ft.Icons.CLOSE, size=24,
                                                color=theme.WHITE),
                            ),
                            _pill(ft.Icons.STOREFRONT, SCENARIO),
                        ],
                    ),
                ),
                # LIVE badge
                ft.Container(
                    top=70, left=16,
                    bgcolor=theme.AI_LIVE,
                    border_radius=16,
                    padding=ft.Padding.symmetric(vertical=6, horizontal=11),
                    content=ft.Row(
                        spacing=7,
                        tight=True,
                        controls=[
                            ft.Container(width=7, height=7, border_radius=999,
                                         bgcolor=theme.WHITE),
                            ft.Text("LIVE · 02:14", size=11,
                                    weight=ft.FontWeight.W_600,
                                    color=theme.WHITE),
                        ],
                    ),
                ),
                # name + status
                ft.Container(
                    bottom=96, left=0, right=0,
                    content=ft.Column(
                        spacing=4,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text(TEACHER, size=15,
                                    weight=ft.FontWeight.W_500,
                                    color=theme.DARK_ACCENT),
                            status,
                        ],
                    ),
                ),
                ft.Container(bottom=34, left=0, right=0, content=bars),
            ],
        ),
    )

    subtitles = ft.Container(
        expand=True,
        padding=ft.Padding.only(left=20, right=20, top=20),
        content=ft.Column(
            spacing=12,
            controls=[
                ft.Row(
                    spacing=8,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        sub_label,
                        ft.Container(expand=True, height=1,
                                     bgcolor=theme.AI_DIVIDER),
                    ],
                ),
                ft.Column(
                    spacing=6,
                    controls=[sub_zh, sub_py, sub_en],
                ),
            ],
        ),
    )

    controls_row = ft.Container(
        padding=ft.Padding.only(left=20, right=20, top=12, bottom=26),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                _round_icon(ft.Icons.SUBTITLES),
                ft.Container(
                    width=88, height=88,
                    on_click=toggle_mic,
                    content=mic_button,
                ),
                _round_icon(ft.Icons.LIGHTBULB_OUTLINE),
            ],
        ),
    )

    return ft.View(
        route="/practice",
        padding=0,
        spacing=0,
        bgcolor=theme.DARK_BG,
        controls=[stage, subtitles, controls_row],
    )
