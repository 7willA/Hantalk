# Hantalk — Audio Plan

Status: **draft, nothing built yet** · Written 2026-08-18

Today `assets/audio/` is empty, `services/audio_service.py` and `data/audio_map.py`
are empty stubs, and `flet-audio` is not installed. The phonetic player in
`views/lesson/phonetic_view.py` is a mockup — a hardcoded `ProgressBar(value=0.45)`
and the text "0:02 / 0:04". This document is the plan to make it real.

---

## 1. The core decision: two tiers of audio

Hantalk has two kinds of audio and they do **not** have the same requirements.

| | Vocabulary | Dialogue |
|---|---|---|
| Content | Isolated words (名字, 老師) | Full sentences |
| What matters | Correct tone per syllable | Tone sandhi, rhythm, emotion |
| TTS quality | Excellent — indistinguishable in practice | Flat, mechanical |
| Plan | **TTS, permanently.** Never needs replacing. | **TTS now, human voice later** — lesson by lesson |

This split is what makes the whole thing affordable. Roughly 80% of the audio
files are vocabulary, and that 80% is *finished the day it is generated*.

Human recording effort is therefore reserved for ~6 dialogue lines per lesson —
about 72 lines across all 12 lessons. That is one afternoon with two native
speakers, not a multi-week project.

---

## 2. Tooling: `edge-tts`

