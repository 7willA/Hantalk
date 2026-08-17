# Copyright (c) 2026 Wilkend. All rights reserved.
# Hantalk - proprietary software. See LICENSE at the repository root.
# Unauthorized copying, modification, or redistribution is prohibited.

"""GrammarPattern model — yon modèl fraz ak tablo estrikti li.

Flutter counterpart: lib/models/grammar_pattern.dart
"""

from dataclasses import dataclass, field


@dataclass
class GrammarPattern:
    title: str
    formula: str
    explanation: str
    headers: list[str] = field(default_factory=list)
    rows: list[list[str]] = field(default_factory=list)

