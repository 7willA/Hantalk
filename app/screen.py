# Copyright (c) 2026 Wilkend. All rights reserved.
# Hantalk - proprietary software. See LICENSE at the repository root.
# Unauthorized copying, modification, or redistribution is prohibited.


import flet as ft

from app import theme

SAFE_PADDING = 10


def screen(
    route: str,
    controls: list[ft.Control],
    *,
    centered: bool = True,
    scroll: bool = True,
    spacing: int = 0,
    padding: int | ft.Padding = 20,
    bgcolor: str | None = None,
    safe_bottom: bool = True,
    **view_kwargs,
) -> ft.View:
    
    align = (ft.MainAxisAlignment.CENTER if centered
             else ft.MainAxisAlignment.START)

    return ft.View(
        route=route,
        bgcolor=bgcolor or theme.BACKGROUND,
        padding=padding if isinstance(padding, ft.Padding)
        else ft.Padding.all(padding),
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.SafeArea(
                expand=True,
                minimum_padding=SAFE_PADDING,
                avoid_intrusions_bottom=safe_bottom,
                content=ft.Column(
                    expand=True,
                    spacing=spacing,
                    scroll=ft.ScrollMode.AUTO if scroll else None,
                    alignment=align,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=controls,
                ),
            )
        ],
        **view_kwargs,
    )


# ── Only one side ──────────────────────────────────────────

def _one_side(control: ft.Control, *, top: bool, bottom: bool) -> ft.SafeArea:
    
    return ft.SafeArea(
        content=control,
        avoid_intrusions_top=top,
        avoid_intrusions_bottom=bottom,
        avoid_intrusions_left=False,
        avoid_intrusions_right=False,
        minimum_padding=0,
        expand=getattr(control, "expand", None),
    )


def safe_top(control: ft.Control) -> ft.SafeArea:
    """For a header stuck at the top of the screen (notch, status bar)."""
    return _one_side(control, top=True, bottom=False)


def safe_bottom(control: ft.Control) -> ft.SafeArea:
    return _one_side(control, top=False, bottom=True)
