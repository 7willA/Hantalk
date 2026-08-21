# Copyright (c) 2026 Wilkend. All rights reserved.
# Hantalk - proprietary software. See LICENSE at the repository root.
# Unauthorized copying, modification, or redistribution is prohibited.

"""Session — the state of an exercise session.

Flutter counterpart: none — this is a new layer.

THE MISSING PIECE BETWEEN `Exercise` AND THE SCREEN

  Without it, the screen would have to hold the queue, count correct
  answers, and decide when the session is done — three things that
  have nothing to do with drawing. Here, the screen just asks: what's
  the current question, and calls `answer()`. Everything else happens
  inside.

NO HEARTS, NO PUNISHMENT

  When you make a mistake, the exercise goes BACK into the queue, ~3
  questions later. That's what replaces Duolingo's hearts.

  Two reasons:
    1. It's a REAL consequence — your session gets longer.
    2. It's spaced repetition within a session, which is what actually
       makes people learn. A heart that disappears doesn't teach
       anything.

  The consequence: `queue` GROWS during the session. That's why
  progress counts `cleared / planned` and not `index / len(queue)` —
  otherwise the bar would go backward every time you make a mistake,
  which would be discouraging.
"""

import random
import time
from dataclasses import dataclass, field

from models.exercise import Exercise, ExerciseKind

DEFAULT_SIZE = 12
"""How many exercises are in a session.

Duolingo stays between 12 and 20. We use 12 — a 2-3 minute session. A
lesson can produce 80+ possible exercises, so we're not short on
content; it's the pace we're protecting.
"""

REQUEUE_GAP = 3
"""How many questions after a miss before the exercise comes back."""

PLAYABLE_KINDS = {
    ExerciseKind.RECOGNIZE,
    ExerciseKind.RECALL,
    ExerciseKind.PINYIN,
    ExerciseKind.TRANSLATE,
    ExerciseKind.REPLY,
}
"""Kinds that `exercise_view` knows how to draw TODAY.

`ExerciseKind.BUILD` generates fine (see `exercise_generator.py`) but
the screen has 4 fixed choice boxes — it has no slots or word bank. If
we let BUILD through, the person would see 7 words and every tap would
give "wrong answer", because `answer` is the WHOLE sentence.

Once the word-bank panel exists, add `ExerciseKind.BUILD` here. It's a
one-line change — the generator is already ready.
"""

XP_PER_CORRECT = 10
COMBO_BONUS_AT = 3
COMBO_BONUS = 5
"""The reward system, taken from the `fafu` prototype.

WHY XP AND COMBO BUT NOT HEARTS

  `fafu` came with three things together: XP, combo, and 5 hearts. We
  kept the first two and dropped the hearts.

  XP and combo GIVE. They say "what you just did counts", and the
  combo rewards something good for learning: staying focused across
  several questions in a row.

  Hearts TAKE AWAY. They close the session on the person who makes the
  most mistakes — exactly the person who needs to stay. The requeue is
  already the consequence: you make a mistake, the question comes
  back, your session gets longer. That teaches. A "you lost all your
  hearts" screen doesn't teach anything.
"""

MAX_SECONDS_PER_ANSWER = 60
"""Time cap for ONE question.

We count active time, not wall-clock time. If your phone is in your
pocket for 20 minutes between two questions, that question counts as
60 seconds, not 20 minutes. Without this cap, the daily goal (see
`settings_service.daily_goal_min`) could fill itself up while you
sleep.
"""


def _mixed_sample(
    pool: list[Exercise],
    size: int,
    rng: random.Random,
) -> list[Exercise]:
    """Pick `size` exercises, but with a MIX of kinds.

    If we just picked randomly, a session could give 12 RECOGNIZE in a
    row — the same thing 12 times. Here we group by kind, and take one
    of each kind per round, until we have enough.
    """
    by_kind: dict[ExerciseKind, list[Exercise]] = {}
    for ex in pool:
        by_kind.setdefault(ex.kind, []).append(ex)

    for group in by_kind.values():
        rng.shuffle(group)

    kinds = list(by_kind)
    rng.shuffle(kinds)

    picked: list[Exercise] = []
    while len(picked) < size and any(by_kind[k] for k in kinds):
        for kind in kinds:
            if by_kind[kind]:
                picked.append(by_kind[kind].pop())
            if len(picked) >= size:
                break

    rng.shuffle(picked)
    return picked


