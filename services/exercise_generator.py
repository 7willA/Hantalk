# Copyright (c) 2026 Wilkend. All rights reserved.
# Hantalk - proprietary software. See LICENSE at the repository root.
# Unauthorized copying, modification, or redistribution is prohibited.

"""Exercise generator — fabrike egzèsis depi kontni ki deja egziste.

Flutter counterpart: pa gen — se yon nivo nouvo.

POUKISA NOU JENERE OLYE NOU EKRI ALAMEN

  12 leson × ~25 mo = plizyè santèn egzèsis. Ekri yo alamen se tape, se
  pa devlopman — epi chak fwa w korije yon mo ou ta oblije chèche tout
  egzèsis ki sèvi avè l.

  Isit la, lè w ekri vre kontni pou leson 5, egzèsis li yo chanje
  POUKONT YO. Se menm lespri ak `fill_demo_content()`.

  Sa jeneratè a PA ka fè: anseye yon pattern gramatikal ak nuans. Pou
  sa, `Lesson` gen dwa pote yon lis egzèsis ekri alamen yon jou — epi
  `generate()` ap jis ranpli twou yo. Ekran an p ap konnen diferans lan.

TON YO SAN MIKWO

  `tone_variants()` anba a se pyès ki pi enteresan nan fichye a. Li pran
  `míngzi` epi li bay `mīngzi`, `mǐngzi`, `mìngzi`, `mingzi` — menm
  silab, move ton. Sa fòse zòrèy la ak je a sou TON, ki se pwoblèm
  nimewo 1 nan Mandarin, san nou pa bezwen ni mikwo ni analiz son.
"""

import random

from models.exercise import Exercise, ExerciseKind

# ── Ton yo ────────────────────────────────────────────────────

# Chak ranje: vwayèl san ton, ton 1, 2, 3, 4.
_TONE_ROWS: dict[str, str] = {
    "a": "aāáǎà",
    "e": "eēéěè",
    "i": "iīíǐì",
    "o": "oōóǒò",
    "u": "uūúǔù",
    "ü": "üǖǘǚǜ",
}

# karaktè ki make → (vwayèl debaz, nimewo ton)
_MARKED: dict[str, tuple[str, int]] = {
    ch: (base, tone)
    for base, row in _TONE_ROWS.items()
    for tone, ch in enumerate(row)
}


def tone_variants(pinyin: str) -> list[str]:
    """Tout vèsyon `pinyin` ak yon sèl ton chanje.

    >>> tone_variants("míngzi")
    ['mingzi', 'mīngzi', 'mǐngzi', 'mìngzi']

    Si mo a pa gen okenn mak ton (mo ton netral), li bay yon lis vid —
    epi moun ki rele l la dwe jwenn lòt move chwa yon lòt kote.
    """
    out: list[str] = []
    for i, ch in enumerate(pinyin):
        entry = _MARKED.get(ch)
        if entry is None:
            continue
        base, tone = entry
        if tone == 0:
            continue                      # vwayèl san mak — pa yon ton
        row = _TONE_ROWS[base]
        for t in range(5):
            if t != tone:
                out.append(pinyin[:i] + row[t] + pinyin[i + 1:])
    return out


# ── Move chwa ─────────────────────────────────────────────────

