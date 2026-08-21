# Copyright (c) 2026 Wilkend. All rights reserved.
# Hantalk - proprietary software. See LICENSE at the repository root.
# Unauthorized copying, modification, or redistribution is prohibited.

"""Unit view — inside a unit: 5 activity nodes on a path.

Route: /unit/{n}   (n = lesson number, which is also the unit number)

THIS IS WHERE HANTALK STOPS LOOKING LIKE EVERYONE ELSE

  Three of the 5 nodes can't exist in Duolingo:

    Phonetic  漢字 · ㄅㄆㄇ · Tongyong · Pinyin — 4 writing systems for
              the same phrase. No other language needs this.
    Tones     陰平 · 陽平 · 上聲 · 去聲 + the neutral tone.
    Practice  talk with an AI teacher.

  The nodes don't create any new content: they lead to screens that
  already exist (/lesson, /vocab, /phonetic, /drills, /practice). The
  tabs in `lesson_view.py` stay — this is just a second path to the
  same content.

THE GUIDE BUTTON

  In the top-right corner of the banner (where Duolingo puts its notes
  icon) there's a button that opens the unit guide: the grammar
  patterns + the cultural note. This is content that already exists in
  `models/lesson.py` but had nowhere to appear.
"""

import flet as ft

from app import theme
from app.screen import safe_top
from controls.node_callout import locked_callout, node_callout
from controls.path_banner import path_banner
from controls.path_node import KIND_ICONS, path_node
from data.lessons.all_lessons import get_lesson, section_of
from models.activity import ActivityState, build_activities


def _guide_dialog(page: ft.Page, lesson, bg: str) -> None:
    """The unit guide: the grammar patterns + the cultural note."""
    blocks: list[ft.Control] = []

    for pattern in lesson.patterns:
        blocks.append(
            ft.Container(
                bgcolor=theme.SURFACE_VARIANT,
                border_radius=theme.RADIUS_MD,
                padding=ft.Padding.all(14),
                content=ft.Column(
                    spacing=5,
                    controls=[
                        ft.Text(pattern.title, size=theme.SIZE_LABEL,
                                weight=ft.FontWeight.W_700, color=bg),
                        ft.Text(pattern.formula, font_family=theme.FONT_ZH,
                                size=18, weight=ft.FontWeight.W_500,
                                color=theme.TEXT),
                        ft.Text(pattern.explanation, size=theme.SIZE_SMALL,
                                color=theme.TEXT_SECONDARY),
                    ],
                ),
            )
        )

    if lesson.culture_note:
        blocks.append(
            ft.Container(
                padding=ft.Padding.only(top=4),
                content=ft.Column(
                    spacing=6,
                    controls=[
                        ft.Text("CULTURE NOTE", size=theme.SIZE_LABEL,
                                weight=ft.FontWeight.W_700,
                                color=theme.TEXT_MUTED),
                        ft.Text(lesson.culture_note, size=theme.SIZE_BODY,
                                color=theme.TEXT_SECONDARY),
                    ],
                ),
            )
        )

    if not blocks:
        blocks.append(
            ft.Text("This guide has not been written for this unit yet.",
                    size=theme.SIZE_BODY, color=theme.TEXT_MUTED)
        )

    def close(e):
        page.pop_dialog()

    page.show_dialog(
        ft.AlertDialog(
            bgcolor=theme.SURFACE,
            shape=ft.RoundedRectangleBorder(radius=theme.RADIUS_LG),
            title=ft.Text("Unit guide", size=theme.SIZE_H3,
                          weight=ft.FontWeight.W_700, color=theme.TEXT),
            content=ft.Container(
                width=320,
                content=ft.Column(spacing=10, tight=True, scroll=ft.ScrollMode.AUTO,
                                  controls=blocks),
            ),
            actions=[
                ft.TextButton("Close", on_click=close,
                              style=ft.ButtonStyle(color=theme.PRIMARY)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
    )


def unit_view(page: ft.Page, lesson_number: int) -> ft.View:
    lesson = get_lesson(lesson_number)
    section = section_of(lesson)
    bg, fg = theme.section_color(section.color_index)
    activities = build_activities(lesson)

    # Which node has its card open — we start with the active one.
    first_active = next(
        (a.kind.value for a in activities
         if a.state is ActivityState.ACTIVE),
        None,
    )
    state = {"open": first_active}

    body = ft.Column(expand=True, spacing=0, scroll=ft.ScrollMode.AUTO)

    def make_go(route: str):
        async def handler(e):
            await page.push_route(route)
        return handler

    def make_toggle(kind_value: str):
        def handler(e):
            state["open"] = (None if state["open"] == kind_value
                             else kind_value)
            rebuild()
            page.update()
        return handler

    def rebuild() -> None:
        out: list[ft.Control] = [
            ft.Container(
                padding=ft.Padding.only(top=16, bottom=20),
                content=path_banner(
                    kicker=f"{section.label()} · UNIT {lesson.number}",
                    traditional=lesson.traditional,
                    english=lesson.english,
                    bg=bg,
                    fg=fg,
                    on_action=lambda e: _guide_dialog(page, lesson, bg),
                ),
            )
        ]

        for i, activity in enumerate(activities):
            out.append(
                path_node(
                    label=activity.title,
                    state=activity.state,
                    color=bg,
                    on_color=fg,
                    index=i,
                    icon=KIND_ICONS[activity.kind],
                    on_click=make_toggle(activity.kind.value),
                )
            )

            if state["open"] == activity.kind.value:
                if activity.state is ActivityState.LOCKED:
                    out.append(
                        locked_callout(
                            activity.title,
                            "Finish the previous activity to unlock this one.",
                        )
                    )
                else:
                    label = ("REVIEW" if activity.state is ActivityState.DONE
                             else "START")
                    out.append(
                        node_callout(
                            title=activity.title,
                            subtitle=activity.subtitle,
                            meta=activity.count_label(),
                            bg=bg,
                            fg=fg,
                            action_label=label,
                            on_action=make_go(activity.route),
                        )
                    )

            out.append(ft.Container(height=24))

        out.append(ft.Container(height=20))
        body.controls = out

    rebuild()

    async def go_back(e):
        await page.push_route("/home")

    header = ft.Container(
        bgcolor=theme.SURFACE,
        border=ft.Border.only(bottom=ft.BorderSide(1, theme.OUTLINE)),
        padding=ft.Padding.only(left=8, right=20, top=14, bottom=14),
        content=ft.Row(
            spacing=4,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    padding=ft.Padding.all(8),
                    border_radius=999,
                    on_click=go_back,
                    content=ft.Icon(ft.Icons.ARROW_BACK, size=24,
                                    color=theme.TEXT),
                ),
                ft.Column(
                    spacing=0,
                    expand=True,
                    controls=[
                        ft.Text(f"Unit {lesson.number}",
                                size=theme.SIZE_H3,
                                weight=ft.FontWeight.W_600, color=theme.TEXT),
                        ft.Text(section.english, size=theme.SIZE_SMALL,
                                color=theme.TEXT_MUTED),
                    ],
                ),
            ],
        ),
    )

    return ft.View(
        route=f"/unit/{lesson_number}",
        padding=0,
        spacing=0,
        bgcolor=theme.BACKGROUND,
        controls=[
            safe_top(header),
            ft.Container(
                expand=True,
                padding=ft.Padding.symmetric(horizontal=theme.PAD_PAGE),
                content=body,
            ),
        ],
    )
