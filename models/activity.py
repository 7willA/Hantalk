# Copyright (c) 2026 Wilkend. All rights reserved.
# Hantalk - proprietary software. See LICENSE at the repository root.
# Unauthorized copying, modification, or redistribution is prohibited.

"""Activity model — yon nœud sou chemen an anndan yon inite.

Flutter counterpart: pa gen — se yon nivo nouvo.

LIDE A

  Yon leson Hantalk deja gen 5 onglè: Dialogue · Vocab · Syntax ·
  Activities · Notes. Nan Duolingo, yon inite gen ~5 nœud sou yon
  chemen. Se menm bagay la — nou jis chanje fòm afichaj la.

  Donk yon `Activity` PA yon nouvo kontni. Se yon fenèt sou kontni ki
  deja nan `Lesson`. `build_activities()` gade sa leson an genyen epi
  li fabrike lis nœud yo.

DE NAN 5 YO SE PA HANTALK

  `FONETIK` (4 sistèm: 漢字 / ㄅㄆㄇ / Tongyong / Pinyin) ak `TON`
  (陰平 / 陽平 / 上聲 / 去聲) pa egziste nan Duolingo ni HelloChinese.
  Yo pa ka egziste — lòt lang pa bezwen yo. Se la chemen Hantalk la
  sispann sanble ak lòt moun.
"""

from dataclasses import dataclass
from enum import Enum


class ActivityKind(str, Enum):
    """Kalite nœud. Valè a se sa ki ale nan yon wout URL."""

    DYALOG = "dyalog"
    VOKABILE = "vokabile"
    FONETIK = "fonetik"
    TON = "ton"
    AI = "ai"


class ActivityState(str, Enum):
    DONE = "done"
    ACTIVE = "active"
    LOCKED = "locked"


# Tit ak sou-tit yo viv isit la, pa nan ekran an, konsa yo rete menm
# kèlkeswa kote nou montre yo (chemen an, popup la, rezime a).
KIND_LABELS: dict[ActivityKind, tuple[str, str]] = {
    ActivityKind.DYALOG: ("Dyalòg", "Koute epi li konvèsasyon an"),
    ActivityKind.VOKABILE: ("Vokabilè", "Kat memwa pou mo nouvo yo"),
    ActivityKind.FONETIK: ("Fonetik", "漢字 · ㄅㄆㄇ · Tongyong · Pinyin"),
    ActivityKind.TON: ("Ton", "Antrene 4 ton yo ak ton netral la"),
    ActivityKind.AI: ("Pratike", "Pale ak pwofesè AI a"),
}

# Lòd nœud yo sou chemen an. Fonetik vin apre dyalòg paske ou bezwen
# tande fraz la anvan ou dekonpoze son li.
KIND_ORDER: tuple[ActivityKind, ...] = (
    ActivityKind.DYALOG,
    ActivityKind.VOKABILE,
    ActivityKind.FONETIK,
    ActivityKind.TON,
    ActivityKind.AI,
)


@dataclass
class Activity:
    kind: ActivityKind
    lesson_number: int
    state: ActivityState = ActivityState.LOCKED

    item_count: int = 0
    """Konbyen bagay ladan l — liy dyalòg, mo, silab. 0 = nou pa konnen."""

    done_count: int = 0

    @property
    def title(self) -> str:
        return KIND_LABELS[self.kind][0]

    @property
    def subtitle(self) -> str:
        return KIND_LABELS[self.kind][1]

    @property
    def route(self) -> str:
        """Wout la pou nœud sa a.

        Wout ki deja egziste yo pa chanje — nou jis mape sou yo.
        """
        n = self.lesson_number
        return {
            ActivityKind.DYALOG: f"/lesson/{n}",
            ActivityKind.VOKABILE: f"/vocab/{n}",
            ActivityKind.FONETIK: f"/phonetic/{n}/0",
            ActivityKind.TON: "/drills",
            ActivityKind.AI: "/practice",
        }[self.kind]

    def count_label(self) -> str:
        """'3 sou 8' — sa ki parèt nan popup la."""
        if not self.item_count:
            return ""
        return f"{self.done_count} sou {self.item_count}"


def _item_count(lesson, kind: ActivityKind) -> int:
    """Konbyen bagay yon nœud genyen, dapre kontni leson an."""
    if kind is ActivityKind.DYALOG:
        return len(lesson.dialogue.lines) if lesson.dialogue else 0
    if kind is ActivityKind.VOKABILE:
        return len(lesson.vocabulary)
    if kind is ActivityKind.FONETIK:
        return len(lesson.dialogue.lines) if lesson.dialogue else 0
    if kind is ActivityKind.TON:
        return 5          # 4 ton + ton netral la
    return 0              # AI a pa gen kantite fiks


def build_activities(lesson) -> list[Activity]:
    """Fabrike 5 nœud yon inite, ak eta yo.

    KIJAN ETA YO DESIDE

      Si leson an bloke  → tout nœud bloke.
      Sinon nou pran `lesson.progress` (0.0 → 1.0) epi nou tradui l an
      nœud: ak 5 nœud, 0.5 vle di 2 fini epi 3zyèm nan aktif.

      Sa a se yon aprosimasyon. Lè `progress_service.py` ap swiv chak
      aktivite separeman, se sèl fonksyon sa a k ap chanje — ekran an
      p ap konnen anyen.
    """
    total = len(KIND_ORDER)
    finished = int(round(getattr(lesson, "progress", 0.0) * total))
    finished = max(0, min(finished, total))

    activities: list[Activity] = []
    for i, kind in enumerate(KIND_ORDER):
        if lesson.is_locked:
            state = ActivityState.LOCKED
        elif i < finished:
            state = ActivityState.DONE
        elif i == finished:
            state = ActivityState.ACTIVE
        else:
            state = ActivityState.LOCKED

        count = _item_count(lesson, kind)
        activities.append(
            Activity(
                kind=kind,
                lesson_number=lesson.number,
                state=state,
                item_count=count,
                done_count=count if state is ActivityState.DONE else 0,
            )
        )
    return activities
