# Copyright (c) 2026 Wilkend. All rights reserved.
# Hantalk - proprietary software. See LICENSE at the repository root.
# Unauthorized copying, modification, or redistribution is prohibited.

"""Path node — yon sib sou chemen an.

Sèvi de kote:
  - Home        → chak nœud se yon INITE (li montre nimewo inite a)
  - Unit screen → chak nœud se yon AKTIVITE (li montre yon ikon)

TWA ETA

  DONE    plen ak koulè seksyon an, ak yon ✓
  ACTIVE  plen, PI GWO, ak yon bag alantou — se li ki rele je a
  LOCKED  gri plat, ikon etenn

ZIGZAG LA

  `node_offset()` se sèl kote pozisyon orizontal la kalkile. Jodi a li
  bay yon zigzag senp. Lè nou vle chemen koube Duolingo a, se sèl
  fonksyon sa a ak yon `ft.canvas` pou liy lan ki chanje — okenn ekran
  pa bezwen konnen.

  Nou sèvi ak marge POZITIF sèlman (goch OSWA dwat), paske marge negatif
  pa fyab nan Flet.
"""

import flet as ft

from app import theme
from models.activity import ActivityKind, ActivityState

# Ikon pou chak kalite aktivite. Yo viv isit la, pa nan `models/`,
# paske yon ikon se yon desizyon afichaj.
KIND_ICONS: dict[ActivityKind, str] = {
    ActivityKind.DYALOG: ft.Icons.FORUM,
    ActivityKind.VOKABILE: ft.Icons.STYLE,
    ActivityKind.EGZESIS: ft.Icons.CHECK_CIRCLE_OUTLINE,
    ActivityKind.FONETIK: ft.Icons.TRANSLATE,
    ActivityKind.TON: ft.Icons.GRAPHIC_EQ,
    ActivityKind.AI: ft.Icons.MIC,
}

SIZE_ACTIVE = 84
SIZE_NORMAL = 68

# Pwofil zigzag la. Li anwole, donk li mache ak nenpòt kantite nœud.
# Valè pozitif = pouse adwat, negatif = pouse agoch, an piksèl.
_ZIGZAG = (0, 52, 74, 52, 0, -52, -74, -52)


def node_offset(index: int) -> int:
    """Dekalaj orizontal nœud nimewo `index` la."""
    return _ZIGZAG[index % len(_ZIGZAG)]


def _circle(state: ActivityState, color: str, inner: ft.Control) -> ft.Control:
    """Sib la — gwosè ak koulè li chanje dapre eta a."""
    active = state is ActivityState.ACTIVE
    locked = state is ActivityState.LOCKED
    size = SIZE_ACTIVE if active else SIZE_NORMAL

    circle = ft.Container(
        width=size,
        height=size,
        border_radius=999,
        alignment=ft.Alignment.CENTER,
        bgcolor=theme.SURFACE_VARIANT if locked else color,
        content=inner,
    )

    if not active:
        return circle

    # Bag la: yon dezyèm sèk pi gwo dèyè premye a.
    return ft.Container(
        width=size + 14,
        height=size + 14,
        border_radius=999,
        alignment=ft.Alignment.CENTER,
        border=ft.Border.all(3, color),
        content=circle,
    )


def _inner(state: ActivityState, on_color: str, icon: str | None,
           text: str | None) -> ft.Control:
    """Sa ki anndan sib la: ✓ si fini, sinon ikon oswa nimewo."""
    locked = state is ActivityState.LOCKED
    fg = theme.TEXT_MUTED if locked else on_color

    if state is ActivityState.DONE:
        return ft.Icon(ft.Icons.CHECK, size=32, color=fg)
    if icon is not None:
        return ft.Icon(icon, size=30, color=fg)
    return ft.Text(str(text), size=26, weight=ft.FontWeight.BOLD, color=fg)


def path_node(
    label: str,
    state: ActivityState,
    color: str,
    on_color: str,
    index: int,
    on_click=None,
    icon: str | None = None,
    text: str | None = None,
    sublabel: str = "",
) -> ft.Control:
    """Yon nœud konplè: sib la + tit la anba li, dekale sou chemen an."""
    locked = state is ActivityState.LOCKED

    # NÒT: yon nœud bloke RETE tap-able. Se ekran an ki deside sa pou
    # montre — jeneralman `locked_callout()` ki esplike poukisa li bloke.
    # Yon sèk ki pa reponn ditou fè moun panse app la kase.
    node = ft.Container(
        on_click=on_click,
        content=ft.Column(
            spacing=8,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                _circle(state, color, _inner(state, on_color, icon, text)),
                ft.Column(
                    spacing=1,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text(
                            label,
                            size=theme.SIZE_BODY,
                            weight=ft.FontWeight.W_600,
                            color=theme.TEXT_MUTED if locked else theme.TEXT,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        *([ft.Text(sublabel, size=theme.SIZE_SMALL,
                                   color=theme.TEXT_MUTED,
                                   text_align=ft.TextAlign.CENTER)]
                          if sublabel else []),
                    ],
                ),
            ],
        ),
    )

    offset = node_offset(index)
    margin = (ft.Margin.only(left=offset * 2) if offset > 0
              else ft.Margin.only(right=-offset * 2) if offset < 0
              else None)

    return ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[ft.Container(content=node, margin=margin)],
    )
