# Copyright (c) 2026 Wilkend. All rights reserved.
# Hantalk - proprietary software. See LICENSE at the repository root.
# Unauthorized copying, modification, or redistribution is prohibited.

"""Done drill pou ekran 06.

Chak drill gen yon koub ton — yon lis pwen (x, y) nan yon gri 120 × 34
kote y=0 se anlè epi y=34 anba. `phonetic_view` pa itilize sa; se
`drills_view` ki desine yo sou yon ft.Canvas.
"""

from dataclasses import dataclass, field


@dataclass
class Drill:
    key: str
    glyph: str
    title: str
    subtitle: str
    hint: str
    points: list[tuple[float, float]] = field(default_factory=list)
    dot: bool = False
    pills: list[str] = field(default_factory=list)


DRILLS = [
    Drill(
        key="tone1",
        glyph="媽",
        title="Tone 1",
        subtitle="High level · 20 syllables",
        hint="Hold a flat, high pitch from start to finish.",
        points=[(6, 8), (114, 8)],
    ),
    Drill(
        key="tone2",
        glyph="麻",
        title="Tone 2",
        subtitle="Rising · 20 syllables",
        hint="Start mid and climb — like asking 'huh?' in English.",
        points=[(6, 26), (114, 6)],
    ),
    Drill(
        key="tone3",
        glyph="馬",
        title="Tone 3",
        subtitle="Dipping · 20 syllables",
        hint="Dip low and hold there. In Taiwan the rise is often dropped.",
        points=[(6, 10), (44, 26), (76, 26), (114, 4)],
    ),
    Drill(
        key="tone4",
        glyph="罵",
        title="Tone 4",
        subtitle="Falling · 20 syllables",
        hint="Drop sharply from high to low, like a firm 'No!'",
        points=[(6, 5), (114, 28)],
    ),
    Drill(
        key="neutral",
        glyph="嗎",
        title="Neutral tone",
        subtitle="Light · 16 syllables",
        hint="Short and unstressed. Its pitch depends on the tone before it.",
        dot=True,
    ),
    Drill(
        key="pairs",
        glyph="zh / z",
        title="Initials & finals",
        subtitle="Tricky pairs · 32 items",
        hint="Taiwanese Mandarin often merges zh/z and ch/c — train both.",
        pills=["zh / z", "ch / c", "-an / -ang"],
    ),
]


def get_drill(key: str) -> Drill:
    for d in DRILLS:
        if d.key == key:
            return d
    raise KeyError(f"Pa gen drill {key}")
