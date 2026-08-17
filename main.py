# Copyright (c) 2026 Wilkend. All rights reserved.
# Hantalk - proprietary software. See LICENSE at the repository root.
# Unauthorized copying, modification, or redistribution is prohibited.

"""Hantalk — entry point"""

import flet as ft

from app import router, theme
from services import settings_service


def main(page: ft.Page):
    page.title = "Hantalk"
    theme.apply_theme(page)

    async def route_change(_):
        page.views.clear()
        page.views.append(router.resolve(page, page.route))
        page.update()

    async def view_pop(_):
        """Bouton 'back' Android la."""
        if len(page.views) > 1:
            page.views.pop()
            await page.push_route(page.views[-1].route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    # page.route deja "/" nan demaraj, donk push_route("/") pa fè anyen.
    page.views.append(router.resolve(page, page.route))
    page.update()

    async def load_settings():
        """Li paramèt ki sove yo yon sèl fwa, epi redesine ekran an.

        LÒD LA ENPÒTAN. Sa a dwe kouri APRE premye View la nan
        `page.views`, pa anvan. De rezon:

          1. `ft.SharedPreferences` se yon Service ki atache sou yon View
             (gade `app/router.py`). Si pa gen View, pa gen sèvis.
          2. `page.update()` pase pa `page.views[0]`. Si lis la vid, Flet
             voye `RuntimeError("views list is empty.")` epi app la tonbe.

        Splash la dire 2 segond, donk lekti a gen tan fini anvan premye
        ekran ki bezwen paramèt yo parèt. Si li echwe, valè pa defo yo
        rete anplas epi app la kontinye mache.
        """
        try:
            await settings_service.load()
        except Exception:
            pass          # valè pa defo yo rete anplas
        try:
            page.update()
        except Exception:
            pass          # ekran an poko pare — pa grav, l ap desine apre

    page.run_task(load_settings)


ft.run(main, assets_dir="assets")
