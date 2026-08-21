# Copyright (c) 2026 Wilkend. All rights reserved.
# Hantalk - proprietary software. See LICENSE at the repository root.
# Unauthorized copying, modification, or redistribution is prohibited.

import copy

from data.lessons.lesson_01 import LESSON_01
from data.lessons.lesson_02 import LESSON_02
from models.lesson import Lesson
from models.section import Section

ALL_LESSONS = [
    # 01 — 叫 / 是, questions with 嗎 and 呢
    LESSON_01,
    # 02 — greetings, 很 + adjective, 也
    LESSON_02,
    # 03 — 喜歡 + verb, negation with 不
    Lesson(3, "我喜歡聽台語歌", "I Like Listening to Taiwanese Songs"),
    # 04 — measure words, price, 這 / 那
    Lesson(4, "這件衣服多少錢？", "How Much Is This Shirt?"),
    # 05 — 有 / 沒有, 幾, family
    Lesson(5, "我有兩個姐姐", "I Have Two Older Sisters", is_locked=True),
    # 06 — 想, 的 as nominalizer
    Lesson(6, "我想買一杯珍奶", "I Want to Buy a Bubble Tea",
           is_locked=True),
    # 07 — degree complement with 得
    Lesson(7, "你的中文說得很好", "Your Chinese Sounds Really Good",
           is_locked=True),
    # 08 — relative clause with 的
    Lesson(8, "這是我昨天買的手機", "This Is the Phone I Bought Yesterday",
           is_locked=True),
    # 09 — 在, location words
    Lesson(9, "你家在哪裡？", "Where Is Your Home?", is_locked=True),
    # 10 — 到 … 去 + 了 (completed action)
    Lesson(10, "我到台南去了", "I Went to Tainan", is_locked=True),
    # 11 — time expressions, 幾點
    Lesson(11, "你幾點下班？", "What Time Do You Get Off Work?",
           is_locked=True),
    # 12 — duration with 了
    Lesson(12, "我在台灣住了三年", "I Lived in Taiwan for Three Years",
           is_locked=True),
]


def fill_demo_content(lessons: list[Lesson]) -> None:
    """Borrow content from lessons 1/2 for lessons that don't have their own yet.

    `copy.deepcopy` matters here: without it, all lessons would share the SAME
    dialogue object, and changing one would change them all — the same trap
    as using a list as a default value.
    """
    sources = [LESSON_01, LESSON_02]

    for i, lesson in enumerate(lessons):
        src = sources[i % len(sources)]

        if lesson.dialogue is None:
            lesson.dialogue = copy.deepcopy(src.dialogue)
        if not lesson.vocabulary:
            lesson.vocabulary = copy.deepcopy(src.vocabulary)
        if not lesson.patterns:
            lesson.patterns = copy.deepcopy(src.patterns)
        if not lesson.culture_note:
            lesson.culture_note = src.culture_note


fill_demo_content(ALL_LESSONS)


# ══════════════════════════════════════════════════════════
# SECTIONS — Section → Unit (= Lesson) → Activity
# ══════════════════════════════════════════════════════════
#
# TO ADD A SECTION, there's just one thing to do: add a `Section`
# to the list below and set its lesson numbers. No code to touch.
# `color_index` wraps around the palette in `app/theme.py`, so you never
# run out of colors — even with 30 sections.
#
# RULE: every lesson must appear in EXACTLY one section.
# `_check_sections()` below verifies this on every startup.

ALL_SECTIONS = [
    Section(
        number=1,
        traditional="基礎一",
        english="Foundations 1",
        level="Beginner",
        description="Say your name, greet people, and ask how much something costs.",
        lesson_numbers=[1, 2, 3, 4],
        color_index=0,
    ),
    Section(
        number=2,
        traditional="基礎二",
        english="Foundations 2",
        level="Beginner",
        description="Talk about your family, what you want, and describe how someone does something.",
        lesson_numbers=[5, 6, 7, 8],
        color_index=1,
    ),
    Section(
        number=3,
        traditional="日常生活",
        english="Everyday Life",
        level="Intermediate",
        description="Where, when, and what already happened — talk about your day.",
        lesson_numbers=[9, 10, 11, 12],
        color_index=2,
    ),
]


def _apply_sections() -> None:
    """Set `section_number` on every lesson from ALL_SECTIONS.

    The sections are the source of truth. The lesson just carries a copy
    of the number for quick lookup — so we can't end up with two facts
    that disagree.
    """
    for section in ALL_SECTIONS:
        for number in section.lesson_numbers:
            for lesson in ALL_LESSONS:
                if lesson.number == number:
                    lesson.section_number = section.number
                    break


def _check_sections() -> None:
    """Check that every lesson is in exactly one section, and none is missing.

    We run this check on startup because it's an easy mistake to make when
    adding sections (copying a line and forgetting to change the numbers),
    and it would show up as a unit disappearing from Home — hard to figure out.
    """
    seen: dict[int, int] = {}
    for section in ALL_SECTIONS:
        for number in section.lesson_numbers:
            if number in seen:
                raise ValueError(
                    f"Lesson {number} is in section {seen[number]} AND "
                    f"section {section.number}. It must be in exactly one."
                )
            seen[number] = section.number

    missing = [l.number for l in ALL_LESSONS if l.number not in seen]
    if missing:
        raise ValueError(
            f"These lessons aren't in any section: {missing}. "
            f"Add them to a Section in ALL_SECTIONS."
        )

    unknown = [n for n in seen if not any(l.number == n for l in ALL_LESSONS)]
    if unknown:
        raise ValueError(
            f"ALL_SECTIONS references lessons that don't exist: {unknown}."
        )


_apply_sections()
_check_sections()


# ── Lookup ────────────────────────────────────────────────

LESSONS_BY_NUMBER: dict[int, Lesson] = {l.number: l for l in ALL_LESSONS}


def get_lesson(number: int) -> Lesson:
    """Get a lesson by its number. Raises KeyError if it doesn't exist."""
    lesson = LESSONS_BY_NUMBER.get(number)
    if lesson is None:
        raise KeyError(f"No lesson {number}")
    return lesson


def get_section(number: int) -> Section:
    """Get a section by its number."""
    for section in ALL_SECTIONS:
        if section.number == number:
            return section
    raise KeyError(f"No section {number}")


def section_lessons(section: Section) -> list[Lesson]:
    """A section's units, in order."""
    return [LESSONS_BY_NUMBER[n] for n in section.lesson_numbers
            if n in LESSONS_BY_NUMBER]


def section_of(lesson: Lesson) -> Section:
    """Which section a unit belongs to."""
    return get_section(lesson.section_number)


def current_lesson() -> Lesson:
    """First unit that isn't finished and isn't locked — what 'Continue' opens."""
    for lesson in ALL_LESSONS:
        if not lesson.is_locked and lesson.progress < 1.0:
            return lesson
    return ALL_LESSONS[0]
