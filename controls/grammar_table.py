# Copyright (c) 2026 Wilkend. All rights reserved.
# Hantalk - proprietary software. See LICENSE at the repository root.
# Unauthorized copying, modification, or redistribution is prohibited.

"""Grammar table control — Structure of the board for the table syntax .
Design: screen 02.
"""

import flet as ft

from app import theme
from models.grammar_pattern import GrammarPattern


def _cell(text: str, header: bool) -> ft.Control:
    return ft.Container(
        expand=True,
        padding=ft.Padding.symmetric(
            vertical=10 if header else 12, horizontal=12
        ),
        content=ft.Text(
            text,
            font_family=None if header else theme.FONT_ZH,
            size=11 if header else 18,
            weight=ft.FontWeight.W_600 if header else ft.FontWeight.W_500,
            color=theme.TEXT_SECONDARY if header else theme.TEXT,
        ),
    )


def grammar_table(pattern: GrammarPattern) -> ft.Control:
    """Card with the formula on top and the structure table below."""
    rows: list[ft.Control] = [
        ft.Container(
            bgcolor=theme.SURFACE_VARIANT,
            content=ft.Row(
                spacing=0,
                controls=[_cell(h, header=True) for h in pattern.headers],
            ),
        )
    ]
    for row in pattern.rows:
        rows.append(
            ft.Container(
                border=ft.Border.only(top=ft.BorderSide(1, theme.DIVIDER)),
                content=ft.Row(
                    spacing=0,
                    controls=[_cell(c, header=False) for c in row],
                ),
            )
        )

    return ft.Column(
        spacing=14,
        controls=[
            ft.Container(
                bgcolor=theme.SURFACE,
                border_radius=16,
                padding=ft.Padding.all(16),
                content=ft.Column(
                    spacing=0,
                    controls=[
                        ft.Text(
                            pattern.title.upper(),
                            size=12,
                            weight=ft.FontWeight.W_600,
                            color=theme.PRIMARY_DARK,
                        ),
                        ft.Container(height=8),
                        ft.Text(
                            pattern.formula,
                            font_family=theme.FONT_ZH,
                            size=22,
                            weight=ft.FontWeight.W_500,
                            color=theme.TEXT,
                        ),
                        ft.Container(height=6),
                        ft.Text(
                            pattern.explanation,
                            size=13,
                            color=theme.TEXT_SECONDARY,
                        ),
                    ],
                ),
            ),
            ft.Container(
                border=ft.Border.all(1, theme.OUTLINE),
                border_radius=16,
                clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                content=ft.Column(spacing=0, controls=rows),
            ),
        ],
    )
