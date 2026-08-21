# Copyright (c) 2026 Wilkend. All rights reserved.
# Hantalk - proprietary software. See LICENSE at the repository root.
# Unauthorized copying, modification, or redistribution is prohibited.



from dataclasses import dataclass, field
from enum import Enum


class ExerciseKind(str, Enum):
    """Question kind. The value is text so we can save it later."""

    RECOGNIZE = "recognize"
    """名字 → «name». See the character, find the meaning."""

    RECALL = "recall"
    """«name» → 名字. Meaning given, find the character. Harder."""

    PINYIN = "pinyin"
    """名字 → míngzi. Distractors are the SAME syllable with the WRONG TONE.

    This is a tone exercise that works WITHOUT a microphone. Duolingo
    doesn't do this.
    """

    TRANSLATE = "translate"
    """你叫什麼名字？ → «What's your name?». A whole sentence."""

    REPLY = "reply"
    """安安 says something → what 凱文 replies.

    Dialogue lines are already in order, so line N+1 IS the correct
    answer for line N. We don't write anything — the conversation
    produces the exercise on its own.
    """

    BUILD = "build"
    """你會說中文嗎？ → [Can] [you] [speak] [Chinese]

    Build the sentence with word tiles — the most recognizable
    interaction of this kind.

    IT DOESN'T NEED A NEW SHAPE. `answer` is the whole sentence;
    `options` are the words, shuffled, plus a few extra words that
    don't belong. The screen joins the words the person taps with a
    space and sends the result to `Session.answer()` just like any
    other kind. That's why `reshuffled()` works here too: it reshuffles
    the word bank.
    """


@dataclass(frozen=True)
class KindMeta:
    """What the screen needs to know to draw a kind."""

    instruction: str
    """Short phrase that sits above the question."""

    prompt_zh: bool
    """Is the question in Chinese? (picks the font)"""

    options_zh: bool
    """Are the choices in Chinese?"""

    prompt_size: int
    """Size of the question text. Chinese needs to be bigger than Latin."""


KIND_META: dict[ExerciseKind, KindMeta] = {
    ExerciseKind.RECOGNIZE: KindMeta("What does this mean?", True, False, 44),
    ExerciseKind.RECALL: KindMeta("Choose the correct character", False, True, 26),
    ExerciseKind.PINYIN: KindMeta("Which pinyin is correct?", True, False, 44),
    ExerciseKind.TRANSLATE: KindMeta("Translate this sentence", True, False, 28),
    ExerciseKind.REPLY: KindMeta("What would you reply?", True, True, 26),
    ExerciseKind.BUILD: KindMeta("Build the sentence with the words", True, False, 26),
}


@dataclass
class Exercise:
    kind: ExerciseKind

    prompt: str
    """What appears at the top — a character, an English word, or a sentence."""

    answer: str
    """The correct answer. It MUST be in `options`."""

    options: list[str] = field(default_factory=list)
    """The choices, already shuffled. Should never be empty."""

    hint: str = ""
    """Small line under the question — pinyin, or what someone just said."""

    audio: str = ""
    """Path to the audio file. Empty for now — see AUDIO_PLAN.md."""

    source: str = ""
    """Which word/line the exercise came from — for tracking progress later."""

    @property
    def meta(self) -> KindMeta:
        return KIND_META[self.kind]

    def is_correct(self, choice: str) -> bool:
        return choice == self.answer

    def reshuffled(self, rng) -> "Exercise":
        """A copy with the choices in a different order.

        Used when an exercise goes back into the queue after a
        mistake: if the choices stay in the same spot, the person
        remembers the POSITION instead of the answer. That's not what
        we want to teach.
        """
        options = list(self.options)
        rng.shuffle(options)
        return Exercise(
            kind=self.kind,
            prompt=self.prompt,
            answer=self.answer,
            options=options,
            hint=self.hint,
            audio=self.audio,
            source=self.source,
        )
