# Copyright (c) 2026 Wilkend. All rights reserved.
# Hantalk - proprietary software. See LICENSE at the repository root.
# Unauthorized copying, modification, or redistribution is prohibited.

"""Path banner — kat koulè ki anonse yon seksyon oswa yon inite.

Se lide ki pi entelijan nan ekran Duolingo yo: chak bandwòl gen pwòp
koulè li, donk chak seksyon jwenn yon idantite san yo pa desine okenn
imaj. Hantalk pa gen ilistrasyon ni maskòt — koulè ak tipografi se tout
sa nou genyen, epi sa ase.

Estrikti a:

    ┌──────────────────────────────────┬────┐
    │ SEKSYON 1 · DEBITAN              │    │   ← ti majiskil etenn
    │ 基礎一                            │ ⓘ  │   ← tit an chinwa
    │ Foundations 1                    │    │   ← tit an anglè
    └──────────────────────────────────┴────┘
                                        ↑
                            bouton gid la (opsyonèl)
"""

import flet as ft

from app import theme


def path_banner(
    kicker: str,
    traditional: str,
    english: str,
    bg: str,
    fg: str,
    on_action=None,
    action_icon: str = ft.Icons.LIST_ALT,
    progress: str = "",
) -> ft.Control:
    """Bandwòl plen lajè.

    `fg` se koulè tèks la SOU `bg`. Pè yo soti nan `theme.section_color()`,
    ki garanti omwen 4.5:1 — donk nou pa janm bezwen devine isit la.
    """
    head: list[ft.Control] = [
        ft.Text(kicker, size=theme.SIZE_LABEL, weight=ft.FontWeight.W_700,
                color=fg, opacity=0.75),
        ft.Text(traditional, font_family=theme.FONT_ZH, size=22,
                weight=ft.FontWeight.W_600, color=fg),
        ft.Text(english, size=theme.SIZE_SMALL, color=fg, opacity=0.85),
    ]
    if progress:
        head.append(ft.Container(height=2))
        head.append(
            ft.Text(progress, size=theme.SIZE_SMALL, weight=ft.FontWeight.W_600,
                    color=fg, opacity=0.9)
        )

    row: list[ft.Control] = [
        ft.Container(expand=True, content=ft.Column(spacing=3, controls=head))
    ]

    if on_action is not None:
        row.append(
            ft.Container(
                width=1, height=54,
                bgcolor=fg, opacity=0.28,
                margin=ft.Margin.symmetric(horizontal=12),
            )
        )
        row.append(
            ft.Container(
                padding=ft.Padding.all(8),
                border_radius=999,
                on_click=on_action,
                content=ft.Icon(action_icon, size=24, color=fg),
            )
        )

    return ft.Container(
        bgcolor=bg,
        border_radius=theme.RADIUS_LG,
        padding=ft.Padding.symmetric(vertical=16, horizontal=18),
        content=ft.Row(
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=row,
        ),
    )
