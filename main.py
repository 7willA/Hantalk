# Copyright (c) 2026 Wilkend. All rights reserved.
# Hantalk - proprietary software. See LICENSE at the repository root.
# Unauthorized copying, modification, or redistribution is prohibited.

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
        if len(page.views) > 1:
            page.views.pop()
            await page.push_route(page.views[-1].route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    page.views.append(router.resolve(page, page.route))
    page.update()

    async def load_settings():
        
        try:
            await settings_service.load()
        except Exception:
            pass         
        try:
            page.update()
        except Exception:
            pass          

    page.run_task(load_settings)


ft.run(main, assets_dir="assets")
