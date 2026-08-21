# Copyright (c) 2026 Wilkend. All rights reserved.
# Hantalk - proprietary software. See LICENSE at the repository root.
# Unauthorized copying, modification, or redistribution is prohibited.

import flet as ft

from app import theme


def _pointer(color: str) -> ft.Control:
    """Small triangle that points at the node — a square turned 45°."""
    return ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            ft.Container(
                width=18,
                height=18,
                bgcolor=color,
                rotate=ft.Rotate(0.785),      # 45 degrees, in radians
                margin=ft.Margin.only(bottom=-9),
            )
        ],
    )


def node_callout(
    title: str,
    subtitle: str,
    bg: str,
    fg: str,
    action_label: str,
    on_action=None,
    meta: str = "",
) -> ft.Control:
    """The card, with its pointer arrow.

    `bg`/`fg` come from `theme.section_color()`, so the text stays
    easy to read no matter which section it is in.
    """
    body: list[ft.Control] = [
        ft.Text(title, size=theme.SIZE_H3, weight=ft.FontWeight.W_700,
                color=fg),
        ft.Text(subtitle, size=theme.SIZE_SMALL, color=fg, opacity=0.85),
    ]
    if meta:
        body.append(
            ft.Text(meta, size=theme.SIZE_LABEL, weight=ft.FontWeight.W_600,
                    color=fg, opacity=0.75)
        )

    body.append(ft.Container(height=6))
    body.append(
        ft.Container(
            height=46,
            bgcolor=theme.WHITE,
            border_radius=theme.RADIUS_SM,
            alignment=ft.Alignment.CENTER,
            on_click=on_action,
            content=ft.Text(action_label, size=theme.SIZE_SMALL,
                            weight=ft.FontWeight.W_700, color=bg),
        )
    )

    return ft.Column(
        spacing=0,
        controls=[
            _pointer(bg),
            ft.Container(
                bgcolor=bg,
                border_radius=theme.RADIUS_LG,
                padding=ft.Padding.all(16),
                margin=ft.Margin.symmetric(horizontal=8),
                content=ft.Column(spacing=3, controls=body),
            ),
        ],
    )


def locked_callout(title: str, reason: str) -> ft.Control:
    """The "off" version, used for a node that is locked."""
    return ft.Column(
        spacing=0,
        controls=[
            _pointer(theme.SURFACE_VARIANT),
            ft.Container(
                bgcolor=theme.SURFACE_VARIANT,
                border=ft.Border.all(1, theme.OUTLINE),
                border_radius=theme.RADIUS_LG,
                padding=ft.Padding.all(16),
                margin=ft.Margin.symmetric(horizontal=8),
                content=ft.Row(
                    spacing=12,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Icon(ft.Icons.LOCK, size=22,
                                color=theme.TEXT_MUTED),
                        ft.Column(
                            spacing=2,
                            expand=True,
                            controls=[
                                ft.Text(title, size=theme.SIZE_BODY,
                                        weight=ft.FontWeight.W_600,
                                        color=theme.TEXT_SECONDARY),
                                ft.Text(reason, size=theme.SIZE_SMALL,
                                        color=theme.TEXT_MUTED),
                            ],
                        ),
                    ],
                ),
            ),
        ],
    )
