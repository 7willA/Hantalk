# Copyright (c) 2026 Wilkend. All rights reserved.
# Hantalk - proprietary software. See LICENSE at the repository root.
# Unauthorized copying, modification, or redistribution is prohibited.

"""Splash view — logo, ti tan, epi ale sou login.

Flutter counterpart: lib/screens/auth/splash_screen.dart
"""

import asyncio

import flet as ft

from app import theme
from controls.brand import logo_mark

SPLASH_SECONDS = 2


def splash_view(page: ft.Page) -> ft.View:
    """Bati ekran splash la."""

    async def go_next() -> None:
        await asyncio.sleep(SPLASH_SECONDS)
        await page.push_route("/login")

    page.run_task(go_next)

    return ft.View(
        route="/",
        bgcolor=theme.BACKGROUND,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Column(
                expand=True,
                spacing=0,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    logo_mark(96),
                    ft.Container(height=22),
                    ft.Text("Hantalk", size=30, weight=ft.FontWeight.BOLD,
                            color=theme.TEXT),
                    ft.Container(height=6),
                    ft.Text("Learn Taiwanese Mandarin",
                            size=13, color=theme.TEXT_MUTED),
                    ft.Container(height=34),
                    ft.ProgressRing(width=22, height=22, stroke_width=2,
                                    color=theme.PRIMARY),
                ],
            )
        ],
    )
