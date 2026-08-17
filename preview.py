# Copyright (c) 2026 Wilkend. All rights reserved.
# Hantalk - proprietary software. See LICENSE at the repository root.
# Unauthorized copying, modification, or redistribution is prohibited.

"""Preview jetab — pou wè controls yo san Home lan egziste.

Kouri:  flet run preview.py
Efase l lè Home lan fini.
"""

import flet as ft

from app import theme
from controls.lesson_card import lesson_card
from models.lesson import Lesson

DEMO = [
    Lesson(1, "你叫什麼名字", "What Is Your Name?", progress=1.0),
    Lesson(2, "我的家人", "My Family", progress=0.35),
    Lesson(3, "買東西", "Shopping", progress=0.0),
    Lesson(4, "在餐廳", "At the Restaurant", progress=0.0, is_locked=True),
]


def main(page: ft.Page):
    page.title = "Hantalk — preview"
    theme.apply_theme(page)

    page.add(
        ft.Container(
            padding=ft.Padding.all(theme.PAD_PAGE),
            content=ft.Column(
                spacing=10,
                controls=[
                    ft.Text("lesson_card — 4 eta", size=14,
                            color=theme.TEXT_MUTED),
                    *[
                        lesson_card(l, selected=(l.number == 2))
                        for l in DEMO
                    ],
                ],
            ),
        )
    )


ft.run(main, assets_dir="assets")
