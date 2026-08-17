<div align="center">

# Hantalk

**Learn Mandarin Chinese as it is actually used in Taiwan.**

Built with [Flet](https://flet.dev) — one Python codebase, running on desktop, web, and mobile.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Flet](https://img.shields.io/badge/Flet-0.85.3-00C4B4)
![License](https://img.shields.io/badge/License-Proprietary-red)
![Status](https://img.shields.io/badge/Status-In%20development-yellow)

</div>

---

## About

Hantalk teaches **Traditional Chinese** the way it is written and spoken in
Taiwan — not the simplified characters most apps default to. It is built for
international learners: exchange students, degree students, and anyone living in
Taiwan who needs the language that is actually on the signs and in the
classroom.

The core idea is **phonetic flexibility**. Learners in Taiwan encounter several
competing romanization and phonetic systems, and every classroom picks a
different one. Hantalk lets the learner display any combination of four systems
side by side, and switch at any time:

| System | Example (名字) | Common where |
|:--|:--|:--|
| 漢字 Hànzì | 名字 | everywhere |
| ㄅㄆㄇㄈ Bopomofo | ㄇㄧㄥˊ ㄗ˙ | Taiwanese schools |
| Tongyong Pinyin | míngzi | Taiwanese signage |
| Hanyu Pinyin | míngzi | international textbooks |

At least one system always stays enabled, so a lesson can never render blank.

## Features

- **Lesson path** — a visual, node-based progression through units and lessons
- **Dialogues** — two-speaker conversations with per-line phonetics and translation
- **Vocabulary cards** — word, phonetics, part of speech, and meaning
- **Grammar patterns** — pattern tables with worked examples
- **Drills** — practice exercises generated from lesson content
- **AI conversation practice** — free-form speaking practice *(in progress)*
- **Progress tracking** — daily goals and streaks
- **Settings** — phonetic systems, audio speed, daily goal, notifications, light/dark theme, and Chinese text scaling (0.8×–1.4×), all persisted on-device

## Screens

```
/                    splash
/login  /register    authentication
/home                dashboard and lesson path
/unit/{n}            unit overview
/lesson/{n}          lesson: dialogue, vocabulary, grammar
/phonetic/{n}/{i}    per-character phonetic breakdown
/vocab/{n}           vocabulary review for a lesson
/drills              practice drills
/practice            AI conversation
/profile             progress and streaks
/settings            preferences
```

## Project structure

```
hantalk_flet/
├── main.py              entry point — theme, routing, settings bootstrap
├── app/
│   ├── router.py        route table (static + parameterized) → View
│   └── theme.py         design tokens: color, type, spacing, radius
├── models/              domain types (Lesson, Dialogue, VocabularyEntry, …)
├── data/
│   ├── lessons/         lesson content as Python data
│   ├── drills.py        drill definitions
│   └── audio_map.py     text → audio file mapping
├── views/               one package per screen area
├── controls/            reusable widgets (vocab_card, path_node, …)
├── services/            settings, audio, auth, progress, streak
└── assets/
    ├── fonts/           Noto Sans / Noto Sans TC / Noto Serif TC
    ├── images/          logo and brand marks
    └── audio/           pronunciation audio
```

Two architectural notes worth knowing before you read the code, both consequences
of how Flet 0.85 handles services:

1. **Services are attached per-View, not per-Page.** In Flet 0.85,
   `page.services` is really `page.views[0].services`. Since `main.py` clears
   `page.views` on every route change, a service bound to the first View would
   die on the first navigation. `router.resolve()` therefore attaches the
   settings service to *every* View it builds. See `app/router.py`.

2. **Settings load after the first View exists, not before.** `page.update()`
   goes through `page.views[0]`; calling it on an empty list raises
   `RuntimeError("views list is empty.")`. The splash screen's two seconds give
   the disk read time to finish. See the comments in `main.py`.

Settings reads are synchronous by design: `load()` hits the disk once at
startup into an in-memory cache, `get()` reads that cache with no `await`, and
`set()` updates memory immediately and writes to disk behind it. The UI never
waits on I/O, and a failed save degrades to in-memory defaults rather than an
error in the user's face.

> **Note on source comments:** some inline comments are currently in Haitian
> Creole, the author's first language. They are being translated to English as
> the code is revisited. Nothing user-facing is affected.

## Running it

**Requirements:** Python 3.10 or newer.

```powershell
# Windows PowerShell
git clone https://github.com/7willA/Hantalk.git
cd Hantalk

python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

python main.py
```

```bash
# macOS / Linux
git clone https://github.com/7willA/Hantalk.git
cd Hantalk

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python main.py
```

To run it as a web app instead of a desktop window:

```bash
flet run --web main.py
```

### Development helpers

| Script | Purpose |
|:--|:--|
| `python check_data.py` | validate lesson data for missing or malformed fields |
| `python smoke_test.py` | build every route once and confirm nothing raises |
| `python preview.py` | render components in isolation while styling |

## Roadmap

- [ ] Lessons 3 onward
- [ ] Pronunciation audio for all vocabulary
- [ ] Real authentication and cloud progress sync
- [ ] AI conversation backend
- [ ] Speech recognition for pronunciation scoring
- [ ] Multi-language UI localization
- [ ] Android and iOS builds via `flet build`

## Author

**Wilkend** — Computer Science and Information Engineering, National Dong Hwa
University (NDHU), Hualien, Taiwan.

## License

**Proprietary — all rights reserved.** See [LICENSE](LICENSE).

This source is published for viewing, evaluation, and academic review only. It
is not open source: you may read it, but you may not copy, modify, redistribute,
or reuse it in another project without written permission. Third-party
dependencies (Flet, the Noto fonts) remain under their own licenses.
