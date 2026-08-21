# Copyright (c) 2026 Wilkend. All rights reserved.
# Hantalk - proprietary software. See LICENSE at the repository root.
# Unauthorized copying, modification, or redistribution is prohibited.

"""Vocab view — screen 04 in the handoff.

Flashcards: segmented progress bar, flipping cards, Review / Know it.
"""

import flet as ft

from app import theme
from app.screen import safe_bottom, safe_top
from controls.vocab_card import vocab_card
from data.lessons.all_lessons import get_lesson


def vocab_view(page: ft.Page, lesson_number: int) -> ft.View:
    lesson = get_lesson(lesson_number)
    words = lesson.vocabulary

    state = {"index": 0, "revealed": False, "known": set()}

    progress_row = ft.Row(spacing=5)
    card_slot = ft.Container(alignment=ft.Alignment.CENTER)
    subtitle = ft.Text(size=11, color=theme.TEXT_MUTED)

    def rebuild():
        i = state["index"]
        progress_row.controls = [
            ft.Container(
                expand=True,
                height=4,
                border_radius=2,
                bgcolor=theme.PRIMARY if n in state["known"]
                else (theme.PROGRESS_ACTIVE if n == i else theme.DIVIDER),
            )
            for n in range(len(words))
        ]
        card_slot.content = vocab_card(words[i], revealed=state["revealed"])
        subtitle.value = (
            f"Lesson {lesson.number} · card {i + 1} of {len(words)}"
        )

    def flip(e):
        state["revealed"] = not state["revealed"]
        rebuild()
        page.update()

    def step(delta: int):
        state["index"] = (state["index"] + delta) % len(words)
        state["revealed"] = False
        rebuild()
        page.update()

    def mark(known: bool):
        def handler(e):
            if known:
                state["known"].add(state["index"])
            else:
                state["known"].discard(state["index"])
            step(1)
        return handler

    def on_swipe(e: ft.DragEndEvent):
        # negative velocity = right-to-left = next card
        vx = e.primary_velocity or 0
        if vx < -100:
            step(1)
        elif vx > 100:
            step(-1)

    rebuild()

    async def go_back(e):
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
                    on_click=go_back,
                    content=ft.Icon(ft.Icons.ARROW_BACK, size=24,
                                    color=theme.TEXT),
                ),
                ft.Column(
                    expand=True,
                    spacing=0,
                    controls=[
                        ft.Text("Flashcards", size=17,
                                weight=ft.FontWeight.W_500,
                                color=theme.TEXT),
                        subtitle,
                    ],
                ),
                ft.Container(
                    padding=ft.Padding.all(8),
                    border_radius=999,
                    on_click=lambda e: step(1),
                    content=ft.Icon(ft.Icons.SHUFFLE, size=24,
                                    color=theme.TEXT_SECONDARY),
                ),
            ],
        ),
    )

    def _hint(icon: str, side: str) -> ft.Control:
        return ft.Container(
            opacity=0.5,
            content=ft.Column(
                spacing=2,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Icon(icon, size=22, color=theme.TEXT_MUTED),
                    ft.Text(side, size=9, color=theme.TEXT_MUTED),
                ],
            ),
        )

    stage = ft.GestureDetector(
        expand=True,
        on_tap=flip,
        on_horizontal_drag_end=on_swipe,
        content=ft.Container(
            expand=True,
            padding=ft.Padding.all(20),
            content=ft.Row(
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    _hint(ft.Icons.CHEVRON_LEFT, "PREV"),
                    ft.Container(
                        expand=True,
                        content=ft.Column(
                            alignment=ft.MainAxisAlignment.CENTER,
                            scroll=ft.ScrollMode.AUTO,
                            controls=[card_slot],
                        ),
                    ),
                    _hint(ft.Icons.CHEVRON_RIGHT, "NEXT"),
                ],
            ),
        ),
    )

    actions = ft.Container(
        padding=ft.Padding.only(left=20, right=20, bottom=26),
        content=ft.Row(
            spacing=12,
            controls=[
                ft.Container(
                    expand=True,
                    height=52,
                    border_radius=26,
                    border=ft.Border.all(1, theme.PRIMARY),
                    bgcolor=theme.BACKGROUND,
                    alignment=ft.Alignment.CENTER,
                    on_click=mark(False),
                    content=ft.Row(
                        spacing=8,
                        tight=True,
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Icon(ft.Icons.REFRESH, size=20,
                                    color=theme.PRIMARY),
                            ft.Text("Review", size=15,
                                    weight=ft.FontWeight.W_600,
                                    color=theme.PRIMARY),
                        ],
                    ),
                ),
                ft.Container(
                    expand=True,
                    height=52,
                    border_radius=26,
                    bgcolor=theme.PRIMARY,
                    alignment=ft.Alignment.CENTER,
                    on_click=mark(True),
                    content=ft.Row(
                        spacing=8,
                        tight=True,
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Icon(ft.Icons.CHECK, size=20,
                                    color=theme.WHITE),
                            ft.Text("Know it", size=15,
                                    weight=ft.FontWeight.W_600,
                                    color=theme.WHITE),
                        ],
                    ),
                ),
            ],
        ),
    )

    return ft.View(
        route=f"/vocab/{lesson_number}",
        padding=0,
        spacing=0,
        bgcolor=theme.BACKGROUND,
        controls=[
            safe_top(header),
            ft.Container(
                padding=ft.Padding.only(left=20, right=20, top=14),
                content=progress_row,
            ),
            stage,
            safe_bottom(actions),
        ],
    )
