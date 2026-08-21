# Copyright (c) 2026 Wilkend. All rights reserved.
# Hantalk - proprietary software. See LICENSE at the repository root.
# Unauthorized copying, modification, or redistribution is prohibited.

"""Drills view — screen 06 in the handoff.

Accuracy card · 2×3 grid of tone tiles (curves on ft.Canvas) · selected
drill panel · "Start drill" button · NavigationBar.
"""

import flet as ft
import flet.canvas as cv

from app import theme
from app.screen import safe_top
from data.drills import DRILLS, Drill

ACCURACY = 84
SYLLABLES = 240

TILE_W = 120
TILE_H = 34


def _contour(drill: Drill, active: bool) -> ft.Control:
    """The tone curve drawn on a Canvas."""
    line_color = theme.WHITE if active else theme.PRIMARY
    grid_color = theme.ON_PRIMARY_SOFT_DIM if active else theme.OUTLINE

    shapes: list[cv.Shape] = [
        cv.Line(0, 30, TILE_W, 30,
                paint=ft.Paint(stroke_width=1, color=grid_color)),
    ]

    if drill.dot:
        shapes.append(
            cv.Circle(TILE_W / 2, 17, 5,
                      paint=ft.Paint(color=line_color,
                                     style=ft.PaintingStyle.FILL))
        )
    elif drill.points:
        for (x1, y1), (x2, y2) in zip(drill.points, drill.points[1:]):
            shapes.append(
                cv.Line(x1, y1, x2, y2,
                        paint=ft.Paint(
                            stroke_width=3.5,
                            color=line_color,
                            stroke_cap=ft.StrokeCap.ROUND,
                        ))
            )

    return ft.Container(
        height=TILE_H,
        margin=ft.Margin.only(top=12, bottom=10),
        content=cv.Canvas(shapes=shapes, expand=True),
    )


def _pills(drill: Drill, active: bool) -> ft.Control:
    fg = theme.WHITE if active else theme.TEXT_SECONDARY
    bg = theme.ON_PRIMARY_FILM if active else theme.SURFACE_VARIANT
    return ft.Container(
        margin=ft.Margin.only(top=14, bottom=10),
        content=ft.Row(
            spacing=5,
            wrap=True,
            controls=[
                ft.Container(
                    bgcolor=bg,
                    border_radius=6,
                    padding=ft.Padding.symmetric(vertical=4, horizontal=7),
                    content=ft.Text(p, size=11, color=fg),
                )
                for p in drill.pills
            ],
        ),
    )


def _tile(drill: Drill, active: bool, on_click) -> ft.Control:
    fg = theme.WHITE if active else theme.TEXT
    dim = theme.ON_PRIMARY_SOFT if active else theme.TEXT_MUTED

    return ft.Container(
        expand=True,
        bgcolor=theme.PRIMARY if active else theme.SURFACE,
        border_radius=18,
        padding=ft.Padding.all(14),
        on_click=on_click,
        content=ft.Column(
            spacing=0,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    controls=[
                        ft.Text(
                            drill.glyph,
                            font_family=theme.FONT_ZH_SERIF if not drill.pills
                            else theme.FONT_ZH,
                            size=30,
                            weight=ft.FontWeight.W_500,
                            color=fg,
                        ),
                        ft.Icon(
                            ft.Icons.PLAY_CIRCLE if active
                            else ft.Icons.PLAY_CIRCLE_OUTLINE,
                            size=19, color=dim,
                        ),
                    ],
                ),
                _pills(drill, active) if drill.pills
                else _contour(drill, active),
                ft.Text(drill.title, size=14,
                        weight=ft.FontWeight.W_600, color=fg),
                ft.Container(height=2),
                ft.Text(drill.subtitle, size=11, color=dim),
            ],
        ),
    )


