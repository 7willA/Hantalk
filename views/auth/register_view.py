# Copyright (c) 2026 Wilkend. All rights reserved.
# Hantalk - proprietary software. See LICENSE at the repository root.
# Unauthorized copying, modification, or redistribution is prohibited.

"""Register view — create an account.

DEMO: no backend yet. A valid form leads straight to /home.
`auth_service` is still a stub — the single call site is marked TODO below.

WHAT THIS SCREEN ASKS

  Display name, email OR phone number, password, confirm password, and
  consent. Nothing else. Everything a language app wants to know about
  the learner (level, goal, phonetic system, daily goal) belongs AFTER
  signup, in an onboarding flow, where the user is already invested.

  Social sign-in buttons live on the LOGIN screen, not here.

VALIDATION RULES

  Errors appear on blur (when the user leaves a field), never on every
  keystroke — nobody wants "invalid email" flashing at them while they
  are still typing the first letter. An error clears the instant the
  user fixes it. The submit button stays disabled until every rule
  passes, and a final check runs on submit anyway.

  The rules themselves live in `app/validators.py`, shared with /login
  and /forgot — one source of truth, so a phone number accepted here
  can never be rejected at login.
"""

import flet as ft

from app import theme, validators
from app.screen import screen
from controls.brand import logo_mark

# Ki koulè pou chak nivo nan mèt fòs modpas la. `validators.strength()`
# bay nòt la ak etikèt la; ekran an chwazi koulè a.
STRENGTH_COLORS = (
    theme.ERROR_TEXT,     # 0 Weak
    theme.ERROR_TEXT,     # 1 Weak
    theme.ACCENT_DARK,    # 2 Fair
    theme.SUCCESS_TEXT,   # 3 Good
    theme.SUCCESS_TEXT,   # 4 Strong
)

# ── Building block ─────────────────────────────────────────

def _field(label: str, password: bool = False, hint: str = "") -> ft.TextField:
    """Same look as the login fields, but with no fixed height.

    A fixed `height=56` clips the `error` text, which renders *below*
    the box. Letting the field size itself keeps the error readable.
    """
    return ft.TextField(
        label=label,
        hint_text=hint or None,
        width=290,
        password=password,
        can_reveal_password=password,
        border_radius=14,
        filled=True,
        bgcolor=theme.SURFACE,
        border_color=theme.OUTLINE,
        focused_border_color=theme.PRIMARY,
        color=theme.TEXT,
        label_style=ft.TextStyle(color=theme.TEXT_MUTED, size=14),
        hint_style=ft.TextStyle(color=theme.TEXT_MUTED, size=13),
        error_style=ft.TextStyle(color=theme.ERROR_TEXT, size=12),
        cursor_color=theme.PRIMARY,
        content_padding=ft.Padding.symmetric(horizontal=16, vertical=18),
    )


