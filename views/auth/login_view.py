# Copyright (c) 2026 Wilkend. All rights reserved.
# Hantalk - proprietary software. See LICENSE at the repository root.
# Unauthorized copying, modification, or redistribution is prohibited.

"""Login view — email, telefòn, oswa non itilizatè; oswa sosyal.

DEMO: pa gen verifikasyon. Nenpòt idantifyan valab mennen sou /home.

Yon sèl chan pou twa kalite idantifyan: se nou ki devine kalite a
(`app/validators.py`), epi ikòn nan bò dwat la montre sa nou konprann.
"""

import flet as ft

from app import theme, validators
from app.screen import screen
from controls.brand import logo_mark

# Ki ikòn pou ki kalite idantifyan.
KIND_ICONS = {
    validators.EMAIL: ft.Icons.ALTERNATE_EMAIL,
    validators.PHONE: ft.Icons.PHONE_OUTLINED,
    validators.USERNAME: ft.Icons.PERSON_OUTLINE,
}

# Koulè ofisyèl Facebook la. Li pa nan `theme.py` espre: theme.py se
# palèt Hantalk, epi yon koulè mak yon lòt konpayi pa dwe antre ladan l
# — demen si nou vire tout app la an mòd nwa, koulè sa a pa dwe chanje.
FACEBOOK_BLUE = "#1877F2"


def _field(label: str, password: bool = False) -> ft.TextField:
    """Pa gen `height` fiks: `error` la desine ANBA bwat la epi yon
    wotè fiks ta koupe l."""
    return ft.TextField(
        label=label,
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
        error_style=ft.TextStyle(color=theme.ERROR_TEXT, size=12),
        cursor_color=theme.PRIMARY,
        content_padding=ft.Padding.symmetric(horizontal=16, vertical=18),
    )


def _social_button(label: str, badge: ft.Control, on_click) -> ft.Button:
    """Bouton blan ak yon ti bòdi — segondè devan CTA navy la."""
    return ft.Button(
        width=290,
        height=50,
        on_click=on_click,
        style=ft.ButtonStyle(
            bgcolor=theme.SURFACE,
            color=theme.TEXT,
            side=ft.BorderSide(1, theme.OUTLINE),
            shape=ft.RoundedRectangleBorder(radius=25),
            padding=ft.Padding.symmetric(horizontal=18),
        ),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
            controls=[
                badge,
                ft.Text(label, size=14, weight=ft.FontWeight.W_500,
                        color=theme.TEXT),
            ],
        ),
    )


def _divider_with_label(label: str) -> ft.Container:
    def line() -> ft.Container:
        return ft.Container(height=1, bgcolor=theme.OUTLINE, expand=True)

    return ft.Container(
        width=290,
        content=ft.Row(
            spacing=12,
            controls=[
                line(),
                ft.Text(label, size=12, color=theme.TEXT_MUTED),
                line(),
            ],
        ),
    )


