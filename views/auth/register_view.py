# Copyright (c) 2026 Wilkend. All rights reserved.
# Hantalk - proprietary software. See LICENSE at the repository root.
# Unauthorized copying, modification, or redistribution is prohibited.

"""Register view — kreye yon kont.

DEMO: pa gen okenn kont ki kreye vre. Fòm nan mennen sou /home.
"""

import flet as ft

from app import theme
from views.auth.login_view import _field


def register_view(page: ft.Page) -> ft.View:
    username = _field("Username")
    email = _field("Email")
    password = _field("Password", password=True)

    agree = ft.Checkbox(
        label="I agree to the terms",
        value=False,
        active_color=theme.PRIMARY,
        label_style=ft.TextStyle(size=13, color=theme.TEXT_SECONDARY),
    )

    register_btn = ft.Button(
        "Sign up",
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
        register_btn.disabled = not (
            username.value and email.value and password.value and agree.value
        )
        page.update()

    async def submit(e):
        # pita: rele auth_service pou kreye kont lan
        await page.push_route("/home")

    async def go_login(e):
        await page.push_route("/login")

    for field in (username, email, password):
        field.on_change = validate
    agree.on_change = validate
    register_btn.on_click = submit

    return ft.View(
        route="/register",
        bgcolor=theme.BACKGROUND,
        padding=ft.Padding.all(20),
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Column(
                expand=True,
                spacing=0,
                scroll=ft.ScrollMode.AUTO,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text("Create your account", size=26,
                            weight=ft.FontWeight.BOLD, color=theme.TEXT),
                    ft.Container(height=4),
                    ft.Text("12 lessons of Taiwanese Mandarin await",
                            size=13, color=theme.TEXT_MUTED),
                    ft.Container(height=26),
                    username,
                    ft.Container(height=12),
                    email,
                    ft.Container(height=12),
                    password,
                    ft.Container(height=10),
                    ft.Container(width=290, content=agree),
                    ft.Container(height=16),
                    register_btn,
                    ft.Container(height=6),
                    ft.TextButton(
                        "Already have an account? Log in",
                        on_click=go_login,
                        style=ft.ButtonStyle(color=theme.PRIMARY),
                    ),
                ],
            )
        ],
    )
