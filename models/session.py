# Copyright (c) 2026 Wilkend. All rights reserved.
# Hantalk - proprietary software. See LICENSE at the repository root.
# Unauthorized copying, modification, or redistribution is prohibited.

"""Session — eta yon sesyon egzèsis.

Flutter counterpart: pa gen — se yon nivo nouvo.

SE PYÈS KI TE MANKE ANT `Exercise` AK EKRAN AN

  San li, ekran an ta oblije kenbe liy nan, konte bon repons yo, epi
  deside kilè sesyon an fini — twa bagay ki pa gen anyen pou wè ak
  desine. Isit la, ekran an jis mande: ki kesyon kounye a, epi li rele
  `answer()`. Tout rès la fèt anndan.

PA GEN KÈ, PA GEN PINISYON

  Lè w twonpe w, egzèsis la RETOUNEN nan liy nan, ~3 kesyon pi devan.
  Se sa ki ranplase kè Duolingo yo.

  De rezon:
    1. Se yon KONSEKANS reyèl — sesyon w vin pi long.
    2. Se repetisyon espase andedan yon sesyon, ki se sa ki reyèlman
       fè moun aprann. Yon kè ki disparèt pa anseye anyen.

  Konsekans lan: `queue` GRANDI pandan sesyon an. Se poutèt sa pwogrè a
  konte `cleared / planned` epi non `index / len(queue)` — sinon ba a
  ta rekile chak fwa ou fè yon erè, epi sa ta dekourajan.
"""

import random
from dataclasses import dataclass, field

from models.exercise import Exercise, ExerciseKind

DEFAULT_SIZE = 12
"""Konbyen egzèsis nan yon sesyon.

Duolingo rete ant 12 ak 20. Nou pran 12 — yon sesyon 2–3 minit. Yon
leson bay 80+ egzèsis posib, donk nou pa manke; se rit la n ap pwoteje.
"""

REQUEUE_GAP = 3
"""Konbyen kesyon apre ou yon egzèsis rate retounen."""


def _mixed_sample(
    pool: list[Exercise],
    size: int,
    rng: random.Random,
) -> list[Exercise]:
    """Chwazi `size` egzèsis, men ak yon MELANJ kalite.

    Si nou te jis pran o aza, yon sesyon ta ka bay 12 REKONET youn dèyè
    lòt — menm bagay la 12 fwa. Isit la nou gwoupe pa kalite, epi nou
    pran youn nan chak kalite atou wonn, jiskaske nou gen ase.
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
    """Konbyen egzèsis DISTENK sesyon an gen. Li pa janm chanje."""

    rng: random.Random = field(default_factory=random.Random)

    index: int = 0
    cleared: int = 0
    """Konbyen egzèsis ki repons kòrèk. Li rive nan `planned` nan fen."""

    mistakes: int = 0
    """Konbyen move repons ANTOU (yon egzèsis ka konte plizyè fwa)."""

    # ── Konstwiksyon ─────────────────────────────────────────

    @classmethod
    def for_lesson(cls, lesson, size: int = DEFAULT_SIZE) -> "Session":
        """Yon sesyon pou yon leson. Lòd la chanje chak fwa."""
        from services.exercise_generator import generate_exercises

        rng = random.Random()
        pool = generate_exercises(lesson)
        queue = _mixed_sample(pool, size, rng)
        return cls(queue=queue, planned=len(queue), rng=rng)

    # ── Lekti ────────────────────────────────────────────────

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
        """Leson an pa gen ase kontni pou fè yon sesyon."""
        return self.planned == 0

    @property
    def progress(self) -> float:
        """Ant 0.0 ak 1.0 — sa ba a anwo a montre."""
        if not self.planned:
            return 0.0
        return min(1.0, self.cleared / self.planned)

    @property
    def position(self) -> str:
        """'4 / 12' — kote nou ye nan sesyon an."""
        return f"{min(self.cleared + 1, self.planned)} / {self.planned}"

    @property
    def accuracy(self) -> int:
        """Pousantaj bon repons, 0–100.

        Chak egzèsis konte yon sèl bon repons (`planned`), epi chak erè
        ajoute yon tantativ anplis.
        """
        attempts = self.planned + self.mistakes
        if not attempts:
            return 0
        return round(100 * self.planned / attempts)

    # ── Aksyon ───────────────────────────────────────────────

    def answer(self, choice: str) -> bool:
        """Anrejistre yon repons epi avanse. Retounen si li te bon.

        Sou yon erè, egzèsis la retounen nan liy nan ak chwa yo melanje
        ankò — konsa moun nan pa ka sonje POZISYON bon repons lan.
        """
        exercise = self.current
        if exercise is None:
            return False

        correct = exercise.is_correct(choice)
        if correct:
            self.cleared += 1
        else:
            self.mistakes += 1
            where = min(self.index + REQUEUE_GAP, len(self.queue))
            self.queue.insert(where, exercise.reshuffled(self.rng))

        self.index += 1
        return correct
