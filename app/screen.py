# Copyright (c) 2026 Wilkend. All rights reserved.
# Hantalk - proprietary software. See LICENSE at the repository root.
# Unauthorized copying, modification, or redistribution is prohibited.

"""Screen — kokiy la chak ekran Hantalk chita ladan l.

POUKISA MODIL SA A EGZISTE

  Chak `ft.View` te gen menm dis liy repete: menm padding, menm
  `ft.Column` ki santre, menm `scroll`. Lè logo a te kole sou bar
  estati iPhone 11 la, fòk nou te ale korije chak fichye youn pa youn.

  Kounye a gen yon sèl kote. Yon nouvo ekran ekri:

      return screen("/wout-mwen", [
          ft.Text("Bonjou"),
      ])

  epi li resevwa SafeArea a, padding lan ak defilman an gratis. Si yon
  jou nou dwe chanje yon bagay pou tout app la — yon nouvo aparèy ak yon
  lòt fòm notch, yon padding diferan — se yon sèl liy pou n chanje.

KISA `ft.SafeArea` YE

  Sou telefòn modèn, ekran an pa tout pou app la: gen notch la, bar
  estati a, ak ti bar jès la anba. `ft.SafeArea` mande sistèm nan ki
  wotè zòn sa yo ye epi li kite plas la. Nou pa ka kode yon chif fiks:
  li diferan sou chak modèl telefòn.

  `SAFE_PADDING` se yon ti espas ANPLIS, pou aparèy ki pa gen notch
  ditou (Android ansyen, mòd Desktop) pa gen kontni ki kole sou bò a.
"""

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
    """Bati yon `ft.View` ki respekte bò aparèy la.

    route       wout la, egz. "/login"
    controls    kontni ekran an, youn anba lòt
    centered    True  → kontni an santre vètikalman (ekran auth, eta vid)
                False → li kòmanse anwo a (lis, paj ki long)
    scroll      kite defilman an louvri. Mete False sèlman si ekran an
                gen pwòp lis li ki defile deja — de defilman youn nan lòt
                bay yon santiman dwòl.
    padding     espas ozalantou kontni an, ANNDAN zòn ki an sekirite a
    safe_bottom False lè ekran an gen yon `navigation_bar`: bar la deja
                okipe zòn anba a, donk kontni an pa bezwen evite l de fwa
    **view_kwargs  tout lòt bagay `ft.View` aksepte (appbar,
                navigation_bar, floating_action_button…)
    """
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


# ── Sèlman yon bò ──────────────────────────────────────────

def _one_side(control: ft.Control, *, top: bool, bottom: bool) -> ft.SafeArea:
    """Kite plas pou yon SÈL bò aparèy la, san manyen mizanpaj la.

    `screen()` bon pou ekran ki senp. Men anpil ekran Hantalk bati yon
    pil: yon header ki kole anwo, yon kò ki defile, yon bar aksyon ki
    kole anba. Si nou te vlope tout pil la nan yon SafeArea, header la
    t ap pèdi koulè fon li nan zòn notch la — sa parèt kase.

    Donk nou vlope MOSO a: header la resevwa espas anwo a, bar anba a
    resevwa espas anba a, epi kò a pa chanje ditou.

    `expand` kopye sou SafeArea a paske se li ki nan Column lan kounye
    a — san sa yon kò ki te ranpli ekran an t ap tonbe nan wotè kontni
    li sèlman.
    """
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
    """Pou header ki kole anwo ekran an (notch, bar estati)."""
    return _one_side(control, top=True, bottom=False)


def safe_bottom(control: ft.Control) -> ft.SafeArea:
    """Pou bar aksyon ki kole anba a (bar jès iPhone la).

    Pa bezwen l lè ekran an gen yon `navigation_bar`: Flet mete bar sa a
    deyò kò a epi sistèm nan deja kite plas pou li.
    """
    return _one_side(control, top=False, bottom=True)
