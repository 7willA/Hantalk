# Copyright (c) 2026 Wilkend. All rights reserved.
# Hantalk - proprietary software. See LICENSE at the repository root.
# Unauthorized copying, modification, or redistribution is prohibited.

"""Tout 12 leson Hantalk yo, nan lòd.

Pwogresyon gramatikal la swiv yon kourikoulòm klasik pou debitan
(estrikti pa estrikti). Tit ak kontni yo se materyèl orijinal Hantalk.

ETA KOUNYE A
------------
Leson 1 ak 2 gen kontni reyèl (dyalòg, vokabilè, pattern, nòt kiltirèl).
Leson 3 rive 12 gen sèlman tit yo. `fill_demo_content()` prete kontni
leson 1/2 pou yo, konsa tout ekran yo gen kichòy pou montre pandan demo a.
Lè w ekri vre kontni yon leson, retire l nan prete a — sa a otomatik:
si `lesson.dialogue` pa `None`, fonksyon an pa manyen l.
"""

import copy

from data.lessons.lesson_01 import LESSON_01
from data.lessons.lesson_02 import LESSON_02
from models.lesson import Lesson
from models.section import Section

ALL_LESSONS = [
    # 01 — 叫 / 是, kesyon ak 嗎 ak 呢
    LESSON_01,
    # 02 — salitasyon, 很 + adjektif, 也
    LESSON_02,
    # 03 — 喜歡 + vèb, negasyon ak 不
    Lesson(3, "我喜歡聽台語歌", "I Like Listening to Taiwanese Songs"),
    # 04 — mo mezi, pri, 這 / 那
    Lesson(4, "這件衣服多少錢？", "How Much Is This Shirt?"),
    # 05 — 有 / 沒有, 幾, fanmi
    Lesson(5, "我有兩個姐姐", "I Have Two Older Sisters", is_locked=True),
    # 06 — 想, 的 kòm nominalizè
    Lesson(6, "我想買一杯珍奶", "I Want to Buy a Bubble Tea",
           is_locked=True),
    # 07 — konpleman degre ak 得
    Lesson(7, "你的中文說得很好", "Your Chinese Sounds Really Good",
           is_locked=True),
    # 08 — pwopozisyon relatif ak 的
    Lesson(8, "這是我昨天買的手機", "This Is the Phone I Bought Yesterday",
           is_locked=True),
    # 09 — 在, mo kote
    Lesson(9, "你家在哪裡？", "Where Is Your Home?", is_locked=True),
    # 10 — 到 … 去 + 了 (aksyon fini)
    Lesson(10, "我到台南去了", "I Went to Tainan", is_locked=True),
    # 11 — ekspresyon lè, 幾點
    Lesson(11, "你幾點下班？", "What Time Do You Get Off Work?",
           is_locked=True),
    # 12 — dire ak 了
    Lesson(12, "我在台灣住了三年", "I Lived in Taiwan for Three Years",
           is_locked=True),
]


