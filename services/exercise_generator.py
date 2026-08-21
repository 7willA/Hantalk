# Copyright (c) 2026 Wilkend. All rights reserved.
# Hantalk - proprietary software. See LICENSE at the repository root.
# Unauthorized copying, modification, or redistribution is prohibited.

"""Exercise generator — builds exercises from content that already exists.

Flutter counterpart: none — this is a new layer.

WHY WE GENERATE INSTEAD OF WRITING BY HAND

  12 lessons × ~25 words = several hundred exercises. Writing them by
  hand is typing, not development — and every time you fix a word you'd
  have to go find every exercise that uses it.

  Here, when you write real content for lesson 5, its exercises change
  ON THEIR OWN. Same spirit as `fill_demo_content()`.

  What this generator CANNOT do: teach a grammar pattern with nuance.
  For that, `Lesson` may carry a list of hand-written exercises someday
  — and `generate()` will just fill in the gaps. The screen won't know
  the difference.

TONES WITHOUT A MICROPHONE

  `tone_variants()` below is the most interesting piece in this file.
  It takes `míngzi` and gives back `mīngzi`, `mǐngzi`, `mìngzi`,
  `mingzi` — same syllable, wrong tone. This forces the ear and the eye
  onto TONE, which is problem number 1 in Mandarin, without needing a
  microphone or sound analysis.
"""

import random

from models.exercise import Exercise, ExerciseKind

# ── Tones ────────────────────────────────────────────────────

# Each row: vowel without tone, tone 1, 2, 3, 4.
_TONE_ROWS: dict[str, str] = {
    "a": "aāáǎà",
    "e": "eēéěè",
    "i": "iīíǐì",
    "o": "oōóǒò",
    "u": "uūúǔù",
    "ü": "üǖǘǚǜ",
}

# marked character → (base vowel, tone number)
_MARKED: dict[str, tuple[str, int]] = {
    ch: (base, tone)
    for base, row in _TONE_ROWS.items()
    for tone, ch in enumerate(row)
}


def tone_variants(pinyin: str) -> list[str]:
    """All versions of `pinyin` with a single tone changed.

    >>> tone_variants("míngzi")
    ['mingzi', 'mīngzi', 'mǐngzi', 'mìngzi']

    If the word has no tone mark at all (a neutral-tone word), it
    returns an empty list — and the caller must find other distractors
    elsewhere.
    """
    out: list[str] = []
    for i, ch in enumerate(pinyin):
        entry = _MARKED.get(ch)
        if entry is None:
            continue
        base, tone = entry
        if tone == 0:
            continue                      # vowel without a mark — not a tone
        row = _TONE_ROWS[base]
        for t in range(5):
            if t != tone:
                out.append(pinyin[:i] + row[t] + pinyin[i + 1:])
    return out


# ── Distractors ─────────────────────────────────────────────────

def _distractors(
    correct: str,
    near: list[str],
    far: list[str],
    rng: random.Random,
    n: int = 3,
    exclude: str = "",
) -> list[str]:
    """Pick `n` wrong answers.

    `near` comes first (same lesson — harder, more instructive), then
    we fill in with `far` (rest of the course) if that's not enough.

    `exclude` is the question itself. We must remove it on purpose:
    right now lessons 3–12 borrow content from lessons 1–2
    (`fill_demo_content()`), so the same phrase shows up in multiple
    lessons. Without this guard, a REPLY exercise could ask «你好！»
    and offer «你好！» as a wrong choice — which isn't wrong at all, and
    makes the question unfair.
    """
    picked: list[str] = []
    for pool in (near, far):
        candidates = [
            x for x in dict.fromkeys(pool)     # remove duplicates, keep order
            if x and x != correct and x != exclude and x not in picked
        ]
        rng.shuffle(candidates)
        picked.extend(candidates[: n - len(picked)])
        if len(picked) >= n:
            break
    return picked


def _make(
    kind: ExerciseKind,
    prompt: str,
    answer: str,
    distractors: list[str],
    rng: random.Random,
    hint: str = "",
    source: str = "",
) -> Exercise | None:
    """Build an exercise, or None if there aren't enough wrong answers.

    A question with only one choice isn't a question. We require at
    least two wrong answers — otherwise we silently skip the exercise.
    """
    if len(distractors) < 2:
        return None
    options = [answer, *distractors]
    rng.shuffle(options)
    return Exercise(
        kind=kind,
        prompt=prompt,
        answer=answer,
        options=options,
        hint=hint,
        source=source,
    )


# ── Word bank (BUILD) ────────────────────────────────────────────

BUILD_MIN_WORDS = 3
BUILD_MAX_WORDS = 8
"""A 2-word sentence isn't an exercise; a 10-word sentence is a chore."""

BUILD_EXTRA = 3
"""How many extra words we add to the bank so it's not too easy."""

_TRAILING = " .!?,;:"


def _words(sentence: str) -> list[str]:
    """Split a sentence into words, without punctuation at the end.

    We strip the final punctuation because if we left it, the last
    tile would say «Chinese?» and the person would know it's the last
    one — the exercise would answer itself.
    """
    return [w for w in sentence.strip(_TRAILING).split() if w]


