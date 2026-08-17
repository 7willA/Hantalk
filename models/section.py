# Copyright (c) 2026 Wilkend. All rights reserved.
# Hantalk - proprietary software. See LICENSE at the repository root.
# Unauthorized copying, modification, or redistribution is prohibited.

"""Section model — yon gwoup inite ki fè yon nivo nan kou a.

Flutter counterpart: pa gen — se yon nivo nouvo.

YERAJI A

    Section    "Debitan 1"                 ← fichye sa a
      └── Unit = yon Lesson (你叫什麼名字)   ← models/lesson.py
            └── Activity = yon nœud         ← models/activity.py

BATI POU L GRANDI

  Ou di w ap ajoute anpil seksyon ak anpil nivo pi devan. Donk:

  1. `Section` PA kenbe objè `Lesson` yo — li kenbe NIMEWO yo
     (`lesson_numbers`). Konsa ajoute yon seksyon se ekri yon liy nan
     `data/lessons/all_lessons.py`, pa touche modèl la.

  2. Koulè a se yon ENDÈKS (`color_index`), pa yon hex. Palèt la viv nan
     `app/theme.py`. Lè w gen 20 seksyon, endèks la anwole sou palèt la
     otomatikman — ou pa janm bloke paske w manke koulè.

  3. `level` se tèks lib ("Debitan", "Entèmedyè", "HSK 3"...). Nou pa
     fè yon Enum paske yon Enum ta vle di chak nouvo nivo mande yon
     chanjman kòd.
"""

from dataclasses import dataclass, field


@dataclass
class Section:
    number: int
    """Lòd afichaj la — 1, 2, 3... Se sa ki parèt nan 'SEKSYON 2'."""

    traditional: str
    """Tit la an chinwa, pou bandwòl la (egz. 基礎一)."""

    english: str
    """Tit la an anglè (egz. 'Foundations 1')."""

    level: str = ""
    """Etikèt nivo lib: 'Debitan', 'Entèmedyè', 'HSK 3'..."""

    description: str = ""
    """Yon fraz ki di sa moun nan pral kapab fè apre seksyon an."""

    lesson_numbers: list[int] = field(default_factory=list)
    """Nimewo leson yo, nan lòd. Se yo ki fè inite seksyon an."""

    color_index: int = 0
    """Endèks nan palèt seksyon an (`theme.section_color()`)."""

    is_locked: bool = False

    # ── enfòmasyon nou kalkile ────────────────────────────────

    @property
    def unit_count(self) -> int:
        return len(self.lesson_numbers)

    def progress(self, lessons_by_number: dict[int, object]) -> float:
        """Mwayèn pwogrè inite yo, ant 0.0 ak 1.0.

        Nou pase diksyonè a kòm agiman olye nou enpòte done yo isit la.
        Sa kenbe `models/` pwòp: yon modèl pa dwe konnen ki kote done
        yo soti — sinon w ap jwenn enpòtasyon sikilè lè app la grandi.
        """
        if not self.lesson_numbers:
            return 0.0
        total = 0.0
        for n in self.lesson_numbers:
            lesson = lessons_by_number.get(n)
            total += getattr(lesson, "progress", 0.0) if lesson else 0.0
        return total / len(self.lesson_numbers)

    def completed_units(self, lessons_by_number: dict[int, object]) -> int:
        """Konbyen inite ki fini nèt — pou konte a '3 / 6'."""
        done = 0
        for n in self.lesson_numbers:
            lesson = lessons_by_number.get(n)
            if lesson is not None and getattr(lesson, "progress", 0.0) >= 1.0:
                done += 1
        return done

    def label(self) -> str:
        """'SEKSYON 2' — ti majiskil ki chita anwo bandwòl la."""
        return f"SEKSYON {self.number}"
