# Copyright (c) 2026 Wilkend. All rights reserved.
# Hantalk - proprietary software. See LICENSE at the repository root.
# Unauthorized copying, modification, or redistribution is prohibited.

"""Path node — a dot on the path.

Used in two places:
  - Home        → each node is a UNIT (it shows the unit number)
  - Unit screen → each node is an ACTIVITY (it shows an icon)

THREE STATES

  DONE    filled with the section color, with a checkmark
  ACTIVE  filled, BIGGER, with a ring around it — this is what draws the eye
  LOCKED  flat gray, dim icon

THE ZIGZAG

  `node_offset()` is the only place the horizontal position is
  calculated. Today it gives a simple zigzag. When we want the curved
  Duolingo-style path, only this function and an `ft.canvas` for the
  connecting line need to change — no screen needs to know.

  We only use POSITIVE margins (left OR right), because negative
  margins are not reliable in Flet.
"""

import flet as ft

from app import theme
from models.activity import ActivityKind, ActivityState

# Icon for each activity type. They live here, not in `models/`,
# because an icon is a display decision.
KIND_ICONS: dict[ActivityKind, str] = {
    ActivityKind.DIALOGUE: ft.Icons.FORUM,
    ActivityKind.VOCABULARY: ft.Icons.STYLE,
    ActivityKind.EXERCISES: ft.Icons.CHECK_CIRCLE_OUTLINE,
    ActivityKind.PHONETICS: ft.Icons.TRANSLATE,
    ActivityKind.TONES: ft.Icons.GRAPHIC_EQ,
    ActivityKind.AI: ft.Icons.MIC,
}

SIZE_ACTIVE = 84
SIZE_NORMAL = 68

# The zigzag pattern. It loops, so it works with any number of nodes.
# Positive value = push right, negative = push left, in pixels.
_ZIGZAG = (0, 52, 74, 52, 0, -52, -74, -52)


def node_offset(index: int) -> int:
    """Horizontal offset for node number `index`."""
    return _ZIGZAG[index % len(_ZIGZAG)]


def _circle(state: ActivityState, color: str, inner: ft.Control) -> ft.Control:
    """The dot — its size and color change based on the state."""
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

    # The ring: a second, bigger circle behind the first one.
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
    """What's inside the dot: a checkmark if done, otherwise an icon or number."""
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
    """A full node: the dot + its label below it, offset along the path."""
    locked = state is ActivityState.LOCKED

    # NOTE: a locked node STAYS tap-able. It's up to the screen to
    # decide what to show — usually `locked_callout()`, which explains
    # why it's locked. A circle that doesn't respond at all makes
    # people think the app is broken.
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
