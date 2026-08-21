# Copyright (c) 2026 Wilkend. All rights reserved.
# Hantalk - proprietary software. See LICENSE at the repository root.
# Unauthorized copying, modification, or redistribution is prohibited.

"""Lesson card control — lesson card for the Home list.
Design: screen 01 HOME in the handoff (sc-for lessons).
"""

import flet as ft

from app import theme
from models.lesson import Lesson


def lesson_card(
    lesson: Lesson,
    selected: bool = False,
    on_click=None,
) -> ft.Control:
    """Build a lesson card for the Home list.

    lesson    -- the lesson data to show
    selected  -- true if this is the lesson currently being read (pink background)
    on_click  -- function to call when the card is tapped
    """
    locked = lesson.is_locked
    done = lesson.progress >= 1.0
    active = 0 < lesson.progress < 1

    # card background
    if locked:
        card_bg = theme.LOCKED_BG
    elif selected:
        card_bg = theme.PRIMARY_CONTAINER
    else:
        card_bg = theme.SURFACE

    if locked:
        badge_bg = theme.DIVIDER
        badge_fg = theme.TEXT_MUTED
    elif done or active:
        badge_bg = theme.PRIMARY
        badge_fg = theme.WHITE
    else:
        badge_bg = theme.DIVIDER
        badge_fg = theme.TEXT_SECONDARY

    if locked:
        icon_name = ft.Icons.LOCK
        icon_color = theme.TEXT_MUTED
    elif done:
        icon_name = ft.Icons.CHECK_CIRCLE
        icon_color = theme.PRIMARY
    else:
        icon_name = ft.Icons.CHEVRON_RIGHT
        icon_color = theme.TEXT_MUTED

    bar_color = theme.PRIMARY if done else theme.PROGRESS_ACTIVE

    # title + subtitle (+ progress bar if the lesson is not locked)
    middle = [
        ft.Text(
            lesson.traditional,
            font_family=theme.FONT_ZH,
            size=20,
            weight=ft.FontWeight.W_500,
            color=theme.TEXT,
            max_lines=1,
            overflow=ft.TextOverflow.ELLIPSIS,
        ),
        ft.Text(
            lesson.english,
            size=theme.SIZE_SMALL,
            color=theme.TEXT_MUTED,
            max_lines=1,
            overflow=ft.TextOverflow.ELLIPSIS,
        ),
    ]
    if not locked:
        middle.append(
            ft.Container(
                margin=ft.Margin.only(top=9),
                content=ft.ProgressBar(
                    value=lesson.progress,
                    bgcolor=theme.OUTLINE,
                    color=bar_color,
                    height=5,
                    border_radius=3,
                ),
            )
        )

    return ft.Container(
        bgcolor=card_bg,
        border_radius=18,
        border=ft.Border.all(
            1,
            theme.SELECTED_BORDER if selected else ft.Colors.TRANSPARENT,
        ),
        padding=ft.Padding.symmetric(vertical=14, horizontal=15),
        opacity=0.55 if locked else 1,
        on_click=None if locked else on_click,
        content=ft.Row(
            spacing=14,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    width=38,
                    height=38,
                    bgcolor=badge_bg,
                    border_radius=12,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Text(
                        "" if locked else str(lesson.number).zfill(2),
                        size=theme.SIZE_BODY,
                        weight=ft.FontWeight.W_600,
                        color=badge_fg,
                    ),
                ),
                ft.Column(
                    expand=True,
                    spacing=2,
                    controls=middle,
                ),
                ft.Icon(icon_name, size=22, color=icon_color),
            ],
        ),
    )
