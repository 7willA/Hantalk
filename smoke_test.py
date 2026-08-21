# Copyright (c) 2026 Wilkend. All rights reserved.
# Hantalk - proprietary software. See LICENSE at the repository root.
# Unauthorized copying, modification, or redistribution is prohibited.



import traceback

import flet as ft

from app import router
from data.lessons.all_lessons import ALL_LESSONS


class FakePage:
 

    route = "/"
    views: list = []

    def __init__(self):
        self.theme = None
        self.fonts = {}

    async def push_route(self, route):
        pass

  

    def run_task(self, fn, *args):
  
        import asyncio
        assert asyncio.iscoroutinefunction(fn), (
            f"run_task needs an `async def`, it received {fn!r}"
        )

    def update(self):
        pass


ROUTES = [
    "/", "/login", "/register", "/home", "/drills", "/practice", "/profile",
    "/settings",
    "/lesson/1", "/lesson/12", "/vocab/2", "/phonetic/1/0", "/phonetic/2/5",
    "/unit/1", "/unit/2", "/exercise/1", "/exercise/2", "/exercise/12",
    "/nope", "/lesson/99",
]


def main() -> int:
    failures = 0

    for route in ROUTES:
        try:
            view = router.resolve(FakePage(), route)
            assert isinstance(view, ft.View), f"{route} did not return a View"
            print(f"  ok   {route:<18} → {len(view.controls)} controls")
        except Exception:
            failures += 1
            print(f"  FAIL {route}")
            traceback.print_exc()

    print()
    for lesson in ALL_LESSONS:
        d = lesson.dialogue
        problems = []
        if d is None or not d.lines:
            problems.append("no dialogue")
        if not lesson.vocabulary:
            problems.append("no vocabulary")
        for p in lesson.patterns:
            if any(len(r) != len(p.headers) for r in p.rows):
                problems.append(f"crooked table in {p.title}")
        if problems:
            failures += 1
            print(f"  FAIL lesson {lesson.number}: {', '.join(problems)}")

    print()
    if failures:
        print(f"❌ {failures} problems")
    else:
        print(f"✅ {len(ROUTES)} routes + {len(ALL_LESSONS)} lessons — all good")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