def register_view(page: ft.Page) -> ft.View:
    # ── Fields ─────────────────────────────────────────────
    display_name = _field("Display name", hint="What should we call you?")
    contact = _field("Email or phone number")
    password = _field("Password", password=True)
    confirm = _field("Confirm password", password=True)

    # ── Password strength meter ────────────────────────────
    bars = [
        ft.Container(height=4, expand=True, border_radius=2,
                     bgcolor=theme.DIVIDER)
        for _ in range(4)
    ]
    strength_label = ft.Text("", size=11, color=theme.TEXT_MUTED,
                             weight=ft.FontWeight.W_600)
    strength_meter = ft.Container(
        width=290,
        visible=False,
        content=ft.Column(
            spacing=5,
            controls=[
                ft.Row(spacing=4, controls=bars),
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text(f"{validators.MIN_PASSWORD}+ characters, letters and numbers",
                                size=11, color=theme.TEXT_MUTED),
                        strength_label,
                    ],
                ),
            ],
        ),
    )

    # ── Terms + privacy ────────────────────────────────────
    async def open_terms(e):
        # TODO(you): point these at the real documents.
        await page.launch_url("https://github.com/7willA/Hantalk")

    link = ft.TextStyle(
        size=13,
        color=theme.PRIMARY,
        weight=ft.FontWeight.W_600,
        decoration=ft.TextDecoration.UNDERLINE,
    )
    plain = ft.TextStyle(size=13, color=theme.TEXT_SECONDARY)

    agree = ft.Checkbox(
        value=False,
        active_color=theme.PRIMARY,
        splash_radius=0,
    )
    terms_row = ft.Container(
        width=290,
        content=ft.Row(
            spacing=2,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                agree,
                ft.Container(
                    expand=True,
                    content=ft.Text(
                        spans=[
                            ft.TextSpan("I agree to the ", plain),
                            ft.TextSpan("Terms", link, on_click=open_terms),
                            ft.TextSpan(" and ", plain),
                            ft.TextSpan("Privacy Policy", link,
                                        on_click=open_terms),
                        ],
                    ),
                ),
            ],
        ),
    )

    # ── Form-level error banner ────────────────────────────
    banner_text = ft.Text("", size=12, color=theme.ERROR_TEXT, expand=True)
    banner = ft.Container(
        width=290,
        visible=False,
        padding=ft.Padding.symmetric(horizontal=14, vertical=10),
        border_radius=12,
        bgcolor=theme.ACCENT_SOFT,
        content=ft.Row(
            spacing=8,
            controls=[
                ft.Icon(ft.Icons.ERROR_OUTLINE, size=16, color=theme.ERROR),
                banner_text,
            ],
        ),
    )

    # ── Submit button ──────────────────────────────────────
    spinner = ft.ProgressRing(width=18, height=18, stroke_width=2,
                              color=theme.WHITE, visible=False)
    btn_label = ft.Text("Create account", size=15,
                        weight=ft.FontWeight.W_600, color=theme.WHITE)
    register_btn = ft.Button(
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

    # ── Logic ──────────────────────────────────────────────
    def _errors() -> dict[ft.TextField, str | None]:
        pw = password.value or ""
        return {
            display_name: validators.name_error(display_name.value or ""),
            contact: validators.contact_error(contact.value or ""),
            password: validators.password_error(pw),
            confirm: validators.confirm_error(pw, confirm.value or ""),
        }

    def _form_is_valid() -> bool:
        return not any(_errors().values()) and bool(agree.value)

    def refresh(e=None):
        """Runs on every keystroke: meter + button state, no new errors."""
        pw = password.value or ""
        score, label = validators.strength(pw)
        color = STRENGTH_COLORS[score]
        strength_meter.visible = bool(pw)
        strength_label.value = label
        strength_label.color = color
        for i, bar in enumerate(bars):
            bar.bgcolor = color if i < score else theme.DIVIDER

        # Clear a field's error the moment the user fixes it — but never
        # raise a new one here; that is `check`'s job, on blur.
        for field, err in _errors().items():
            if field.error and err is None:
                field.error = None

        if banner.visible and _form_is_valid():
            banner.visible = False

        register_btn.disabled = not _form_is_valid()
        page.update()

    def check(field: ft.TextField):
        """On blur — an empty field is untouched, not wrong."""
        def handler(e):
            field.error = _errors()[field] if field.value else None
            page.update()
        return handler

    async def submit(e):
        # Re-validate everything: the button can only be reached through
        # a valid form, but never trust the UI state alone.
        errors = _errors()
        for field, err in errors.items():
            field.error = err
        if any(errors.values()):
            page.update()
            return
        if not agree.value:
            banner_text.value = "Please accept the Terms to continue."
            banner.visible = True
            page.update()
            return

        # Loading state — stops double taps and shows the app is working.
        register_btn.disabled = True
        spinner.visible = True
        btn_label.value = "Creating account…"
        banner.visible = False
        page.update()

        try:
            # TODO(you): auth_service.sign_up(
            #     contact.value, password.value, display_name.value)
            # On failure: banner_text.value = "…"; banner.visible = True
            await page.push_route("/home")
        except Exception:
            spinner.visible = False
            btn_label.value = "Create account"
            register_btn.disabled = False
            banner_text.value = "Could not create your account. Try again."
            banner.visible = True
            page.update()

    async def go_login(e):
        await page.push_route("/login")

    # ── Wiring ─────────────────────────────────────────────
    for field in (display_name, contact, password, confirm):
        field.on_change = refresh
        field.on_blur = check(field)
    confirm.on_submit = submit
    agree.on_change = refresh
    register_btn.on_click = submit

    return screen("/register", [
        ft.Container(height=8),
        logo_mark(52),
        ft.Container(height=14),
        ft.Text("Create your account", size=26,
                weight=ft.FontWeight.BOLD, color=theme.TEXT),
        ft.Container(height=4),
        ft.Text("12 lessons of Taiwanese Mandarin await",
                size=13, color=theme.TEXT_MUTED),
        ft.Container(height=26),

        display_name,
        ft.Container(height=12),
        contact,
        ft.Container(height=12),
        password,
        ft.Container(height=8),
        strength_meter,
        ft.Container(height=12),
        confirm,
        ft.Container(height=10),
        terms_row,
        ft.Container(height=10),
        banner,
        ft.Container(height=10),
        register_btn,
        ft.Container(height=6),
        ft.TextButton(
            "Already have an account? Log in",
            on_click=go_login,
            style=ft.ButtonStyle(color=theme.PRIMARY),
        ),
        ft.Container(height=8),
    ])