[`edge-tts`](https://github.com/rany2/edge-tts) is a Python package that uses
Microsoft Edge's online text-to-speech service.

Why this one:

- **Free, no API key, no account, no billing setup.**
- Ships real Taiwanese Mandarin neural voices (`zh-TW-*`), not Mainland `zh-CN`.
  This matters — Hantalk teaches traditional characters and Taiwan usage.
- Supports `rate` adjustment, which gives a genuine slow reading rather than a
  pitch-shifted playback.

**Critical point: `edge-tts` runs on the development PC, never inside the app.**
Audio files are generated once, committed, and bundled into the APK. The app has
no network dependency, no API key in the binary, and no per-user cost.

Install:

```bash
pip install edge-tts
```

### Risk

`edge-tts` is an unofficial wrapper around a Microsoft endpoint. It has broken
before when Microsoft changed the service. This is acceptable **because it is a
build-time tool**: if it breaks, already-generated files keep working, and the
fallback (Google Cloud TTS or Azure Speech, both with free tiers well above our
volume) only affects future generation.

---

## 3. Voice casting

Verify the exact available voice names first — this list changes:

```bash
edge-tts --list-voices | grep zh-TW
```

There are only about **three** `zh-TW` neural voices, and Hantalk already has
four speaking characters. Proposed assignment:

| Character | Sex | Voice | Notes |
|---|---|---|---|
| 林安安 | F | `zh-TW-HsiaoChenNeural` | Main student, Lesson 1 |
| 杜凱文 | M | `zh-TW-YunJheNeural` | Main student, Lesson 1 |
| 陳老師 | F | `zh-TW-HsiaoYuNeural` | Teacher — distinct from 安安 |
| 李明 | M | `zh-TW-YunJheNeural` + `pitch=+8Hz` | Shares the male voice |
| Vocabulary | — | `zh-TW-HsiaoChenNeural` | One neutral voice throughout |

The pitch offset on 李明 is a workaround, not a solution. If two male characters
appear in the *same* dialogue, the ear will notice. Two options if that becomes a
problem: prioritise those lines for human recording, or avoid putting two male
characters in one scene when writing lessons 3–12.

Casting lives in **one dictionary** in the generator script, keyed by speaker
name, with a fallback voice for unknown speakers. Adding a character is one line.

---

## 4. File naming: derive, never map

**`data/audio_map.py` should be deleted.** A lookup table mapping content to
filenames is a second source of truth that has to be kept in sync forever.

Instead the path is *computed* from data the app already has:

```
assets/audio/L01/d01.mp3         dialogue line 1, normal speed
assets/audio/L01/d01_slow.mp3    dialogue line 1, slow
assets/audio/L01/v01.mp3         vocabulary entry 1
assets/audio/L01/v01_slow.mp3
```

- `L{lesson:02d}` — lesson number, zero-padded
- `d{index:02d}` / `v{index:02d}` — 1-based position in `lesson.dialogue.lines`
  or `lesson.vocabulary`
- `_slow` suffix for the reduced-rate version

One helper function produces this path. Nothing to maintain, nothing to
desynchronise. The existing `DialogueLine.audio` and `VocabularyEntry.audio`
fields stay, but only as an **override** for special cases — empty means "use
the derived path".

### Why not one file plus playback-rate control?

Because it is uncertain whether `flet-audio` 0.85 exposes a playback rate, and
because a TTS engine reading slowly produces clearer, more natural speech than
software-slowing a normal recording. Two files removes both the uncertainty and
the quality loss, and costs about 5 MB.

---

## 5. The generator script

`tools/generate_audio.py` — **idempotent and re-runnable**.

Behaviour:

1. Walk `ALL_LESSONS`.
2. For every dialogue line and vocabulary entry, compute both target paths.
3. **If the file already exists, skip it.**
4. Otherwise call `edge-tts` with the cast voice, write the file.
5. Print a summary: generated / skipped / failed.

Point 3 is the whole design. It means:

- Writing real content for lesson 5 next month → re-run → only lesson 5 generates.
- Recording a human voice for lesson 1 → drop the file in place → the script
  will never overwrite it.

This is deliberately the same principle as `fill_demo_content()` in
`data/lessons/all_lessons.py`: **whatever already exists wins.**

Flags worth having: `--lesson N` to regenerate one lesson, and `--force` to
overwrite (needed when a lesson's text is corrected).

### Output format

- MP3, mono, 32 kbps — speech at this bitrate is clean, and it keeps the APK small.
- Normal speed: default rate. Slow: `rate="-25%"`.

---

## 6. Playback in the app

- Add `flet-audio` to `requirements.txt`.
- `services/audio_service.py` exposes: play a path, stop, toggle normal/slow.
- `assets_dir="assets"` is already set in `main.py`, so `assets/audio/...` is
  bundled automatically.
- `controls/audio_button.py` already exists as a stub — it becomes the single
  reusable play button used by the dialogue view, vocab cards, and phonetic view.

Then `phonetic_view.py`'s fake player is replaced with a real one: the
`ProgressBar` bound to actual position, real duration text, and the Normal/Slow
pills wired to the two files.

---

## 7. Order of work

Do **not** generate all 12 lessons first. The point of this order is to get a
definitive answer on packaging while only one new dependency is in play.

| Step | Action | Answers |
|---|---|---|
| 1 | `pip install edge-tts`, generate **Lesson 1 only** (~62 files, ~5 min) | Do the voices sound right? Are the tones correct? |
| 2 | `pip install flet-audio`, one button that plays one file, tested in the Flet companion app | Does playback work at all? |
| 3 | **`flet build apk`** | Does `flet-audio` survive packaging? This is the real question, and only one new package can be blamed if it fails. |
| 4 | If step 3 passes → generate lessons 2–12 | — |

Step 3 is the first APK build of the project. It is deliberately placed here:
the app currently has exactly one dependency (`flet`), so `flet-audio` is the
only variable.

---

## 8. Volume and size budget

Actual counts from the current codebase:

| Lesson | Dialogue lines | Vocabulary | Items | Files (×2 speeds) |
|---|---|---|---|---|
| 1 | 6 | 25 | 31 | 62 |
| 2 | 6 | 8 | 14 | 28 |
| 3–12 | not written yet | not written yet | ~21 est. | ~420 est. |
| **Total** | | | **~255** | **~510** |

At 32 kbps mono and ~2.5 s average length, roughly **10 KB per file → ~5 MB
total**. Comfortably acceptable inside an APK.

Note: lessons 3–12 currently borrow lesson 1–2 content through
`fill_demo_content()`. Audio should **not** be generated for borrowed content —
the generator must skip any lesson whose content is still borrowed, or it will
produce hundreds of duplicate files that get thrown away. This needs a flag on
`Lesson` (e.g. `has_own_content`) or a check against `fill_demo_content`.

---

## 9. Path to human recordings

When real voices are recorded, nothing in the app changes:

1. Record the ~6 dialogue lines for a lesson (normal and slow, or slow generated
   by the speaker reading slowly — not software).
2. Export as mono MP3, 32 kbps, matching the derived filenames.
3. Drop them into `assets/audio/L0N/`.
4. The generator skips them forever after.

Recording target order: Lesson 1 first (it is the demo everyone sees), then in
lesson order.

Vocabulary is **not** on this list. TTS is good enough for isolated words
permanently.

---

## 10. Explicitly out of scope

- **Speech recognition / pronunciation scoring.** Separate problem, later.
- **Real-time pitch contour.** Not viable in Flet — no PCM stream into Python.
  Tone feedback, when it comes, will be record → stop → analyse → draw once.
- **Streaming audio from a server.** Everything ships in the APK.
- **Dangdai textbook audio.** Reference only — copyright. Never shipped.

---

## 11. Open questions

- [ ] Confirm the exact `zh-TW` voice names with `edge-tts --list-voices`.
- [ ] Decide how the generator detects borrowed vs. original lesson content.
- [ ] Confirm `flet-audio` 0.85 API: does it report position/duration, needed for
      a real progress bar in `phonetic_view`?
- [ ] Is 32 kbps acceptable for tone clarity, or is 48 kbps needed? Test in step 1.
