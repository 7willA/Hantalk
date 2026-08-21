# Copyright (c) 2026 Wilkend. All rights reserved.
# Hantalk - proprietary software. See LICENSE at the repository root.
# Unauthorized copying, modification, or redistribution is prohibited.

"""Phonetic view — screen 03 in the handoff.

4 toggle-able phonetic systems + an audio player (demo, no sound).
"""

import flet as ft

from app import theme
from app.screen import safe_bottom, safe_top
from controls.phonetic_text import phonetic_card, phonetic_chip
from data.lessons.all_lessons import get_lesson


def phonetic_view(page: ft.Page, lesson_number: int, line_index: int) -> ft.View:
    lesson = get_lesson(lesson_number)
    lines = lesson.dialogue.lines if lesson.dialogue else []
    line_index = max(0, min(line_index, len(lines) - 1))
    line = lines[line_index]

    # Local screen state — which systems are visible, and the player state.
    state = {
        "trad": True,
        "pin": True,
        "playing": False,
        "slow": False,
    }

    body = ft.Column(
        expand=True,
        spacing=12,
        scroll=ft.ScrollMode.AUTO,
    )
    chips_row = ft.Row(spacing=8, wrap=True)
    play_icon = ft.Icon(ft.Icons.PLAY_ARROW, size=30, color=theme.WHITE)
    speed_row = ft.Row(spacing=0)

    def rebuild_body():
        cards = []
        if state["trad"]:
            cards.append(phonetic_card(
                "Characters", line.traditional, 46, serif=True))
        if state["pin"]:
            cards.append(phonetic_card("Pinyin", line.pinyin, 25))

        cards.append(
            ft.Container(
                margin=ft.Margin.only(top=4),
                padding=ft.Padding.only(top=16),
                border=ft.Border.only(top=ft.BorderSide(1, theme.DIVIDER)),
                content=ft.Column(
                    spacing=8,
                    controls=[
                        ft.Text("ENGLISH", size=10,
                                weight=ft.FontWeight.W_600,
                                color=theme.TEXT_MUTED),
                        ft.Text(line.english, size=19, color=theme.TEXT),
                    ],
                ),
            )
        )
        body.controls = cards

    def toggle(key):
        def handler(e):
            state[key] = not state[key]
            rebuild_chips()
            rebuild_body()
            page.update()
        return handler

    def rebuild_chips():
        chips_row.controls = [
            phonetic_chip("Characters", state["trad"], toggle("trad")),
            phonetic_chip("Pinyin", state["pin"], toggle("pin")),
        ]

    def toggle_play(e):
        state["playing"] = not state["playing"]
        play_icon.icon = (ft.Icons.PAUSE if state["playing"]
                          else ft.Icons.PLAY_ARROW)
        page.update()

    def set_speed(slow: bool):
        def handler(e):
            state["slow"] = slow
            rebuild_speed()
            page.update()
        return handler

    def _speed_pill(label: str, active: bool, on_click) -> ft.Control:
        return ft.Container(
            padding=ft.Padding.symmetric(vertical=6, horizontal=12),
            border_radius=8,
            bgcolor=theme.BACKGROUND if active else ft.Colors.TRANSPARENT,
            on_click=on_click,
            content=ft.Text(
                label, size=12,
                weight=ft.FontWeight.W_600 if active else ft.FontWeight.NORMAL,
                color=theme.TEXT if active else theme.TEXT_SECONDARY,
            ),
        )

    def rebuild_speed():
        speed_row.controls = [
            _speed_pill("Normal", not state["slow"], set_speed(False)),
            _speed_pill("Slow", state["slow"], set_speed(True)),
        ]

    rebuild_chips()
    rebuild_body()
    rebuild_speed()

    async def close(e):
        await page.push_route(f"/lesson/{lesson_number}")

    header = ft.Container(
        bgcolor=theme.SURFACE,
        padding=ft.Padding.symmetric(vertical=14, horizontal=8),
        content=ft.Row(
            spacing=4,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    padding=ft.Padding.all(8),
                    border_radius=999,
                    on_click=close,
                    content=ft.Icon(ft.Icons.CLOSE, size=24,
                                    color=theme.TEXT),
                ),
                ft.Column(
                    expand=True,
                    spacing=0,
                    controls=[
                        ft.Text(f"Line {line_index + 1} of {len(lines)}",
                                size=17, weight=ft.FontWeight.W_500,
                                color=theme.TEXT),
                        ft.Text(f"{line.speaker} · Lesson {lesson.number}",
                                size=11, color=theme.TEXT_MUTED),
                    ],
                ),
                ft.Container(
                    padding=ft.Padding.all(8),
                    content=ft.Icon(ft.Icons.TEXT_FIELDS, size=24,
                                    color=theme.TEXT_SECONDARY),
                ),
            ],
        ),
    )

    player = ft.Container(
        bgcolor=theme.SURFACE_VARIANT,
        border=ft.Border.only(top=ft.BorderSide(1, theme.OUTLINE)),
        padding=ft.Padding.only(left=20, right=20, top=16, bottom=22),
        content=ft.Column(
            spacing=14,
            controls=[
                ft.Row(
                    spacing=14,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Container(
                            width=56, height=56,
                            bgcolor=theme.PRIMARY,
                            border_radius=999,
                            alignment=ft.Alignment.CENTER,
                            on_click=toggle_play,
                            content=play_icon,
                        ),
                        ft.Column(
                            expand=True,
                            spacing=8,
                            controls=[
                                ft.ProgressBar(
                                    value=0.45, height=4, border_radius=2,
                                    color=theme.PRIMARY, bgcolor=theme.TRACK,
                                ),
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    controls=[
                                        ft.Text("0:02", size=11,
                                                color=theme.TEXT_SECONDARY),
                                        ft.Text("0:04", size=11,
                                                color=theme.TEXT_SECONDARY),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
                ft.Row(
                    spacing=8,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text("Speed", size=12,
                                color=theme.TEXT_SECONDARY),
                        ft.Container(
                            bgcolor=theme.DIVIDER,
                            border_radius=10,
                            padding=ft.Padding.all(3),
                            content=speed_row,
                        ),
                        ft.Container(expand=True),
                        ft.Icon(ft.Icons.REPEAT, size=22,
                                color=theme.TEXT_SECONDARY),
                        ft.Icon(ft.Icons.MIC, size=22,
                                color=theme.TEXT_SECONDARY),
                    ],
                ),
            ],
        ),
    )

    return ft.View(
        route=f"/phonetic/{lesson_number}/{line_index}",
        padding=0,
        spacing=0,
        bgcolor=theme.BACKGROUND,
        controls=[
            safe_top(header),
            ft.Container(
                padding=ft.Padding.only(left=20, right=20, top=16),
                content=chips_row,
            ),
            ft.Container(
                expand=True,
                padding=ft.Padding.only(left=20, right=20, top=18, bottom=20),
                content=body,
            ),
            safe_bottom(player),
        ],
    )
