# Copyright (c) 2026 Wilkend. All rights reserved.
# Hantalk - proprietary software. See LICENSE at the repository root.
# Unauthorized copying, modification, or redistribution is prohibited.

"""Brand — logo Hantalk la.

Anvan, chak ekran te desine yon kare wouj ak yon "H" ladan l — yon
plas rezève. Kounye a se vre logo a.

DE FICHYE, DE SÈVIS

  logo_tile.png     204×204, squircle la ak fon blan li — sa se
                    logo a jan li ye. Li mache sou nenpòt koulè fon.
  logo_wordmark.png 605×200, icon la + mo "Hantalk" la.

  Tou de gen kwen transparan, donk nou pa bezwen okenn `bgcolor`
  dèyè yo — yo koupe pwòp fòm yo.

  Yo soti nan `logo6.jpeg` (koupe epi netwaye), donk si w chanje logo
  a yon jou, se de fichye sa yo pou w ranplase — okenn kòd pa chanje.

`error_content` LA ENPÒTAN

  Si yon fichye asèt manke (yon move chemen, yon bilding APK ki bliye
  yo), Flet ta montre yon bwat vid san esplikasyon. Ak `error_content`
  nou tonbe sou ansyen kare "H" la: ekran an rete lizib epi ou wè la
  menm gen yon pwoblèm asèt.
"""

import flet as ft

from app import theme

MARK_SRC = "/images/logo_tile.png"
WORDMARK_SRC = "/images/logo_wordmark.png"


def _fallback(size: int, radius: int) -> ft.Control:
    """Ansyen kare 'H' la — sèlman si imaj la pa ka chaje."""
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
    """Icon la sèlman — kare, ak kwen awondi li deja ladan l."""
    return ft.Image(
        src=MARK_SRC,
        width=size,
        height=size,
        fit=ft.BoxFit.CONTAIN,
        filter_quality=ft.FilterQuality.HIGH,
        error_content=_fallback(size, int(size * 0.27)),
    )


def logo_wordmark(width: int = 200) -> ft.Control:
    """Icon la + mo 'Hantalk' la, nan tipografi mak la."""
    return ft.Image(
        src=WORDMARK_SRC,
        width=width,
        fit=ft.BoxFit.CONTAIN,
        filter_quality=ft.FilterQuality.HIGH,
        error_content=_fallback(int(width * 0.33), int(width * 0.09)),
    )
