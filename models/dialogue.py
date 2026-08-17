# Copyright (c) 2026 Wilkend. All rights reserved.
# Hantalk - proprietary software. See LICENSE at the repository root.
# Unauthorized copying, modification, or redistribution is prohibited.

"""Dialogue + DialogueLine models.

Flutter counterpart: lib/models/dialogue.dart
"""

from dataclasses import dataclass, field


@dataclass
class DialogueLine:
    speaker: str
    avatar: str
    traditional: str
    pinyin: str
    english: str
    is_left: bool = True
    audio: str = ""


@dataclass
class Dialogue:
    scene: str
    scene_en: str
    lines: list[DialogueLine] = field(default_factory=list)

