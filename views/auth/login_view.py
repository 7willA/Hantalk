# Copyright (c) 2026 Wilkend. All rights reserved.
# Hantalk - proprietary software. See LICENSE at the repository root.
# Unauthorized copying, modification, or redistribution is prohibited.

"""Login view — koneksyon ak email/modpas.

DEMO: pa gen okenn verifikasyon. Nenpòt email + modpas mennen sou /home.
"""

import flet as ft

from app import theme
from controls.brand import logo_mark


def _field(label: str, password: bool = False) -> ft.TextField:
    return ft.TextField(
        label=label,
        width=290,
        height=56,
        password=password,
        can_reveal_password=password,
        border_radius=14,
        filled=True,
        bgcolor=theme.SURFACE,
        border_color=theme.OUTLINE,
        focused_border_color=theme.PRIMARY,
        color=theme.TEXT,
        label_style=ft.TextStyle(color=theme.TEXT_MUTED, size=14),
        cursor_color=theme.PRIMARY,
    )


def login_view(page: ft.Page) -> ft.View:
    email = _field("Email")
    password = _field("Password", password=True)

    login_btn = ft.Button(
        "Log in",
        width=290,
        height=52,
        disabled=True,
        bgcolor=theme.PRIMARY,
        color=theme.WHITE,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=26),
            text_style=ft.TextStyle(size=15, weight=ft.FontWeight.W_600),
        ),
    )

    def validate(e):
        login_btn.disabled = not (email.value and password.value)
        page.update()

    async def submit(e):
        # pita: rele auth_service isit la
        await page.push_route("/home")

    async def go_register(e):
        await page.push_route("/register")

    async def skip(e):
        await page.push_route("/home")

    email.on_change = validate
    password.on_change = validate
    login_btn.on_click = submit

    return ft.View(
        route="/login",
        bgcolor=theme.BACKGROUND,
        padding=ft.Padding.all(20),
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Column(
                expand=True,
                spacing=0,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    logo_mark(64),
                    ft.Container(height=18),
                    ft.Text("Welcome back", size=26,
                            weight=ft.FontWeight.BOLD, color=theme.TEXT),
                    ft.Container(height=4),
                    ft.Text("Log in to keep your streak going", size=13,
                            color=theme.TEXT_MUTED),
                    ft.Container(height=28),
                    email,
                    ft.Container(height=12),
                    password,
                    ft.Container(height=20),
                    login_btn,
                    ft.Container(height=6),
                    ft.TextButton(
                        "No account? Register",
                        on_click=go_register,
                        style=ft.ButtonStyle(color=theme.PRIMARY),
                    ),
                    ft.TextButton(
                        "Skip for now (demo)",
                        on_click=skip,
                        style=ft.ButtonStyle(color=theme.TEXT_MUTED),
                    ),
                ],
            )
        ],
    )
