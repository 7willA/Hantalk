# Copyright (c) 2026 Wilkend. All rights reserved.
# Hantalk - proprietary software. See LICENSE at the repository root.
# Unauthorized copying, modification, or redistribution is prohibited.

"""VocabularyEntry model — yon sèl mo vokabilè.

Flutter counterpart: lib/models/vocabulary_entry.dart
"""

from dataclasses import dataclass


@dataclass
class VocabularyEntry:
    traditional: str
    pinyin: str
    pos: str
    english: str

    example_zh: str = ""
    example_pinyin: str = ""
    example_en: str = ""
    audio: str = ""

    