# Copyright (c) 2026 Wilkend. All rights reserved.
# Hantalk - proprietary software. See LICENSE at the repository root.
# Unauthorized copying, modification, or redistribution is prohibited.

"""Test tool for the data layer — run it in the terminal, not in the app.

    python check_data.py

It shows the Section → Unit → Node structure without opening the app.
Use it every time you change `ALL_SECTIONS` or a lesson: if you make
a mistake (a lesson in two sections, a forgotten lesson), it will tell
you right away instead of the unit just disappearing from Home with no explanation.
"""

from app import theme
from data.lessons.all_lessons import (
    ALL_LESSONS,
    ALL_SECTIONS,
    LESSONS_BY_NUMBER,
    current_lesson,
    section_lessons,
)
from models.activity import KIND_ORDER, build_activities

MARK = {"done": "●", "active": "◉", "locked": "○"}


def main() -> None:
    total_nodes = len(ALL_LESSONS) * len(KIND_ORDER)
    print()
    print("═" * 62)
    print(f"  {len(ALL_SECTIONS)} seksyon · {len(ALL_LESSONS)} inite · "
          f"{total_nodes} nœud")
    print("═" * 62)

    for section in ALL_SECTIONS:
        bg, _fg = theme.section_color(section.color_index)
        done = section.completed_units(LESSONS_BY_NUMBER)
        pct = section.progress(LESSONS_BY_NUMBER)

        print()
        print(f"  {section.label()} · {section.traditional} "
              f"{section.english}  [{section.level}]  {bg}")
        print(f"  {section.description}")
        print(f"  {done}/{section.unit_count} inite fini · pwogrè {pct:.0%}")
        print("  " + "─" * 58)

        for lesson in section_lessons(section):
            marks = "".join(MARK[a.state.value]
                            for a in build_activities(lesson))
            lock = "  (bloke)" if lesson.is_locked else ""
            content = "" if lesson.has_content else "  [tit sèlman]"
            print(f"    Inite {lesson.number:2}  {marks}  "
                  f"{lesson.traditional}{lock}{content}")

    print()
    print("─" * 62)
    cur = current_lesson()
    print(f"  Kontinye sou: Inite {cur.number} · {cur.traditional}")
    print(f"  Nœud li yo:")
    for a in build_activities(cur):
        count = a.count_label() or "—"
        print(f"    {MARK[a.state.value]} {a.title:10} {count:12} {a.route}")
    print()
    print("  Lejand:  ● fini   ◉ aktif   ○ bloke")
    print()


if __name__ == "__main__":
    main()
