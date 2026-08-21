# Copyright (c) 2026 Wilkend. All rights reserved.
# Hantalk - proprietary software. See LICENSE at the repository root.
# Unauthorized copying, modification, or redistribution is prohibited.



from dataclasses import dataclass
from enum import Enum


class ActivityKind(str, Enum):
    """Node kind. The value is what goes into a URL route."""

    DIALOGUE = "dialogue"
    VOCABULARY = "vocabulary"
    EXERCISES = "exercises"
    PHONETICS = "phonetics"
    TONES = "tones"
    AI = "ai"


class ActivityState(str, Enum):
    DONE = "done"
    ACTIVE = "active"
    LOCKED = "locked"


# Titles and subtitles live here, not in the screen, so they stay the
# same no matter where we show them (the path, the popup, the summary).
KIND_LABELS: dict[ActivityKind, tuple[str, str]] = {
    ActivityKind.DIALOGUE: ("Dialogue", "Listen to and read the conversation"),
    ActivityKind.VOCABULARY: ("Vocabulary", "Flashcards for new words"),
    ActivityKind.EXERCISES: ("Exercises", "Test what you remember — 12 questions"),
    ActivityKind.PHONETICS: ("Phonetics", "漢字 · ㄅㄆㄇ · Tongyong · Pinyin"),
    ActivityKind.TONES: ("Tones", "Practice the 4 tones plus the neutral tone"),
    ActivityKind.AI: ("Practice", "Talk with the AI teacher"),
}

# Order of nodes on the path. Phonetics comes after dialogue because you
# need to hear the sentence before you break down its sounds.
#
# EXERCISES sits after VOCABULARY on purpose: it's the first moment in the
# unit where the app ASKS you for something instead of SHOWING you
# something. Before it, you received; after it, you produce.
KIND_ORDER: tuple[ActivityKind, ...] = (
    ActivityKind.DIALOGUE,
    ActivityKind.VOCABULARY,
    ActivityKind.EXERCISES,
    ActivityKind.PHONETICS,
    ActivityKind.TONES,
    ActivityKind.AI,
)


@dataclass
class Activity:
    kind: ActivityKind
    lesson_number: int
    state: ActivityState = ActivityState.LOCKED

    item_count: int = 0
    """How many items it contains — dialogue lines, words, syllables. 0 = we don't know."""

    done_count: int = 0

    @property
    def title(self) -> str:
        return KIND_LABELS[self.kind][0]

    @property
    def subtitle(self) -> str:
        return KIND_LABELS[self.kind][1]

    @property
    def route(self) -> str:
        """The route for this node.

        Existing routes don't change — we just map onto them.
        """
        n = self.lesson_number
        return {
            ActivityKind.DIALOGUE: f"/lesson/{n}",
            ActivityKind.VOCABULARY: f"/vocab/{n}",
            ActivityKind.EXERCISES: f"/exercise/{n}",
            ActivityKind.PHONETICS: f"/phonetic/{n}/0",
            ActivityKind.TONES: "/drills",
            ActivityKind.AI: "/practice",
        }[self.kind]

    def count_label(self) -> str:
        """'3 of 8' — what appears in the popup."""
        if not self.item_count:
            return ""
        return f"{self.done_count} of {self.item_count}"


def _item_count(lesson, kind: ActivityKind) -> int:
    """How many items a node has, based on the lesson's content."""
    if kind is ActivityKind.DIALOGUE:
        return len(lesson.dialogue.lines) if lesson.dialogue else 0
    if kind is ActivityKind.VOCABULARY:
        return len(lesson.vocabulary)
    if kind is ActivityKind.EXERCISES:
        # A fixed-size session. `models/session.py` has the value — we
        # don't import it here so `models/activity.py` stays free of
        # dependencies.
        return 12
    if kind is ActivityKind.PHONETICS:
        return len(lesson.dialogue.lines) if lesson.dialogue else 0
    if kind is ActivityKind.TONES:
        return 5          # 4 tones + the neutral tone
    return 0              # AI doesn't have a fixed count


def build_activities(lesson) -> list[Activity]:
    """Build the 5 nodes of a unit, with their states.

    HOW STATES ARE DECIDED

      If the lesson is locked → all nodes are locked.
      Otherwise we take `lesson.progress` (0.0 → 1.0) and translate it
      into nodes: with 5 nodes, 0.5 means 2 done and the 3rd active.

      This is an approximation. Once `progress_service.py` tracks each
      activity separately, only this function will need to change —
      the screen won't know anything happened.
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