def _build(zh: str, en: str, pinyin: str, far_text: list[str],
          rng: random.Random, source: str) -> Exercise | None:
    """A word-bank exercise built from a Chinese sentence and its translation.

    It works for two sources: dialogue lines AND vocabulary example
    sentences. Example sentences are the bigger source — every word in
    lesson 1 has one, so there are 25 short sentences already built to
    show a single word at a time.

    Distractor words come from the text of OTHER lessons, and we
    compare them lowercase: a bank containing both «You» and «you» is
    a trap, not a lesson.
    """
    words = _words(en)
    if not (BUILD_MIN_WORDS <= len(words) <= BUILD_MAX_WORDS):
        return None

    inside = {w.lower() for w in words}
    pool = [
        w
        for other in far_text
        for w in _words(other)
        if w.lower() not in inside
    ]
    extras = _distractors("", list(dict.fromkeys(pool)), [], rng,
                          n=BUILD_EXTRA)
    if len(extras) < 2:
        return None

    options = [*words, *extras]
    rng.shuffle(options)
    return Exercise(
        kind=ExerciseKind.BUILD,
        prompt=zh,
        answer=" ".join(words),
        options=options,
        hint=pinyin,
        source=source,
    )


# ── The generator ────────────────────────────────────────────────

def generate_exercises(lesson, corpus=None) -> list[Exercise]:
    """All the exercises a lesson can produce, without sound.

    `corpus` is the other lessons — that's where distractors come from
    when the lesson alone doesn't have enough. If it's None, we fetch
    `ALL_LESSONS`.

    The result is REPRODUCIBLE: the same lesson gives the same
    exercises every time (rng seeded with the lesson number). This
    makes tests meaningful. It's `Session` that adds randomness, when
    it picks which exercises go into a session.
    """
    if corpus is None:
        from data.lessons.all_lessons import ALL_LESSONS
        corpus = ALL_LESSONS

    rng = random.Random(lesson.number)
    out: list[Exercise] = []

    others = [l for l in corpus if l.number != lesson.number]

    # Text pools — «near» = same lesson, «far» = rest of the course.
    near_zh = [v.traditional for v in lesson.vocabulary]
    near_en = [v.english for v in lesson.vocabulary]
    near_py = [v.pinyin for v in lesson.vocabulary]

    far_zh, far_en, far_py = [], [], []
    far_text: list[str] = []          # full sentences — the BUILD word bank
    for other in others:
        far_zh.extend(v.traditional for v in other.vocabulary)
        far_en.extend(v.english for v in other.vocabulary)
        far_py.extend(v.pinyin for v in other.vocabulary)
        far_text.extend(v.example_en for v in other.vocabulary if v.example_en)
        if other.dialogue:
            far_text.extend(l.english for l in other.dialogue.lines)

    # ── From the vocabulary ──────────────────────────────────────
    for entry in lesson.vocabulary:
        if not entry.traditional or not entry.english:
            continue
        source = f"L{lesson.number}:{entry.traditional}"

        out.append(_make(
            ExerciseKind.RECOGNIZE, entry.traditional, entry.english,
            _distractors(entry.english, near_en, far_en, rng),
            rng, hint=entry.pinyin, source=source,
        ))

        out.append(_make(
            ExerciseKind.RECALL, entry.english, entry.traditional,
            _distractors(entry.traditional, near_zh, far_zh, rng),
            rng, source=source,
        ))

        # BUILD — the example sentence gives a word bank directly.
        if entry.example_zh and entry.example_en:
            out.append(_build(entry.example_zh, entry.example_en,
                             entry.example_pinyin, far_text, rng, source))

        if entry.pinyin:
            # Distractors are the same syllable with a different tone.
            # If the word has no tone mark, we fall back on other
            # words' pinyin.
            variants = tone_variants(entry.pinyin)
            out.append(_make(
                ExerciseKind.PINYIN, entry.traditional, entry.pinyin,
                _distractors(entry.pinyin, variants, near_py + far_py, rng),
                rng, source=source,
            ))

    # ── From the dialogue ───────────────────────────────────────
    lines = lesson.dialogue.lines if lesson.dialogue else []

    # Lines from other lessons — distractors for TRANSLATE and REPLY. We
    # don't take lines from the same dialogue: they all fit together,
    # so they'd be ambiguous.
    far_lines_zh, far_lines_en = [], []
    for other in others:
        if other.dialogue:
            far_lines_zh.extend(l.traditional for l in other.dialogue.lines)
            far_lines_en.extend(l.english for l in other.dialogue.lines)

    for i, line in enumerate(lines):
        source = f"L{lesson.number}:d{i + 1}"

        if line.traditional and line.english:
            out.append(_make(
                ExerciseKind.TRANSLATE, line.traditional, line.english,
                _distractors(line.english, [], far_lines_en, rng,
                             exclude=line.english),
                rng, hint=line.pinyin, source=source,
            ))

        # BUILD — same line, but the person builds the translation.
        if line.traditional and line.english:
            out.append(_build(line.traditional, line.english, line.pinyin,
                             far_text, rng, source))

        # REPLY — the correct answer is the NEXT line.
        if i + 1 < len(lines):
            nxt = lines[i + 1]
            if line.traditional and nxt.traditional:
                out.append(_make(
                    ExerciseKind.REPLY, line.traditional, nxt.traditional,
                    _distractors(nxt.traditional, [], far_lines_zh, rng,
                                 exclude=line.traditional),
                    rng, hint=line.english, source=source,
                ))

    return [ex for ex in out if ex is not None]