def _distractors(
    correct: str,
    near: list[str],
    far: list[str],
    rng: random.Random,
    n: int = 3,
    exclude: str = "",
) -> list[str]:
    """Chwazi `n` move repons.

    `near` an premye (menm leson — pi difisil, pi enstriktif), epi nou
    konplete ak `far` (rès kou a) si sa pa ase.

    `exclude` se kesyon an li menm. Nou dwe retire l espre: kounye a
    leson 3–12 prete kontni leson 1–2 (`fill_demo_content()`), donk
    menm fraz la parèt nan plizyè leson. San gad sa a, yon egzèsis
    REPONN ka mande «你好！» epi ofri «你好！» kòm move chwa — ki pa
    move ditou, epi ki fè kesyon an enjis.
    """
    picked: list[str] = []
    for pool in (near, far):
        candidates = [
            x for x in dict.fromkeys(pool)     # retire doub, kenbe lòd
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
    """Bati yon egzèsis, oswa None si pa gen ase move chwa.

    Yon kesyon ak yon sèl chwa pa yon kesyon. Nou mande omwen de move
    repons — sinon nou sote egzèsis la an silans.
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


# ── Jeneratè a ────────────────────────────────────────────────

def generate_exercises(lesson, corpus=None) -> list[Exercise]:
    """Tout egzèsis yon leson ka bay, san son.

    `corpus` se lòt leson yo — se la move chwa yo soti lè leson an
    poukont li pa gen ase. Si li None, nou al chèche `ALL_LESSONS`.

    Rezilta a REPWODIKTIB: menm leson an bay menm egzèsis yo chak fwa
    (rng grenn ak nimewo leson an). Sa fè tès yo gen sans. Se `Session`
    ki mete azar la, lè li chwazi ki egzèsis pou yon sesyon.
    """
    if corpus is None:
        from data.lessons.all_lessons import ALL_LESSONS
        corpus = ALL_LESSONS

    rng = random.Random(lesson.number)
    out: list[Exercise] = []

    others = [l for l in corpus if l.number != lesson.number]

    # Pisin tèks yo — «near» = menm leson, «far» = rès kou a.
    near_zh = [v.traditional for v in lesson.vocabulary]
    near_en = [v.english for v in lesson.vocabulary]
    near_py = [v.pinyin for v in lesson.vocabulary]

    far_zh, far_en, far_py = [], [], []
    for other in others:
        far_zh.extend(v.traditional for v in other.vocabulary)
        far_en.extend(v.english for v in other.vocabulary)
        far_py.extend(v.pinyin for v in other.vocabulary)

    # ── Depi vokabilè a ──────────────────────────────────────
    for entry in lesson.vocabulary:
        if not entry.traditional or not entry.english:
            continue
        source = f"L{lesson.number}:{entry.traditional}"

        out.append(_make(
            ExerciseKind.REKONET, entry.traditional, entry.english,
            _distractors(entry.english, near_en, far_en, rng),
            rng, hint=entry.pinyin, source=source,
        ))

        out.append(_make(
            ExerciseKind.SONJE, entry.english, entry.traditional,
            _distractors(entry.traditional, near_zh, far_zh, rng),
            rng, source=source,
        ))

        if entry.pinyin:
            # Move chwa yo se menm silab la ak lòt ton. Si mo a pa gen
            # mak ton, nou tonbe sou pinyin lòt mo yo.
            variants = tone_variants(entry.pinyin)
            out.append(_make(
                ExerciseKind.PINYIN, entry.traditional, entry.pinyin,
                _distractors(entry.pinyin, variants, near_py + far_py, rng),
                rng, source=source,
            ))

    # ── Depi dyalòg la ───────────────────────────────────────
    lines = lesson.dialogue.lines if lesson.dialogue else []

    # Liy lòt leson yo — move chwa pou TRADWI ak REPONN. Nou pa pran
    # liy menm dyalòg la: yo tout mache ansanm, donk yo ta anbigi.
    far_lines_zh, far_lines_en = [], []
    for other in others:
        if other.dialogue:
            far_lines_zh.extend(l.traditional for l in other.dialogue.lines)
            far_lines_en.extend(l.english for l in other.dialogue.lines)

    for i, line in enumerate(lines):
        source = f"L{lesson.number}:d{i + 1}"

        if line.traditional and line.english:
            out.append(_make(
                ExerciseKind.TRADWI, line.traditional, line.english,
                _distractors(line.english, [], far_lines_en, rng,
                             exclude=line.english),
                rng, hint=line.pinyin, source=source,
            ))

        # REPONN — bon repons lan se liy ki VIN APRE a.
        if i + 1 < len(lines):
            nxt = lines[i + 1]
            if line.traditional and nxt.traditional:
                out.append(_make(
                    ExerciseKind.REPONN, line.traditional, nxt.traditional,
                    _distractors(nxt.traditional, [], far_lines_zh, rng,
                                 exclude=line.traditional),
                    rng, hint=line.english, source=source,
                ))

    return [ex for ex in out if ex is not None]