def login_view(page: ft.Page) -> ft.View:
    identifier = _field("Email, phone, or username")
    password = _field("Password", password=True)

    # Ikòn nan bò dwat chan an: li di moun nan kisa nou konprann.
    kind_icon = ft.Icon(ft.Icons.PERSON_OUTLINE, size=20,
                        color=theme.TEXT_MUTED, visible=False)
    identifier.suffix = kind_icon

    login_btn = ft.Button(
        "Sign In",
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

    # Ti mesaj anba a — pou bouton sosyal yo ki poko branche.
    notice = ft.Text("", size=12, color=theme.TEXT_MUTED, visible=False)

    def validate(e=None):
        value = identifier.value or ""

        # Ikòn nan swiv sa moun nan ap tape, an tan reyèl.
        kind_icon.visible = bool(value)
        kind_icon.name = KIND_ICONS[validators.identifier_kind(value)]

        # Efase erè a depi moun nan korije l — men pa leve youn isit la.
        if identifier.error and validators.identifier_error(value) is None:
            identifier.error = None
        if password.error and password.value:
            password.error = None

        login_btn.disabled = not (
            validators.identifier_error(value) is None and password.value
        )
        page.update()

    def check_identifier(e):
        """Sou blur — yon chan vid pa yon erè, se yon chan yo poko manyen."""
        identifier.error = (
            validators.identifier_error(identifier.value)
            if identifier.value else None
        )
        page.update()

    async def submit(e):
        identifier.error = validators.identifier_error(identifier.value or "")
        if not password.value:
            password.error = "Enter your password"
        if identifier.error or password.error:
            page.update()
            return

        # Sa a se sa auth_service la dwe resevwa — ni plis ni mwens.
        # `kind` di l nan ki kolòn pou l chèche; `who` se fòm nòmalize a.
        # (Nou pa ekri yo nan console la: yon idantifyan se done prive.)
        kind = validators.identifier_kind(identifier.value)
        who = validators.normalize_identifier(identifier.value)

        # TODO(you): auth_service.sign_in(kind, who, password.value)
        del kind, who
        await page.push_route("/home")

    async def social(e):
        # TODO(you): auth_service.sign_in_with(provider)
        notice.value = "Social login is coming soon."
        notice.visible = True
        page.update()

    async def go_register(e):
        await page.push_route("/register")

    async def go_forgot(e):
        await page.push_route("/forgot")

    async def skip(e):
        await page.push_route("/home")

    identifier.on_change = validate
    identifier.on_blur = check_identifier
    password.on_change = validate
    password.on_submit = submit
    login_btn.on_click = submit

    # Material pa gen logo Google la, donk nou desine yon "G" nan koulè
    # mak la. Ranplase l ak yon vre ikòn nan assets/images lè w vle.
    google_badge = ft.Container(
        width=20, height=20,
        alignment=ft.Alignment.CENTER,
        content=ft.Text("G", size=14, weight=ft.FontWeight.BOLD,
                        color=theme.PRIMARY),
    )
    facebook_badge = ft.Icon(ft.Icons.FACEBOOK, size=20, color=FACEBOOK_BLUE)
    apple_badge = ft.Icon(ft.Icons.APPLE, size=20, color=theme.TEXT)

    forgot_row = ft.Container(
        width=280,
        alignment=ft.Alignment.CENTER,
        content=ft.TextButton(
            "Forgot password?",
            on_click=go_forgot,
            style=ft.ButtonStyle(
                color=theme.TEXT_SECONDARY,
                padding=ft.Padding.symmetric(horizontal=4),
                text_style=ft.TextStyle(size=13),
            ),
        ),
    )

    return screen("/login", [
        ft.Container(height=6),
        logo_mark(60),
        ft.Container(height=16),
        ft.Text("Welcome to Hantalk", size=26,
                weight=ft.FontWeight.BOLD, color=theme.TEXT),
        ft.Container(height=4),
        ft.Text("Enter your details to connect", size=13,
                color=theme.TEXT_MUTED),
        ft.Container(height=28),

        identifier,
        ft.Container(height=12),
        password,
        ft.Container(height=2),
        forgot_row,
        ft.Container(height=10),
        login_btn,

        ft.Container(height=20),
        _divider_with_label("or continue with"),
        ft.Container(height=16),
        _social_button("Continue with Google", google_badge, social),
        ft.Container(height=10),
        _social_button("Continue with Facebook", facebook_badge, social),
        ft.Container(height=10),
        _social_button("Continue with Apple", apple_badge, social),
        ft.Container(height=10),
        notice,

        ft.Container(height=8),
        ft.TextButton(
            "Don't have an account? Create one",
            on_click=go_register,
            style=ft.ButtonStyle(color=theme.PRIMARY),
        ),
        ft.TextButton(
            "Skip for now (demo)",
            on_click=skip,
            style=ft.ButtonStyle(color=theme.TEXT_MUTED),
        ),
        ft.Container(height=8),
    ])