def fill_demo_content(lessons: list[Lesson]) -> None:
    """Prete kontni leson 1/2 pou leson ki poko gen pa yo.

    `copy.deepcopy` enpòtan: san li, tout leson yo ta pataje MENM objè
    dyalòg la, epi chanje youn ta chanje tout — menm pyèj ak yon lis
    ki sèvi kòm valè pa defo.
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
# SEKSYON — Section → Unit (= Lesson) → Activity
# ══════════════════════════════════════════════════════════
#
# POU AJOUTE YON SEKSYON, se yon sèl bagay pou fè: ajoute yon `Section`
# nan lis la anba a epi mete nimewo leson li yo. Pa gen kòd pou touche.
# `color_index` anwole sou palèt la nan `app/theme.py`, donk ou pa janm
# bloke paske w manke koulè — menm ak 30 seksyon.
#
# REGLEMAN: chak leson dwe parèt nan EGZAKTEMAN yon sèl seksyon.
# `_check_sections()` anba a verifye sa nan chak demaraj.

ALL_SECTIONS = [
    Section(
        number=1,
        traditional="基礎一",
        english="Foundations 1",
        level="Debitan",
        description="Di non ou, salye moun, epi mande konbyen yon bagay koute.",
        lesson_numbers=[1, 2, 3, 4],
        color_index=0,
    ),
    Section(
        number=2,
        traditional="基礎二",
        english="Foundations 2",
        level="Debitan",
        description="Pale de fanmi ou, sa ou vle, epi dekri kijan yon moun fè yon bagay.",
        lesson_numbers=[5, 6, 7, 8],
        color_index=1,
    ),
    Section(
        number=3,
        traditional="日常生活",
        english="Everyday Life",
        level="Entèmedyè",
        description="Kote, lè, ak sa ki deja pase — rakonte jounen ou.",
        lesson_numbers=[9, 10, 11, 12],
        color_index=2,
    ),
]


def _apply_sections() -> None:
    """Mete `section_number` sou chak leson depi ALL_SECTIONS.

    Seksyon yo se sous verite a. Leson an jis pote yon kopi nimewo a
    pou rechèch rapid — konsa nou pa ka gen de reyalite ki pa dakò.
    """
    for section in ALL_SECTIONS:
        for number in section.lesson_numbers:
            for lesson in ALL_LESSONS:
                if lesson.number == number:
                    lesson.section_number = section.number
                    break


def _check_sections() -> None:
    """Verifye chak leson nan yon sèl seksyon, epi okenn pa bliye.

    Nou fè tès la nan demaraj paske se yon erè ki fasil pou fè lè w ap
    ajoute seksyon (kopye yon liy epi bliye chanje nimewo yo), epi li
    ta parèt kòm yon inite ki disparèt sou Home — difisil pou konprann.
    """
    seen: dict[int, int] = {}
    for section in ALL_SECTIONS:
        for number in section.lesson_numbers:
            if number in seen:
                raise ValueError(
                    f"Leson {number} nan seksyon {seen[number]} AK "
                    f"seksyon {section.number}. Li dwe nan yon sèl."
                )
            seen[number] = section.number

    missing = [l.number for l in ALL_LESSONS if l.number not in seen]
    if missing:
        raise ValueError(
            f"Leson sa yo pa nan okenn seksyon: {missing}. "
            f"Ajoute yo nan yon Section nan ALL_SECTIONS."
        )

    unknown = [n for n in seen if not any(l.number == n for l in ALL_LESSONS)]
    if unknown:
        raise ValueError(
            f"ALL_SECTIONS pale de leson ki pa egziste: {unknown}."
        )


_apply_sections()
_check_sections()


# ── Rechèch ────────────────────────────────────────────────

LESSONS_BY_NUMBER: dict[int, Lesson] = {l.number: l for l in ALL_LESSONS}


def get_lesson(number: int) -> Lesson:
    """Jwenn yon leson pa nimewo li. Leve KeyError si l pa egziste."""
    lesson = LESSONS_BY_NUMBER.get(number)
    if lesson is None:
        raise KeyError(f"Pa gen leson {number}")
    return lesson


def get_section(number: int) -> Section:
    """Jwenn yon seksyon pa nimewo li."""
    for section in ALL_SECTIONS:
        if section.number == number:
            return section
    raise KeyError(f"Pa gen seksyon {number}")


def section_lessons(section: Section) -> list[Lesson]:
    """Inite yon seksyon, nan lòd."""
    return [LESSONS_BY_NUMBER[n] for n in section.lesson_numbers
            if n in LESSONS_BY_NUMBER]


def section_of(lesson: Lesson) -> Section:
    """Ki seksyon yon inite fè pati."""
    return get_section(lesson.section_number)


def current_lesson() -> Lesson:
    """Premye inite ki poko fini epi ki pa bloke — sa 'Kontinye' louvri."""
    for lesson in ALL_LESSONS:
        if not lesson.is_locked and lesson.progress < 1.0:
            return lesson
    return ALL_LESSONS[0]
