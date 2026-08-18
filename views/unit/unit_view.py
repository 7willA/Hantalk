# Copyright (c) 2026 Wilkend. All rights reserved.
# Hantalk - proprietary software. See LICENSE at the repository root.
# Unauthorized copying, modification, or redistribution is prohibited.

"""Unit view — anndan yon inite: 5 nœud aktivite sou yon chemen.

Wout: /unit/{n}   (n = nimewo leson an, ki se nimewo inite a)

SE ISIT LA HANTALK SISPANN SANBLE AK LÒT MOUN

  Twa nan 5 nœud yo pa ka egziste nan Duolingo:

    Fonetik  漢字 · ㄅㄆㄇ · Tongyong · Pinyin — 4 sistèm ekriti pou
             menm fraz la. Pa gen lòt lang ki bezwen sa.
    Ton      陰平 · 陽平 · 上聲 · 去聲 + ton netral la.
    Pratike  pale ak yon pwofesè AI.

  Nœud yo pa kreye okenn nouvo kontni: yo mennen sou ekran ki deja
  egziste (/lesson, /vocab, /phonetic, /drills, /practice). Onglè yo
  nan `lesson_view.py` rete — se yon dezyèm chemen sou menm kontni an.

BOUTON GID LA

  Nan kwen dwat bandwòl la (kote Duolingo mete ikon nòt li a) gen yon
  bouton ki louvri gid inite a: pattern gramatikal yo + nòt kiltirèl la.
  Sa a se kontni ki deja nan `models/lesson.py` men ki pa t gen kote
  pou l parèt.
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
    """Gid inite a: pattern gramatikal yo + nòt kiltirèl la."""
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
                        ft.Text("NÒT KILTIRÈL", size=theme.SIZE_LABEL,
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
            ft.Text("Gid sa a poko ekri pou inite sa a.",
                    size=theme.SIZE_BODY, color=theme.TEXT_MUTED)
        )

    def close(e):
        page.pop_dialog()

    page.show_dialog(
        ft.AlertDialog(
            bgcolor=theme.SURFACE,
            shape=ft.RoundedRectangleBorder(radius=theme.RADIUS_LG),
            title=ft.Text("Gid inite a", size=theme.SIZE_H3,
                          weight=ft.FontWeight.W_700, color=theme.TEXT),
            content=ft.Container(
                width=320,
                content=ft.Column(spacing=10, tight=True, scroll=ft.ScrollMode.AUTO,
                                  controls=blocks),
            ),
            actions=[
                ft.TextButton("Fèmen", on_click=close,
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

    # Ki nœud ki gen kat li louvri — nou kòmanse ak sa ki aktif la.
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
                    kicker=f"{section.label()} · INITE {lesson.number}",
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
                            "Fini aktivite ki anvan an pou debloke sa a.",
                        )
                    )
                else:
                    label = ("REVIZE" if activity.state is ActivityState.DONE
                             else "KOMANSE")
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
                        ft.Text(f"Inite {lesson.number}",
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
