# Copyright (c) 2026 Wilkend. All rights reserved.
# Hantalk - proprietary software. See LICENSE at the repository root.
# Unauthorized copying, modification, or redistribution is prohibited.

import flet as ft

from app import theme, validators
from app.screen import screen
from controls.brand import logo_mark
from services import auth_service


def _field(label: str) -> ft.TextField:
    return ft.TextField(
        label=label,
        width=290,
        border_radius=14,
        filled=True,
        bgcolor=theme.SURFACE,
        border_color=theme.OUTLINE,
        focused_border_color=theme.PRIMARY,
        color=theme.TEXT,
        label_style=ft.TextStyle(color=theme.TEXT_MUTED, size=14),
        error_style=ft.TextStyle(color=theme.ERROR_TEXT, size=12),
        cursor_color=theme.PRIMARY,
        content_padding=ft.Padding.symmetric(horizontal=16, vertical=18),
    )


def forgot_password_view(page: ft.Page) -> ft.View:
    contact = _field("Email or phone number")

    spinner = ft.ProgressRing(width=18, height=18, stroke_width=2,
                              color=theme.WHITE, visible=False)
    btn_label = ft.Text("Send reset link", size=15,
                        weight=ft.FontWeight.W_600, color=theme.WHITE)
    send_btn = ft.Button(
        width=290,
        height=52,
        disabled=True,
        style=ft.ButtonStyle(
            bgcolor={
                ft.ControlState.DEFAULT: theme.PRIMARY,
                ft.ControlState.DISABLED: theme.DIVIDER,
            },
            shape=ft.RoundedRectangleBorder(radius=26),
        ),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
            controls=[spinner, btn_label],
        ),
    )

    async def go_login(e):
        await page.push_route("/login")

    back_link = ft.TextButton(
        "Back to log in",
        on_click=go_login,
        style=ft.ButtonStyle(color=theme.PRIMARY),
    )

    # The form ───
    form = ft.Column(
        spacing=0,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Text("Forgot your password?", size=26,
                    weight=ft.FontWeight.BOLD, color=theme.TEXT,
                    text_align=ft.TextAlign.CENTER),
            ft.Container(height=6),
            ft.Container(
                width=290,
                content=ft.Text(
                    "Enter the email or phone number on your account and "
                    "we'll send you a link to choose a new password.",
                    size=13, color=theme.TEXT_MUTED,
                    text_align=ft.TextAlign.CENTER),
            ),
            ft.Container(height=26),
            contact,
            ft.Container(height=18),
            send_btn,
        ],
    )

    # The confirmation ───
    sent_to = ft.Text("", size=14, weight=ft.FontWeight.W_600,
                      color=theme.TEXT, text_align=ft.TextAlign.CENTER)
    confirmation = ft.Column(
        visible=False,
        spacing=0,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Container(
                width=64, height=64,
                border_radius=32,
                bgcolor=theme.PRIMARY_CONTAINER,
                alignment=ft.Alignment.CENTER,
                content=ft.Icon(ft.Icons.MARK_EMAIL_READ_OUTLINED,
                                size=30, color=theme.PRIMARY),
            ),
            ft.Container(height=18),
            ft.Text("Check your messages", size=24,
                    weight=ft.FontWeight.BOLD, color=theme.TEXT),
            ft.Container(height=8),
            ft.Container(
                width=290,
                content=ft.Text(
                    "If an account exists, we've sent reset instructions to",
                    size=13, color=theme.TEXT_MUTED,
                    text_align=ft.TextAlign.CENTER),
            ),
            ft.Container(height=4),
            sent_to,
            ft.Container(height=22),
            ft.Button(
                "Back to log in",
                width=290,
                height=52,
                bgcolor=theme.PRIMARY,
                color=theme.WHITE,
                on_click=go_login,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=26),
                    text_style=ft.TextStyle(size=15,
                                            weight=ft.FontWeight.W_600),
                ),
            ),
        ],
    )

    # ── The logic part──────────
    def validate(e=None):
        if contact.error and validators.contact_error(contact.value or "") is None:
            contact.error = None
        send_btn.disabled = validators.contact_error(contact.value or "") is not None
        page.update()

    def check(e):
        contact.error = (
            validators.contact_error(contact.value) if contact.value else None
        )
        page.update()

    async def send(e):
        contact.error = validators.contact_error(contact.value or "")
        if contact.error:
            page.update()
            return

        send_btn.disabled = True
        spinner.visible = True
        btn_label.value = "Sending…"
        page.update()

        auth_service.send_password_reset(
            validators.normalize_identifier(contact.value))
        sent_to.value = contact.value.strip()
        form.visible = False
        confirmation.visible = True
        back_link.visible = False
        page.update()

    contact.on_change = validate
    contact.on_blur = check
    contact.on_submit = send
    send_btn.on_click = send

    return screen("/forgot", [
        ft.Container(height=8),
        logo_mark(56),
        ft.Container(height=20),
        form,
        confirmation,
        ft.Container(height=6),
        back_link,
        ft.Container(height=8),
    ])
