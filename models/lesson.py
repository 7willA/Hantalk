# Copyright (c) 2026 Wilkend. All rights reserved.
# Hantalk - proprietary software. See LICENSE at the repository root.
# Unauthorized copying, modification, or redistribution is prohibited.

"""Lesson model — yon leson konplè.

Flutter counterpart: lib/models/lesson.dart
"""

from dataclasses import dataclass, field

from models.dialogue import Dialogue
from models.grammar_pattern import GrammarPattern
from models.vocabulary_entry import VocabularyEntry


@dataclass
class Lesson:
    """Yon leson — ki sèvi tou kòm yon INITE sou chemen an.

    Nan nouvo estrikti a: Section → Unit → Activity. Yon `Lesson` se
    yon inite; 5 onglè li yo vin 5 nœud (gade `models/activity.py`).
    """

    number: int
    traditional: str
    english: str
    dialogue: Dialogue | None = None
    vocabulary: list[VocabularyEntry] = field(default_factory=list)
    patterns: list[GrammarPattern] = field(default_factory=list)
    culture_note: str = ""
    progress: float = 0.0
    is_locked: bool = False

    section_number: int = 1
    """Ki seksyon inite sa a fè pati. Gade `models/section.py`."""

    @property
    def has_content(self) -> bool:
        """Èske leson an gen vre kontni, oswa se yon tit sèlman?"""
        return self.dialogue is not None or bool(self.vocabulary)