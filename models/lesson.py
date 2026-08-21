# Copyright (c) 2026 Wilkend. All rights reserved.
# Hantalk - proprietary software. See LICENSE at the repository root.
# Unauthorized copying, modification, or redistribution is prohibited.

"""Lesson model — a complete lesson.

Flutter counterpart: lib/models/lesson.dart
"""

from dataclasses import dataclass, field

from models.dialogue import Dialogue
from models.grammar_pattern import GrammarPattern
from models.vocabulary_entry import VocabularyEntry


@dataclass
class Lesson:
    """A lesson — which also acts as a UNIT on the path.

    In the new structure: Section → Unit → Activity. A `Lesson` is
    a unit; its 5 tabs become 5 nodes (see `models/activity.py`).
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
    """Which section this unit belongs to. See `models/section.py`."""

    @property
    def has_content(self) -> bool:
        """Does the lesson have real content, or is it just a title?"""
        return self.dialogue is not None or bool(self.vocabulary)