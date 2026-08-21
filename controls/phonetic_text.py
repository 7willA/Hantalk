# Copyright (c) 2026 Wilkend. All rights reserved.
# Hantalk - proprietary software. See LICENSE at the repository root.
# Unauthorized copying, modification, or redistribution is prohibited.

"""Phonetic text control — a card for a single phonetic system.

Flutter counterpart: lib/widgets/phonetic_text.dart
Design: screen 03, Characters / Pinyin card.
"""

import flet as ft

from app import theme


def phonetic_card(
    label: str,
    text: str,
    size: int,
    color: str | None = None,
    serif: bool = False,
    letter_spacing: float = 0,
) -> ft.Control:
    """Gray card with a label on top and the text below.

    label  -- "Characters", "Pinyin"
    serif  -- True for the characters (Noto Serif TC), False for pinyin
    """
    return ft.Container(
        bgcolor=theme.SURFACE,
        border_radius=20,
        padding=ft.Padding.symmetric(vertical=20, horizontal=18),
        content=ft.Column(
            spacing=0,
            controls=[
                ft.Text(
                    label.upper(),
                    size=10,
                    weight=ft.FontWeight.W_600,
                    color=theme.TEXT_MUTED,
                ),
                ft.Container(height=12),
                ft.Text(
                    text,
                    font_family=theme.FONT_ZH_SERIF if serif
                    else theme.FONT_ZH,
                    size=size,
                    weight=ft.FontWeight.W_500 if serif
                    else ft.FontWeight.NORMAL,
                    color=color or theme.TEXT,
                    selectable=True,
                ),
            ],
        ),
    )


def phonetic_chip(label: str, on: bool, on_click) -> ft.Control:
    """Toggle chip with a checkmark when it's active."""
    return ft.Container(
        height=34,
        padding=ft.Padding.only(left=10, right=13),
        border_radius=9,
        on_click=on_click,
        bgcolor=theme.PRIMARY_CONTAINER if on else ft.Colors.TRANSPARENT,
        border=ft.Border.all(
            1, theme.PRIMARY_CONTAINER if on else theme.OUTLINE
        ),
        content=ft.Row(
            spacing=6,
            tight=True,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Icon(
                    ft.Icons.CHECK if on else ft.Icons.ADD,
                    size=18,
                    color=theme.ON_PRIMARY_DEEP if on
                    else theme.TEXT_SECONDARY,
                ),
                ft.Text(
                    label,
                    size=13,
                    weight=ft.FontWeight.W_500,
                    color=theme.ON_PRIMARY_DEEP if on
                    else theme.TEXT_SECONDARY,
                ),
            ],
        ),
    )
