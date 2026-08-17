# Copyright (c) 2026 Wilkend. All rights reserved.
# Hantalk - proprietary software. See LICENSE at the repository root.
# Unauthorized copying, modification, or redistribution is prohibited.

"""Smoke test — konstwi chak ekran san louvri yon fenèt.

Kouri:  python smoke_test.py

Li pa teste sa ki parèt sou ekran an — li teste ke chak view konstwi
san erè API. Se pi bon fason pou pran yon `AttributeError` Flet anvan
w kouri app la.
"""

import traceback

import flet as ft

from app import router
from data.lessons.all_lessons import ALL_LESSONS


class FakePage:
    """Yon fo `ft.Page` ki jis vale tout sa view yo mande l."""

    route = "/"
    views: list = []

    def __init__(self):
        self.theme = None
        self.fonts = {}

    async def push_route(self, route):
        pass

    # Nòt: `page.pop_route()` PA egziste nan Flet 0.85. Nou pa mete l isit
    # espre — konsa si yon view sèvi avè l ankò, tès la ap kraze.

    def run_task(self, fn, *args):
        pass

    def update(self):
        pass


ROUTES = [
    "/", "/login", "/register", "/home", "/drills", "/practice", "/profile",
    "/lesson/1", "/lesson/12", "/vocab/2", "/phonetic/1/0", "/phonetic/2/5",
    "/nope", "/lesson/99",
]


def main() -> int:
    failures = 0

    for route in ROUTES:
        try:
            view = router.resolve(FakePage(), route)
            assert isinstance(view, ft.View), f"{route} pa bay yon View"
            print(f"  ok   {route:<18} → {len(view.controls)} kontwòl")
        except Exception:
            failures += 1
            print(f"  FAIL {route}")
            traceback.print_exc()

    print()
    for lesson in ALL_LESSONS:
        d = lesson.dialogue
        problems = []
        if d is None or not d.lines:
            problems.append("pa gen dyalòg")
        if not lesson.vocabulary:
            problems.append("pa gen vokabilè")
        for p in lesson.patterns:
            if any(len(r) != len(p.headers) for r in p.rows):
                problems.append(f"tablo kwochi nan {p.title}")
        if problems:
            failures += 1
            print(f"  FAIL leson {lesson.number}: {', '.join(problems)}")

    print()
    if failures:
        print(f"❌ {failures} pwoblèm")
    else:
        print(f"✅ {len(ROUTES)} wout + {len(ALL_LESSONS)} leson — tout bon")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
