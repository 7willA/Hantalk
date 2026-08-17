# Copyright (c) 2026 Wilkend. All rights reserved.
# Hantalk - proprietary software. See LICENSE at the repository root.
# Unauthorized copying, modification, or redistribution is prohibited.

"""Vocab card control — flashcard pou ekran 04.

Flutter counterpart: lib/widgets/vocab_card.dart
"""

import flet as ft

from app import theme
from models.vocabulary_entry import VocabularyEntry


def vocab_card(entry: VocabularyEntry, revealed: bool = True) -> ft.Control:
    """Flashcard blan ak karaktè a gwo epi egzanp lan anba.

    revealed -- False montre karaktè a sèlman (bò kesyon an).
    """
    back = [
        ft.Container(height=20),
        ft.Container(height=1, bgcolor=theme.DIVIDER, width=10_000),
        ft.Container(height=16),
        ft.Text(
            entry.english,
            size=20,
            weight=ft.FontWeight.W_600,
            color=theme.TEXT,
            text_align=ft.TextAlign.CENTER,
        ),
    ]

    if entry.example_zh:
        back += [
            ft.Container(height=18),
            ft.Container(
                bgcolor=theme.SURFACE,
                border_radius=16,
                padding=ft.Padding.symmetric(vertical=14, horizontal=15),
                content=ft.Column(
                    spacing=0,
                    controls=[
                        ft.Text("EXAMPLE", size=9,
                                weight=ft.FontWeight.W_600,
                                color=theme.TEXT_MUTED),
                        ft.Container(height=9),
                        ft.Text(entry.example_zh,
                                font_family=theme.FONT_ZH, size=22,
                                weight=ft.FontWeight.W_500,
                                color=theme.TEXT),
                        ft.Container(height=5),
                        ft.Text(entry.example_pinyin, size=12,
                                color=theme.TEXT_MUTED),
                        ft.Container(height=6),
                        ft.Text(entry.example_en, size=13,
                                color=theme.TEXT_SECONDARY),
                    ],
                ),
            ),
        ]

    back += [
        ft.Container(height=16),
        ft.Row(
            spacing=7,
            tight=True,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Icon(ft.Icons.VOLUME_UP, size=22, color=theme.PRIMARY),
                ft.Text("Hear it", size=13,
                        weight=ft.FontWeight.W_500, color=theme.PRIMARY),
            ],
        ),
    ]

    return ft.Container(
        bgcolor=theme.WHITE,
        border=ft.Border.all(1, theme.OUTLINE),
        border_radius=26,
        padding=ft.Padding.only(left=24, right=24, top=28, bottom=26),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
            controls=[
                ft.Container(
                    alignment=ft.Alignment.CENTER_LEFT,
                    width=10_000,
                    content=ft.Container(
                        bgcolor=theme.PRIMARY_CONTAINER,
                        border_radius=8,
                        padding=ft.Padding.symmetric(
                            vertical=6, horizontal=11),
                        content=ft.Text(entry.pos, size=11,
                                        weight=ft.FontWeight.W_500,
                                        color=theme.PRIMARY_DARK),
                    ),
                ),
                ft.Container(height=16),
                ft.Text(
                    entry.traditional,
                    font_family=theme.FONT_ZH_SERIF,
                    size=96 if len(entry.traditional) <= 2 else 64,
                    weight=ft.FontWeight.W_500,
                    color=theme.TEXT,
                ),
                ft.Container(height=6),
                ft.Text(entry.pinyin, size=22, color=theme.PRIMARY),
                *(back if revealed else []),
            ],
        ),
    )
