# Copyright (c) 2026 Wilkend. All rights reserved.
# Hantalk - proprietary software. See LICENSE at the repository root.
# Unauthorized copying, modification, or redistribution is prohibited.

"""Exercise model — yon sèl kesyon nan bouk la.

Flutter counterpart: pa gen — se yon nivo nouvo.

YON SÈL KLAS, PA YON KLAS PA KALITE

  Tout egzèsis yo gen menm fòm: yon kesyon, yon bon repons, kèk chwa.
  Sa ki chanje se KI KOTE tèks la soti ak KI FONT ki sèvi. Donk yon sèl
  `Exercise` ak yon `kind`, epi ekran an gade `kind` la.

  Si nou te fè yon klas pa kalite, ekran an ta bezwen yon `isinstance()`
  pou chak — epi ajoute yon kalite ta vle di touche ekran an. Konsa, li
  pa touche anyen.

SA KI PA NAN FICHYE SA A

  Pa gen jenerasyon isit la (gade `services/exercise_generator.py`) ni
  eta sesyon an (gade `models/session.py`). Yon `Exercise` pa konnen si
  li reponn oswa non — se `Session` ki sonje sa.
"""

from dataclasses import dataclass, field
from enum import Enum


class ExerciseKind(str, Enum):
    """Kalite kesyon. Valè a se yon tèks pou nou ka sove l pi ta."""

    REKONET = "rekonet"
    """名字 → «name». Wè karaktè a, jwenn sans lan."""

    SONJE = "sonje"
    """«name» → 名字. Sans lan bay, jwenn karaktè a. Pi difisil."""

    PINYIN = "pinyin"
    """名字 → míngzi. Move chwa yo se MENM silab ak MOVE TON.

    Se egzèsis ton ki mache SAN mikwo. Duolingo pa fè sa.
    """

    TRADWI = "tradwi"
    """你叫什麼名字？ → «What's your name?». Yon fraz antye."""

    REPONN = "reponn"
    """安安 di yon bagay → ki sa 凱文 reponn.

    Liy dyalòg yo deja nan lòd, donk liy N+1 la SE bon repons lan pou
    liy N. Nou pa ekri anyen — konvèsasyon an bay egzèsis la poukont li.
    """


@dataclass(frozen=True)
class KindMeta:
    """Sa ekran an bezwen konnen pou l desine yon kalite."""

    instruction: str
    """Ti fraz ki chita anwo kesyon an."""

    prompt_zh: bool
    """Èske kesyon an an chinwa? (chwazi font lan)"""

    options_zh: bool
    """Èske chwa yo an chinwa?"""

    prompt_size: int
    """Gwosè tèks kesyon an. Chinwa bezwen pi gwo pase laten."""


KIND_META: dict[ExerciseKind, KindMeta] = {
    ExerciseKind.REKONET: KindMeta("Kisa sa vle di?", True, False, 44),
    ExerciseKind.SONJE: KindMeta("Chwazi bon karaktè a", False, True, 26),
    ExerciseKind.PINYIN: KindMeta("Ki pinyin ki kòrèk?", True, False, 44),
    ExerciseKind.TRADWI: KindMeta("Tradui fraz sa a", True, False, 28),
    ExerciseKind.REPONN: KindMeta("Ki sa ou ta reponn?", True, True, 26),
}


@dataclass
class Exercise:
    kind: ExerciseKind

    prompt: str
    """Sa ki parèt anwo — karaktè, mo anglè, oswa yon fraz."""

    answer: str
    """Bon repons lan. Li DWE ye nan `options`."""

    options: list[str] = field(default_factory=list)
    """Chwa yo, deja melanje. Vid pa janm ta dwe rive."""

    hint: str = ""
    """Ti liy anba kesyon an — pinyin, oswa sa yon moun sot di."""

    audio: str = ""
    """Chemen son an. Vid pou kounye a — gade AUDIO_PLAN.md."""

    source: str = ""
    """Ki mo/liy egzèsis la soti — pou swiv pwogrè pi devan."""

    @property
    def meta(self) -> KindMeta:
        return KIND_META[self.kind]

    def is_correct(self, choice: str) -> bool:
        return choice == self.answer

    def reshuffled(self, rng) -> "Exercise":
        """Yon kopi ak chwa yo nan yon lòt lòd.

        Sèvi lè yon egzèsis retounen nan liy nan apre yon erè: si chwa
        yo rete nan menm plas la, moun nan sonje POZISYON an olye repons
        lan. Se pa sa nou vle anseye.
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