@dataclass
class Session:
    queue: list[Exercise]
    planned: int
    """How many DISTINCT exercises the session has. Never changes."""

    rng: random.Random = field(default_factory=random.Random)

    index: int = 0
    cleared: int = 0
    """How many exercises were answered correctly. Reaches `planned` at the end."""

    mistakes: int = 0
    """Total number of wrong answers (one exercise can count more than once)."""

    xp: int = 0
    combo: int = 0
    """How many correct answers in a row right now. A mistake resets it to 0."""

    best_combo: int = 0
    """The session's longest combo — what the summary screen celebrates."""

    last_gain: int = 0
    """XP the last answer gave. What the banner shows: «+15 XP»."""

    seconds: float = 0.0
    """Active time, in seconds. See `MAX_SECONDS_PER_ANSWER`."""

    mark: float = field(default_factory=time.monotonic, repr=False)
    """When the last question appeared. `time.monotonic` never goes
    backward, even if the person changes their phone's clock."""

    # ── Construction ─────────────────────────────────────────

    @classmethod
    def for_lesson(cls, lesson, size: int = DEFAULT_SIZE,
                   kinds: set | None = None) -> "Session":
        """A session for a lesson. The order changes every time."""
        from services.exercise_generator import generate_exercises

        allowed = PLAYABLE_KINDS if kinds is None else kinds
        rng = random.Random()
        pool = [ex for ex in generate_exercises(lesson) if ex.kind in allowed]
        queue = _mixed_sample(pool, size, rng)
        return cls(queue=queue, planned=len(queue), rng=rng)

    # ── Reading ────────────────────────────────────────────────

    @property
    def current(self) -> Exercise | None:
        if self.index < len(self.queue):
            return self.queue[self.index]
        return None

    @property
    def is_done(self) -> bool:
        return self.index >= len(self.queue)

    @property
    def is_empty(self) -> bool:
        """The lesson doesn't have enough content to make a session."""
        return self.planned == 0

    @property
    def progress(self) -> float:
        """Between 0.0 and 1.0 — what the bar at the top shows."""
        if not self.planned:
            return 0.0
        return min(1.0, self.cleared / self.planned)

    @property
    def clock(self) -> str:
        """'2:05' — for the TIME card on the summary screen."""
        s = int(self.seconds)
        return f"{s // 60}:{s % 60:02d}"

    @property
    def minutes(self) -> int:
        """Active time in minutes, rounded up as soon as there's at least one second.

        This is what goes toward the daily goal. A 40-second session
        counts as 1 minute — we're not in the business of stealing
        people's time.
        """
        if self.seconds <= 0:
            return 0
        return max(1, round(self.seconds / 60))

    @property
    def position(self) -> str:
        """'4 / 12' — where we are in the session."""
        return f"{min(self.cleared + 1, self.planned)} / {self.planned}"

    @property
    def accuracy(self) -> int:
        """Percentage of correct answers, 0-100.

        Each exercise counts one correct answer (`planned`), and each
        mistake adds one extra attempt.
        """
        attempts = self.planned + self.mistakes
        if not attempts:
            return 0
        return round(100 * self.planned / attempts)

    # ── Actions ───────────────────────────────────────────────

    def answer(self, choice: str) -> bool:
        """Record an answer and move forward. Returns whether it was correct.

        On a mistake, the exercise goes back into the queue with the
        choices shuffled again — so the person can't remember the
        POSITION of the correct answer.
        """
        exercise = self.current
        if exercise is None:
            return False

        now = time.monotonic()
        self.seconds += min(now - self.mark, MAX_SECONDS_PER_ANSWER)
        self.mark = now

        correct = exercise.is_correct(choice)
        if correct:
            self.cleared += 1
            self.combo += 1
            self.best_combo = max(self.best_combo, self.combo)
            self.last_gain = XP_PER_CORRECT
            if self.combo >= COMBO_BONUS_AT:
                self.last_gain += COMBO_BONUS
            self.xp += self.last_gain
        else:
            self.mistakes += 1
            self.combo = 0
            self.last_gain = 0
            where = min(self.index + REQUEUE_GAP, len(self.queue))
            self.queue.insert(where, exercise.reshuffled(self.rng))

        self.index += 1
        return correct
