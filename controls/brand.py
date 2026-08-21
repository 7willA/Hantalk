# Copyright (c) 2026 Wilkend. All rights reserved.
# Hantalk - proprietary software. See LICENSE at the repository root.
# Unauthorized copying, modification, or redistribution is prohibited.

"""Brand — logo Hantalk"""

import flet as ft

from app import theme

MARK_SRC = "/images/logo_tile.png"
WORDMARK_SRC = "/images/logo_wordmark.png"


def _fallback(size: int, radius: int) -> ft.Control:
   
    return ft.Container(
        width=size,
        height=size,
        bgcolor=theme.PRIMARY,
        border_radius=radius,
        alignment=ft.Alignment.CENTER,
        content=ft.Text("H", size=int(size * 0.52),
                        weight=ft.FontWeight.BOLD, color=theme.WHITE),
    )


def logo_mark(size: int = 88) -> ft.Control:
    return ft.Image(
        src=MARK_SRC,
        width=size,
        height=size,
        fit=ft.BoxFit.CONTAIN,
        filter_quality=ft.FilterQuality.HIGH,
        error_content=_fallback(size, int(size * 0.27)),
    )


def logo_wordmark(width: int = 200) -> ft.Control:
    return ft.Image(
        src=WORDMARK_SRC,
        width=width,
        fit=ft.BoxFit.CONTAIN,
        filter_quality=ft.FilterQuality.HIGH,
        error_content=_fallback(int(width * 0.33), int(width * 0.09)),
    )
