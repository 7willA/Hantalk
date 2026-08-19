# Copyright (c) 2026 Wilkend. All rights reserved.
# Hantalk - proprietary software. See LICENSE at the repository root.
# Unauthorized copying, modification, or redistribution is prohibited.

import asyncio

import flet as ft

from app import theme
from app.screen import screen
from controls.brand import logo_mark

SPLASH_SECONDS = 5


def splash_view(page: ft.Page) -> ft.View:
    """Build the screen splash"""

    async def go_next() -> None:
        await asyncio.sleep(SPLASH_SECONDS)
        await page.push_route("/login")

    page.run_task(go_next)

    return screen("/", [
        logo_mark(96),
        ft.Container(height=22),
        ft.Text("Hantalk", size=30, weight=ft.FontWeight.BOLD,
                color=theme.TEXT),
        ft.Container(height=6),
        ft.Text("Learn Taiwanese Mandarin " \
        "the way it's spoken in Taiwan",
                size=13, color=theme.TEXT_MUTED),
        ft.Container(height=34),
        ft.ProgressRing(width=22, height=22, stroke_width=2,
                        color=theme.PRIMARY),
    ], scroll=False)
