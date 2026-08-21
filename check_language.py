"""Fail if any Creole is left in a string literal or comment.

Why a dictionary and not a keyword list: two keyword-based sweeps both
missed `SEKSYON`, `KONTINYE` and `NÒT KILTIRÈL`, because you cannot list
words you forgot exist. This checks every word against an English
dictionary instead and reports what it does not recognise.

Run:  python check_language.py
"""
import ast, io, os, re, sys, tokenize

try:
    from english_words import get_english_words_set
except ImportError:
    sys.exit("pip install english-words")

WORDS = get_english_words_set(["web2"], lower=True)

# Words the dictionary does not carry: tech terms, brand names, pinyin,
# and regular inflections (web2 has no -ed/-ing/-s forms).
ALLOW = set("""
app apps ui ux api url urls http https json css html svg png mp3 apk sqlite
async await bool str int float dict enum dataclass kwargs args repr init
pinyin bopomofo tongyong hanzi mandarin taiwanese taiwan duolingo hellochinese
flet flutter dart python xp combo streak flashcard flashcards ok todo eg ie vs
etc msg config nav mic tts stt ai id ids uuid px ms hex rgb dp regex regexes
utf ascii rfc wcag hsk pavc fafu hantalk wilkend noto notosans notosanstc
notoseriftc ttf squircle wordmark gridlines colorscheme bgcolor textfield
typeerror keyerror tabbar tabbarview navigationbar sharedpreferences deepcopy
dialogueline vocabularyentry grammarpattern exercisekind callout waveform
fullscreen viewport popup popups onboarding scrollable clickable tappable
timezone runtime login logout signup username email placeholder placeholders
backend frontend fallback fallbacks lifecycle docstring docstrings gamification
requeue requeued reshuffle reshuffled distractor distractor distractors
unwinnable rollback optimistic prefs stat stats trad neg adj lib vocab demo
handoff avatar auth box google facebook github gmail com willa cta arg rng prev
info validators checkmark widgets metadata subtitle subtitles boolean uppercase
lowercase keystroke stinky nominalizer kaiwen anan hanyu chen lin du zhong startup ang eng pixels pixel artwork initialization mingzi
""".split())

# `[^\W\d_]` keeps accented letters inside one word, so a pinyin syllable
# like `lǎoshī` stays whole instead of splitting into `osh`.
WORD = re.compile(r"[^\W\d_]{3,}(?:'[^\W\d_]+)?", re.UNICODE)
CJK = re.compile(r"[⺀-鿿＀-￯㄀-ㄯ]")
# Pinyin syllables carry tone marks; skip any word that has one.
TONED = re.compile(r"[āáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜüê]")
HEXISH = re.compile(r"^[0-9a-f]+$")

SUFFIXES = ("s", "es", "ed", "d", "ing", "ly", "er", "est", "ers", "ings")


def _stems(w: str):
    """Every plausible dictionary form of `w`. web2 has no inflections."""
    yield w
    if "'" in w:                       # hantalk's → hantalk
        head = w.split("'")[0]
        yield head
        if w.endswith("n't"):          # doesn't → does,  aren't → are
            yield head[:-1] if head.endswith("n") else head
    for suf in SUFFIXES:
        if not w.endswith(suf) or len(w) - len(suf) < 2:
            continue
        stem = w[: -len(suf)]
        yield stem
        yield stem + "e"               # flipping → flipe? no; making → make
        if stem.endswith("i"):
            yield stem[:-1] + "y"      # activities → activity
        if len(stem) > 2 and stem[-1] == stem[-2]:
            yield stem[:-1]            # dropped → drop, planned → plan


def known(word: str) -> bool:
    w = word.lower()
    if len(w) <= 2 or w in ALLOW or HEXISH.match(w) or TONED.search(w):
        return True
    return any(s in WORDS or s in ALLOW for s in _stems(w))


def scan(path: str):
    src = io.open(path, encoding="utf-8").read()
    chunks = []
    try:
        for node in ast.walk(ast.parse(src)):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                chunks.append((node.lineno, node.value))
    except SyntaxError as exc:
        print(f"  !! {path}: {exc}")
    for tok in tokenize.generate_tokens(io.StringIO(src).readline):
        if tok.type == tokenize.COMMENT:
            chunks.append((tok.start[0], tok.string))
    for line, text in chunks:
        text = CJK.sub(" ", text)
        for w in WORD.findall(text):
            if "_" not in w and not known(w):
                yield line, w, text.strip()[:70]


def main() -> int:
    found = 0
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in (".venv", "__pycache__", ".git")]
        for f in sorted(files):
            if not f.endswith(".py") or f == os.path.basename(__file__):
                continue
            p = os.path.join(root, f)
            for line, word, text in scan(p):
                print(f"  {p}:{line}  {word!r}\n      {text}")
                found += 1
    print()
    if found:
        print(f"❌ {found} word(s) not recognised — translate them, "
              f"or add real English/technical terms to ALLOW")
    else:
        print("✅ no unrecognised words — the project reads as English")
    return 1 if found else 0


if __name__ == "__main__":
    raise SystemExit(main())