def drills_view(page: ft.Page) -> ft.View:
    state = {"key": DRILLS[1].key}

    grid = ft.Column(spacing=12)
    panel_title = ft.Text(size=20, weight=ft.FontWeight.W_500,
                          color=theme.ON_PRIMARY_DEEP)
    panel_hint = ft.Text(size=13, color=theme.PRIMARY_DARK)

    def select(key: str):
        def handler(e):
            state["key"] = key
            rebuild()
            page.update()
        return handler

    def rebuild():
        rows = []
        for i in range(0, len(DRILLS), 2):
            pair = DRILLS[i:i + 2]
            rows.append(
                ft.Row(
                    spacing=12,
                    vertical_alignment=ft.CrossAxisAlignment.STRETCH,
                    controls=[
                        _tile(d, d.key == state["key"], select(d.key))
                        for d in pair
                    ],
                )
            )
        grid.controls = rows

        current = next(d for d in DRILLS if d.key == state["key"])
        panel_title.value = current.title
        panel_hint.value = current.hint

    rebuild()

    async def go(route):
        await page.push_route(route)

    header = ft.Container(
        bgcolor=theme.SURFACE,
        padding=ft.Padding.symmetric(vertical=14, horizontal=8),
        content=ft.Row(
            spacing=4,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    padding=ft.Padding.only(left=12),
                    expand=True,
                    content=ft.Column(
                        spacing=0,
                        controls=[
                            ft.Text("Drills", size=19,
                                    weight=ft.FontWeight.W_500,
                                    color=theme.TEXT),
                            ft.Text("Tones · initials · finals", size=11,
                                    color=theme.TEXT_MUTED),
                        ],
                    ),
                ),
                ft.Container(padding=ft.Padding.all(8),
                             content=ft.Icon(ft.Icons.HISTORY, size=24,
                                             color=theme.TEXT_SECONDARY)),
                ft.Container(padding=ft.Padding.all(8),
                             content=ft.Icon(ft.Icons.HELP_OUTLINE, size=24,
                                             color=theme.TEXT_SECONDARY)),
            ],
        ),
    )

    accuracy_card = ft.Container(
        margin=ft.Margin.only(left=20, right=20, top=18),
        bgcolor=theme.SURFACE,
        border_radius=18,
        padding=ft.Padding.symmetric(vertical=15, horizontal=16),
        content=ft.Row(
            spacing=14,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Icon(ft.Icons.GRAPHIC_EQ, size=26, color=theme.PRIMARY),
                ft.Column(
                    expand=True,
                    spacing=0,
                    controls=[
                        ft.Text("Accuracy this week", size=14,
                                weight=ft.FontWeight.W_600, color=theme.TEXT),
                        ft.Text(f"{ACCURACY}% · {SYLLABLES} syllables "
                                f"recorded", size=12, color=theme.TEXT_MUTED),
                    ],
                ),
                ft.Text(f"{ACCURACY}%", size=22,
                        weight=ft.FontWeight.BOLD, color=theme.PRIMARY),
            ],
        ),
    )

    selected_panel = ft.Container(
        margin=ft.Margin.only(top=18),
        bgcolor=theme.PRIMARY_CONTAINER,
        border_radius=18,
        padding=ft.Padding.all(16),
        content=ft.Column(
            spacing=0,
            controls=[
                ft.Text("SELECTED DRILL", size=11,
                        weight=ft.FontWeight.W_600,
                        color=theme.PRIMARY_DARK),
                ft.Container(height=7),
                panel_title,
                ft.Container(height=4),
                panel_hint,
            ],
        ),
    )

    body = ft.Container(
        expand=True,
        padding=ft.Padding.only(left=20, right=20, top=14, bottom=20),
        content=ft.Column(
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Text("6 DRILL UNITS", size=10,
                        weight=ft.FontWeight.W_600, color=theme.TEXT_MUTED),
                ft.Container(height=12),
                grid,
                selected_panel,
                ft.Container(height=70),
            ],
        ),
    )

    start_button = ft.FloatingActionButton(
        content=ft.Row(
            spacing=10,
            tight=True,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Icon(ft.Icons.MIC, size=24, color=theme.WHITE),
                ft.Text("Start drill", size=15,
                        weight=ft.FontWeight.W_600, color=theme.WHITE),
            ],
        ),
        bgcolor=theme.PRIMARY,
        shape=ft.RoundedRectangleBorder(radius=18),
        width=160,
        height=56,
    )

    async def on_nav(e):
        routes = ["/home", "/drills", "/practice", "/profile"]
        target = routes[e.control.selected_index]
        if target != "/drills":
            await page.push_route(target)

    nav = ft.NavigationBar(
        selected_index=1,
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
        route="/drills",
        padding=0,
        spacing=0,
        bgcolor=theme.BACKGROUND,
        navigation_bar=nav,
        floating_action_button=start_button,
        controls=[safe_top(header), accuracy_card, body],
    )
