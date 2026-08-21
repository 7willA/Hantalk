# Copyright (c) 2026 Wilkend. All rights reserved.
# Hantalk - proprietary software. See LICENSE at the repository root.
# Unauthorized copying, modification, or redistribution is prohibited.

"""Home view — the learning path.

Structure: Section → Unit → (Activity, in `views/unit/unit_view.py`)

WHAT CHANGED COMPARED TO THE OLD VERSION

  Before: a flat list of 12 lesson cards.
  Now: for each section, a colored banner and its units shown as
  zigzag nodes. Tapping a unit opens a small card with a button.

  The idea comes from Duolingo and HelloChinese, but the vocabulary is
  Hantalk's own: these are the PAVC sections, and inside each unit
  there's Dialogue, Vocabulary, Phonetics, Tones, and Practice.

WHAT WE ARE NOT TAKING FROM THEM

  Mascot (we don't have one), gems/hearts/energy (no economy in the
  app), reward chest (nothing else to give out).
"""

import flet as ft

from app import theme
from app.screen import safe_top
from controls.node_callout import locked_callout, node_callout
from controls.path_banner import path_banner
from controls.path_node import path_node
from data.lessons.all_lessons import (
    ALL_LESSONS,
    ALL_SECTIONS,
    LESSONS_BY_NUMBER,
    current_lesson,
    section_lessons,
)
from models.activity import ActivityState

# Demo data for parts not yet connected to a real progress service.
STREAK_DAYS = 12
XP = 1840


def _unit_state(lesson) -> ActivityState:
    """State of a unit on the path."""
    if lesson.is_locked:
        return ActivityState.LOCKED
    if lesson.progress >= 1.0:
        return ActivityState.DONE
    return ActivityState.ACTIVE


def _icon_button(name: str, on_click=None) -> ft.Control:
    return ft.Container(
        padding=ft.Padding.all(6),
        border_radius=999,
        on_click=on_click,
        content=ft.Icon(name, size=24, color=theme.TEXT_SECONDARY),
    )


def _stat(icon: str, value: str, color: str) -> ft.Control:
    """Small stat at the top — colored icon, number in dark text.

    The number stays in `theme.TEXT` because the vivid colors give
    2.06:1 on the background: fine for an icon, not readable for a number.
    """
    return ft.Row(
        spacing=6,
        tight=True,
        controls=[
            ft.Icon(icon, size=20, color=color),
            ft.Text(value, size=theme.SIZE_BODY, weight=ft.FontWeight.W_700,
                    color=theme.TEXT),
        ],
    )


def _top_bar(course_pct: float, on_settings=None) -> ft.Control:
    """Compact row: the logo, the stats, the gear icon."""
    return ft.Container(
        bgcolor=theme.SURFACE,
        border=ft.Border.only(bottom=ft.BorderSide(1, theme.OUTLINE)),
        padding=ft.Padding.only(left=20, right=14, top=16, bottom=14),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Row(
                    spacing=16,
                    controls=[
                        _stat(ft.Icons.LOCAL_FIRE_DEPARTMENT,
                              str(STREAK_DAYS), theme.HOME_STREAK),
                        _stat(ft.Icons.BOLT, f"{XP:,}", theme.HOME_XP),
                        _stat(ft.Icons.SCHOOL, f"{course_pct:.0%}",
                              theme.PRIMARY),
                    ],
                ),
                _icon_button(ft.Icons.SETTINGS_OUTLINED, on_settings),
            ],
        ),
    )


def _nav_bar(page: ft.Page) -> ft.NavigationBar:
    async def on_change(e):
        routes = ["/home", "/drills", "/practice", "/profile"]
        target = routes[e.control.selected_index]
        if target != "/home":
            await page.push_route(target)

    return ft.NavigationBar(
        selected_index=0,
        bgcolor=theme.SURFACE,
        indicator_color=theme.PRIMARY_CONTAINER,
        height=80,
        on_change=on_change,
        border=ft.Border.only(top=ft.BorderSide(1, theme.DIVIDER)),
        destinations=[
            ft.NavigationBarDestination(
                icon=ft.Icons.MENU_BOOK_OUTLINED,
                selected_icon=ft.Icons.MENU_BOOK,
                label="Lessons",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.GRAPHIC_EQ, label="Drills"),
            ft.NavigationBarDestination(
                icon=ft.Icons.FORUM_OUTLINED,
                selected_icon=ft.Icons.FORUM,
                label="Practice",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.PERSON_OUTLINE,
                selected_icon=ft.Icons.PERSON,
                label="Profile",
            ),
        ],
    )


def home_view(page: ft.Page) -> ft.View:
    course_pct = sum(l.progress for l in ALL_LESSONS) / len(ALL_LESSONS)
    current = current_lesson()

    # Which unit has its card open. `None` = none.
    # We start with the current unit open, so the first thing the
    # person sees when they arrive is where they should continue.
    state = {"open": current.number}

    body = ft.Column(
        expand=True,
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
    )

    async def open_unit(number: int):
        await page.push_route(f"/unit/{number}")

    def make_open(number: int):
        async def handler(e):
            await open_unit(number)
        return handler

    def make_toggle(number: int):
        def handler(e):
            state["open"] = None if state["open"] == number else number
            rebuild()
            page.update()
        return handler

    def build_section(section) -> list[ft.Control]:
        bg, fg = theme.section_color(section.color_index)
        lessons = section_lessons(section)
        done = section.completed_units(LESSONS_BY_NUMBER)

        out: list[ft.Control] = [
            ft.Container(
                padding=ft.Padding.only(top=22, bottom=18),
                content=path_banner(
                    kicker=f"{section.label()} · {section.level.upper()}",
                    traditional=section.traditional,
                    english=section.english,
                    bg=bg,
                    fg=fg,
                    progress=f"{done} / {section.unit_count} units",
                ),
            )
        ]

        for i, lesson in enumerate(lessons):
            node_state = _unit_state(lesson)
            out.append(
                path_node(
                    label=lesson.traditional,
                    sublabel=lesson.english,
                    state=node_state,
                    color=bg,
                    on_color=fg,
                    index=i,
                    text=lesson.number,
                    on_click=make_toggle(lesson.number),
                )
            )

            if state["open"] == lesson.number:
                if node_state is ActivityState.LOCKED:
                    out.append(
                        locked_callout(
                            lesson.traditional,
                            "Finish the previous unit to unlock this one.",
                        )
                    )
                else:
                    label = ("REVIEW" if node_state is ActivityState.DONE
                             else "START")
                    out.append(
                        node_callout(
                            title=lesson.traditional,
                            subtitle=lesson.english,
                            meta=f"5 activities · {lesson.progress:.0%} done",
                            bg=bg,
                            fg=fg,
                            action_label=label,
                            on_action=make_open(lesson.number),
                        )
                    )

            out.append(ft.Container(height=26))

        return out

    def rebuild() -> None:
        controls: list[ft.Control] = []
        for section in ALL_SECTIONS:
            controls.extend(build_section(section))
        controls.append(ft.Container(height=20))
        body.controls = controls

    rebuild()

    async def open_settings(e):
        await page.push_route("/settings")

    return ft.View(
        route="/home",
        padding=0,
        spacing=0,
        bgcolor=theme.BACKGROUND,
        navigation_bar=_nav_bar(page),
        controls=[
            safe_top(_top_bar(course_pct, open_settings)),
            ft.Container(
                expand=True,
                padding=ft.Padding.symmetric(horizontal=theme.PAD_PAGE),
                content=body,
            ),
        ],
    )
