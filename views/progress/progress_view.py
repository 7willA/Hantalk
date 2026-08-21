# Copyright (c) 2026 Wilkend. All rights reserved.
# Hantalk - proprietary software. See LICENSE at the repository root.
# Unauthorized copying, modification, or redistribution is prohibited.

"""Profile view — placeholder.

Not part of the UI handoff yet. It exists so the 4th NavigationBar tab
has somewhere to go.
"""

import flet as ft

from app import theme
from app.screen import safe_top
from data.lessons.all_lessons import ALL_LESSONS


def profile_view(page: ft.Page) -> ft.View:
    done = sum(1 for l in ALL_LESSONS if l.progress >= 1.0)
    words = sum(len(l.vocabulary) for l in ALL_LESSONS)

    def _stat(value: str, label: str) -> ft.Control:
        return ft.Container(
            expand=True,
            bgcolor=theme.SURFACE,
            border_radius=18,
            padding=ft.Padding.all(16),
            content=ft.Column(
                spacing=2,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text(value, size=24, weight=ft.FontWeight.BOLD,
                            color=theme.PRIMARY),
                    ft.Text(label, size=11, color=theme.TEXT_MUTED),
                ],
            ),
        )

    async def on_nav(e):
        routes = ["/home", "/drills", "/practice", "/profile"]
        target = routes[e.control.selected_index]
        if target != "/profile":
            await page.push_route(target)

    nav = ft.NavigationBar(
        selected_index=3,
        bgcolor=theme.SURFACE,
        indicator_color=theme.PRIMARY_CONTAINER,
        height=80,
        on_change=on_nav,
        border=ft.Border.only(top=ft.BorderSide(1, theme.DIVIDER)),
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.MENU_BOOK_OUTLINED,
                                        selected_icon=ft.Icons.MENU_BOOK,
                                        label="Lessons"),
            ft.NavigationBarDestination(icon=ft.Icons.GRAPHIC_EQ,
                                        label="Drills"),
            ft.NavigationBarDestination(icon=ft.Icons.FORUM_OUTLINED,
                                        selected_icon=ft.Icons.FORUM,
                                        label="Practice"),
            ft.NavigationBarDestination(icon=ft.Icons.PERSON_OUTLINE,
                                        selected_icon=ft.Icons.PERSON,
                                        label="Profile"),
        ],
    )

    return ft.View(
        route="/profile",
        padding=ft.Padding.all(20),
        bgcolor=theme.BACKGROUND,
        navigation_bar=nav,
        controls=[
            safe_top(ft.Container(height=10)),
            ft.Row(
                spacing=14,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        width=64, height=64, border_radius=999,
                        bgcolor=theme.PRIMARY_CONTAINER,
                        alignment=ft.Alignment.CENTER,
                        content=ft.Text("A", size=28,
                                        weight=ft.FontWeight.BOLD,
                                        color=theme.ON_PRIMARY_DEEP),
                    ),
                    ft.Column(
                        spacing=2,
                        controls=[
                            ft.Text("Alex", size=22,
                                    weight=ft.FontWeight.BOLD,
                                    color=theme.TEXT),
                            ft.Text("Learning since August 2026", size=12,
                                    color=theme.TEXT_MUTED),
                        ],
                    ),
                ],
            ),
            ft.Container(height=24),
            ft.Row(
                spacing=12,
                controls=[
                    _stat(f"{done}", "lessons done"),
                    _stat("12", "day streak"),
                    _stat(f"{words}", "words seen"),
                ],
            ),
            ft.Container(height=24),
            ft.Text("Settings, sync and export land here.",
                    size=13, color=theme.TEXT_MUTED),
        ],
    )
