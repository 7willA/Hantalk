# Copyright (c) 2026 Wilkend. All rights reserved.
# Hantalk - proprietary software. See LICENSE at the repository root.
# Unauthorized copying, modification, or redistribution is prohibited.

"""Router — mape non wout yo sou view yo.

Flutter counterpart: lib/app/router.dart (go_router)

De kalite wout:
  - fiks       "/home", "/drills"        → yon antre nan STATIC
  - ak paramèt "/lesson/2"               → yon patron nan DYNAMIC

Patron yo senp espre: nou koupe wout la sou "/" epi nou konpare
moso pa moso. `{n}` vle di "nenpòt moso, pran l kòm yon nonm".
"""

import flet as ft

from app import theme
from views.auth.login_view import login_view
from views.auth.register_view import register_view
from views.auth.splash_view import splash_view
from views.drills.drills_view import drills_view
from views.home.home_view import home_view
from views.lesson.lesson_view import lesson_view
from views.lesson.phonetic_view import phonetic_view
from views.practice.ai_conversation_view import ai_conversation_view
from views.progress.progress_view import profile_view
from views.settings.settings_view import settings_view
from views.unit.unit_view import unit_view
from views.vocab.vocab_view import vocab_view
from services import settings_service

STATIC = {
    "/": splash_view,
    "/login": login_view,
    "/register": register_view,
    "/home": home_view,
    "/drills": drills_view,
    "/practice": ai_conversation_view,
    "/profile": profile_view,
    "/settings": settings_view,
}

# patron → (fonksyon view)
DYNAMIC = {
    ("unit", "{n}"): unit_view,
    ("lesson", "{n}"): lesson_view,
    ("vocab", "{n}"): vocab_view,
    ("phonetic", "{n}", "{i}"): phonetic_view,
}


def _match(parts: list[str], pattern: tuple[str, ...]) -> list[int] | None:
    """Konpare yon wout ak yon patron. Retounen nonm yo, oswa None."""
    if len(parts) != len(pattern):
        return None

    numbers: list[int] = []
    for part, expected in zip(parts, pattern):
        if expected.startswith("{"):
            if not part.isdigit():
                return None
            numbers.append(int(part))
        elif part != expected:
            return None
    return numbers


def _not_found(page: ft.Page, route: str) -> ft.View:
    async def go_home(e):
        await page.push_route("/home")

    return ft.View(
        route=route,
        bgcolor=theme.BACKGROUND,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Column(
                expand=True,
                spacing=10,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text("404", size=42, weight=ft.FontWeight.BOLD,
                            color=theme.PRIMARY),
                    ft.Text(route, size=13, color=theme.TEXT_MUTED),
                    ft.TextButton("Go home", on_click=go_home,
                                  style=ft.ButtonStyle(color=theme.PRIMARY)),
                ],
            )
        ],
    )


def _build(page: ft.Page, route: str) -> ft.View:
    """Bati View la san okipe sèvis yo."""
    if route in STATIC:
        return STATIC[route](page)

    parts = [p for p in route.split("/") if p]
    for pattern, builder in DYNAMIC.items():
        numbers = _match(parts, pattern)
        if numbers is not None:
            try:
                return builder(page, *numbers)
            except KeyError:
                break

    return _not_found(page, route)


def resolve(page: ft.Page, route: str) -> ft.View:
    """Bay View ki koresponn ak `route`, ak sèvis yo atache sou li.

    POUKISA sèvis la atache ISIT LA epi pa nan main.py:

      Nan Flet 0.85, `page.services` se an reyalite `page.views[0].services`.
      `main.py` fè `page.views.clear()` chak fwa wout la chanje, donk yon
      sèvis ki kole sou premye View la ta mouri nan premye navigasyon an.
      Lè nou atache l sou CHAK View, li toujou vivan kèlkeswa kote nou ye.
    """
    view = _build(page, route)
    view.services = [settings_service.service()]
    return view
