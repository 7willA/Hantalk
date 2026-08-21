# Copyright (c) 2026 Wilkend. All rights reserved.
# Hantalk - proprietary software. See LICENSE at the repository root.
# Unauthorized copying, modification, or redistribution is prohibited.

"""Section model — a group of units that makes up a level in the course.

Flutter counterpart: none — this is a new level.

THE HIERARCHY

    Section    "Beginner 1"                ← this file
      └── Unit = a Lesson (你叫什麼名字)     ← models/lesson.py
            └── Activity = a node           ← models/activity.py

BUILT TO GROW

  You said you'll be adding many sections and many levels later. So:

  1. `Section` does NOT hold `Lesson` objects — it holds their NUMBERS
     (`lesson_numbers`). So adding a section means writing one line in
     `data/lessons/all_lessons.py`, without touching the model.

  2. The color is an INDEX (`color_index`), not a hex value. The
     palette lives in `app/theme.py`. Once you have 20 sections, the
     index wraps around the palette automatically — you're never
     blocked because you're out of colors.

  3. `level` is free text ("Beginner", "Intermediate", "HSK 3"...). We
     didn't make it an Enum because an Enum would mean every new level
     needs a code change.
"""

from dataclasses import dataclass, field


@dataclass
class Section:
    number: int
    """Display order — 1, 2, 3... This is what shows in 'SECTION 2'."""

    traditional: str
    """The title in Chinese, for the banner (e.g. 基礎一)."""

    english: str
    """The title in English (e.g. 'Foundations 1')."""

    level: str = ""
    """Free level label: 'Beginner', 'Intermediate', 'HSK 3'..."""

    description: str = ""
    """A sentence saying what the person will be able to do after this section."""

    lesson_numbers: list[int] = field(default_factory=list)
    """The lesson numbers, in order. These are what make up the section's units."""

    color_index: int = 0
    """Index into the section palette (`theme.section_color()`)."""

    is_locked: bool = False

    # ── computed info ────────────────────────────────

    @property
    def unit_count(self) -> int:
        return len(self.lesson_numbers)

    def progress(self, lessons_by_number: dict[int, object]) -> float:
        """Average progress of the units, between 0.0 and 1.0.

        We pass the dictionary in as an argument instead of importing
        the data here. This keeps `models/` clean: a model shouldn't
        know where the data comes from — otherwise you'll get circular
        imports as the app grows.
        """
        if not self.lesson_numbers:
            return 0.0
        total = 0.0
        for n in self.lesson_numbers:
            lesson = lessons_by_number.get(n)
            total += getattr(lesson, "progress", 0.0) if lesson else 0.0
        return total / len(self.lesson_numbers)

    def completed_units(self, lessons_by_number: dict[int, object]) -> int:
        """How many units are fully finished — for the '3 / 6' count."""
        done = 0
        for n in self.lesson_numbers:
            lesson = lessons_by_number.get(n)
            if lesson is not None and getattr(lesson, "progress", 0.0) >= 1.0:
                done += 1
        return done

    def label(self) -> str:
        """'SECTION 2' — the small caps label sitting above the banner."""
        return f"SECTION {self.number}"
