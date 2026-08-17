# Copyright (c) 2026 Wilkend. All rights reserved.
# Hantalk - proprietary software. See LICENSE at the repository root.
# Unauthorized copying, modification, or redistribution is prohibited.

"""Lesson 1 — 你叫什麼名字 / What Is Your Name?

from models.dialogue import Dialogue, DialogueLine
from models.grammar_pattern import GrammarPattern
from models.lesson import Lesson
from models.vocabulary_entry import VocabularyEntry


LESSON_01 = Lesson(
    number=1,
    traditional="你叫什麼名字",
    english="What Is Your Name?",
    dialogue=Dialogue(
        scene="校園",
        scene_en="On campus",
        lines=[
            DialogueLine(
                speaker="王美美",
                avatar="美",
                traditional="你好！",
                pinyin="nǐ hǎo",
                english="Hello!",
                is_left=True,
            ),
            DialogueLine(
                speaker="李明",
                avatar="明",
                traditional="你好！你叫什麼名字？",
                pinyin="nǐ hǎo! nǐ jiào shénme míngzi?",
                english="Hello! What's your name?",
                is_left=False,
            ),
        ],
    ),
    vocabulary=[
        VocabularyEntry(
            traditional="名字",
            pinyin="míngzi",
            pos="noun",
            english="name",
            example_zh="我的名字是李明。",
            example_pinyin="wǒ de míngzi shì Lǐ Míng",
            example_en="My name is Li Ming.",
        ),
    ],
    patterns=[
        GrammarPattern(
            title="Pattern 1",
            formula="我叫 + 名字",
            explanation="Subject + 叫 + name. Used to state or ask a name.",
            headers=["Subject", "Verb", "Name"],
            rows=[
                ["我", "叫", "李明"],
                ["你", "叫", "什麼名字"],
            ],
        ),
    ],
    culture_note="In Taiwan, family names come first...",
)
"""

"""Lesson 1 — 你叫什麼名字 / What Is Your Name?"""

from models.dialogue import Dialogue, DialogueLine
from models.grammar_pattern import GrammarPattern
from models.lesson import Lesson
from models.vocabulary_entry import VocabularyEntry

LESSON_01 = Lesson(
    number=1,
    traditional="你叫什麼名字",
    english="What Is Your Name?",
    dialogue=Dialogue(
        scene="校園",
        scene_en="On campus",
        lines=[
            DialogueLine(
                speaker="林安安",
                avatar="安",
                traditional="你好！",
                pinyin="nǐ hǎo!",
                english="Hello!",
                is_left=True,
            ),
            DialogueLine(
                speaker="杜凱文",
                avatar="凱",
                traditional="你好！我叫杜凱文，你叫什麼名字？",
                pinyin="nǐ hǎo! wǒ jiào Dù Kǎiwén, nǐ jiào shénme míngzi?",
                english="Hello! My name is Du Kaiwen. What's your name?",
                is_left=False,
            ),
            DialogueLine(
                speaker="林安安",
                avatar="安",
                traditional="我叫林安安。你是哪國人？",
                pinyin="wǒ jiào Lín Ān'ān. nǐ shì nǎ guó rén?",
                english="My name is Lin An'an. Which country are you from?",
                is_left=True,
            ),
            DialogueLine(
                speaker="杜凱文",
                avatar="凱",
                traditional="我是加拿大人，你呢？",
                pinyin="wǒ shì Jiānádà rén, nǐ ne?",
                english="I'm Canadian. And you?",
                is_left=False,
            ),
            DialogueLine(
                speaker="林安安",
                avatar="安",
                traditional="我是臺灣人。你是學生嗎？",
                pinyin="wǒ shì Táiwān rén. nǐ shì xuéshēng ma?",
                english="I'm Taiwanese. Are you a student?",
                is_left=True,
            ),
            DialogueLine(
                speaker="杜凱文",
                avatar="凱",
                traditional="我是學生，我不是老師。",
                pinyin="wǒ shì xuéshēng, wǒ bú shì lǎoshī.",
                english="I'm a student. I'm not a teacher.",
                is_left=False,
            ),
        ],
    ),
    vocabulary=[
        VocabularyEntry(
            traditional="你好",
            pinyin="nǐ hǎo",
            pos="phrase",
            english="hello; hi",
            example_zh="老師，你好！",
            example_pinyin="lǎoshī, nǐ hǎo!",
            example_en="Hello, teacher!",
        ),
        VocabularyEntry(
            traditional="我",
            pinyin="wǒ",
            pos="pronoun",
            english="I; me",
            example_zh="我是學生。",
            example_pinyin="wǒ shì xuéshēng.",
            example_en="I am a student.",
        ),
        VocabularyEntry(
            traditional="你",
            pinyin="nǐ",
            pos="pronoun",
            english="you",
            example_zh="你是加拿大人。",
            example_pinyin="nǐ shì Jiānádà rén.",
            example_en="You are Canadian.",
        ),
        VocabularyEntry(
            traditional="您",
            pinyin="nín",
            pos="pronoun",
            english="you (polite)",
            example_zh="您是林老師嗎？",
            example_pinyin="nín shì Lín lǎoshī ma?",
            example_en="Are you Teacher Lin?",
        ),
        VocabularyEntry(
            traditional="叫",
            pinyin="jiào",
            pos="verb",
            english="to be called (by a given name or full name)",
            example_zh="他叫杜凱文。",
            example_pinyin="tā jiào Dù Kǎiwén.",
            example_en="He is called Du Kaiwen.",
        ),
        VocabularyEntry(
            traditional="姓",
            pinyin="xìng",
            pos="verb",
            english="to have the surname; surname",
            example_zh="我姓林，不姓杜。",
            example_pinyin="wǒ xìng Lín, bú xìng Dù.",
            example_en="My surname is Lin, not Du.",
        ),
        VocabularyEntry(
            traditional="名字",
            pinyin="míngzi",
            pos="noun",
            english="name",
            example_zh="安安是我的名字。",
            example_pinyin="Ān'ān shì wǒ de míngzi.",
            example_en="An'an is my name.",
        ),
        VocabularyEntry(
            traditional="什麼",
            pinyin="shénme",
            pos="question word",
            english="what",
            example_zh="他姓什麼？",
            example_pinyin="tā xìng shénme?",
            example_en="What is his surname?",
        ),
        VocabularyEntry(
            traditional="是",
            pinyin="shì",
            pos="verb",
            english="to be (am, is, are)",
            example_zh="安安是臺灣人。",
            example_pinyin="Ān'ān shì Táiwān rén.",
            example_en="An'an is Taiwanese.",
        ),
        VocabularyEntry(
            traditional="不",
            pinyin="bù",
            pos="adverb",
            english="not; no",
            example_zh="他不是老師。",
            example_pinyin="tā bú shì lǎoshī.",
            example_en="He is not a teacher.",
        ),
        VocabularyEntry(
            traditional="嗎",
            pinyin="ma",
            pos="particle",
            english="question particle (yes/no questions)",
            example_zh="你是學生嗎？",
            example_pinyin="nǐ shì xuéshēng ma?",
            example_en="Are you a student?",
        ),
        VocabularyEntry(
            traditional="呢",
            pinyin="ne",
            pos="particle",
            english="question particle (how about ...?)",
            example_zh="我是臺灣人，你呢？",
            example_pinyin="wǒ shì Táiwān rén, nǐ ne?",
            example_en="I'm Taiwanese. And you?",
        ),
        VocabularyEntry(
            traditional="哪",
            pinyin="nǎ",
            pos="question word",
            english="which",
            example_zh="她是哪國人？",
            example_pinyin="tā shì nǎ guó rén?",
            example_en="Which country is she from?",
        ),
        VocabularyEntry(
            traditional="國",
            pinyin="guó",
            pos="noun",
            english="country; nation",
            example_zh="臺灣、加拿大都是國名。",
            example_pinyin="Táiwān, Jiānádà dōu shì guó míng.",
            example_en="Taiwan and Canada are both country names.",
        ),
        VocabularyEntry(
            traditional="人",
            pinyin="rén",
            pos="noun",
            english="person; people",
            example_zh="他是加拿大人。",
            example_pinyin="tā shì Jiānádà rén.",
            example_en="He is Canadian.",
        ),
        VocabularyEntry(
            traditional="誰",
            pinyin="shéi",
            pos="question word",
            english="who; whom",
            example_zh="誰是林安安？",
            example_pinyin="shéi shì Lín Ān'ān?",
            example_en="Who is Lin An'an?",
        ),
        VocabularyEntry(
            traditional="他",
            pinyin="tā",
            pos="pronoun",
            english="he; him",
            example_zh="他叫杜凱文。",
            example_pinyin="tā jiào Dù Kǎiwén.",
            example_en="He is called Du Kaiwen.",
        ),
        VocabularyEntry(
            traditional="她",
            pinyin="tā",
            pos="pronoun",
            english="she; her",
            example_zh="她姓林。",
            example_pinyin="tā xìng Lín.",
            example_en="Her surname is Lin.",
        ),
        VocabularyEntry(
            traditional="先生",
            pinyin="xiānshēng",
            pos="noun",
            english="Mr.; sir; husband",
            example_zh="杜先生是加拿大人。",
            example_pinyin="Dù xiānshēng shì Jiānádà rén.",
            example_en="Mr. Du is Canadian.",
        ),
        VocabularyEntry(
            traditional="小姐",
            pinyin="xiǎojiě",
            pos="noun",
            english="Miss; young lady",
            example_zh="林小姐叫安安。",
            example_pinyin="Lín xiǎojiě jiào Ān'ān.",
            example_en="Miss Lin's given name is An'an.",
        ),
        VocabularyEntry(
            traditional="老師",
            pinyin="lǎoshī",
            pos="noun",
            english="teacher",
            example_zh="我不是老師，我是學生。",
            example_pinyin="wǒ bú shì lǎoshī, wǒ shì xuéshēng.",
            example_en="I'm not a teacher, I'm a student.",
        ),
        VocabularyEntry(
            traditional="學生",
            pinyin="xuéshēng",
            pos="noun",
            english="student",
            example_zh="凱文是學生。",
            example_pinyin="Kǎiwén shì xuéshēng.",
            example_en="Kaiwen is a student.",
        ),
        VocabularyEntry(
            traditional="臺灣",
            pinyin="Táiwān",
            pos="proper noun",
            english="Taiwan",
            example_zh="我是臺灣人。",
            example_pinyin="wǒ shì Táiwān rén.",
            example_en="I am Taiwanese.",
        ),
        VocabularyEntry(
            traditional="加拿大",
            pinyin="Jiānádà",
            pos="proper noun",
            english="Canada",
            example_zh="凱文是加拿大人。",
            example_pinyin="Kǎiwén shì Jiānádà rén.",
            example_en="Kaiwen is Canadian.",
        ),
        VocabularyEntry(
            traditional="貴姓",
            pinyin="guìxìng",
            pos="phrase",
            english="your honorable surname (polite)",
            example_zh="您貴姓？",
            example_pinyin="nín guìxìng?",
            example_en="May I ask your surname?",
        ),
    ],
    patterns=[
        GrammarPattern(
            title="Pattern 1 — Giving a name with 叫",
            formula="Subject + (不) 叫 + 名字",
            explanation=(
                "叫 introduces a given name or a full name. Negate it with 不. "
                "叫 is never used with a surname alone."
            ),
            headers=["Subject", "(Neg-) Verb", "Name"],
            rows=[
                ["我", "叫", "林安安"],
                ["他", "叫", "凱文"],
                ["她", "不叫", "安安"],
                ["你", "叫", "什麼名字"],
            ],
        ),
        GrammarPattern(
            title="Pattern 2 — Giving a surname with 姓",
            formula="Subject + (不) 姓 + 姓",
            explanation=(
                "姓 takes only the family name. To ask politely, use 您貴姓？ — "
                "the answer is 我姓 + surname, never 我貴姓."
            ),
            headers=["Subject", "(Neg-) Verb", "Surname"],
            rows=[
                ["我", "姓", "杜"],
                ["我", "不姓", "林"],
                ["他", "姓", "什麼"],
                ["您", "貴姓", "？"],
            ],
        ),
        GrammarPattern(
            title="Pattern 3 — Identity with 是",
            formula="Subject + (不) 是 + Noun",
            explanation=(
                "是 links two nouns: A is B. Use 是 with titles such as 先生, "
                "小姐, 老師. A noun placed before another noun modifies it: "
                "臺灣人 = Taiwan person = Taiwanese."
            ),
            headers=["Subject", "(Neg-) 是", "Noun"],
            rows=[
                ["我", "是", "臺灣人"],
                ["凱文", "是", "加拿大人"],
                ["他", "不是", "老師"],
                ["林小姐", "是", "學生"],
            ],
        ),
        GrammarPattern(
            title="Pattern 4 — Yes/no questions with 嗎",
            formula="Statement + 嗎？",
            explanation=(
                "Add 嗎 to the end of a statement; the word order does not change. "
                "Answer by repeating the verb: 是 / 不是, 姓 / 不姓."
            ),
            headers=["Question", "Positive answer", "Negative answer"],
            rows=[
                ["你是學生嗎？", "我是學生。", "我不是學生。"],
                ["他姓林嗎？", "他姓林。", "他不姓林。"],
                ["您是老師嗎？", "我是老師。", "我不是老師。"],
            ],
        ),
        GrammarPattern(
            title="Pattern 5 — Question words stay in place",
            formula="Subject + Verb + 什麼 / 誰 / 哪國",
            explanation=(
                "Chinese question words sit exactly where the answer will sit. "
                "Nothing moves to the front of the sentence."
            ),
            headers=["Question", "Answer"],
            rows=[
                ["你叫什麼名字？", "我叫林安安。"],
                ["他姓什麼？", "他姓杜。"],
                ["誰是加拿大人？", "凱文是加拿大人。"],
                ["她是哪國人？", "她是臺灣人。"],
            ],
        ),
        GrammarPattern(
            title="Pattern 6 — Follow-up questions with 呢",
            formula="Statement，Subject + 呢？",
            explanation=(
                "呢 bounces the same question back without repeating it. "
                "Say the statement first, then the new subject plus 呢."
            ),
            headers=["Statement", "Follow-up", "Reply"],
            rows=[
                ["我是臺灣人，", "你呢？", "我是加拿大人。"],
                ["我姓林，", "你呢？", "我姓杜。"],
                ["凱文是學生，", "安安呢？", "安安也是學生。"],
            ],
        ),
    ],
    culture_note=(
        "Chinese names run surname first, given name second: in 林安安, 林 is the "
        "family name and 安安 the given name. Family names are usually one syllable "
        "and given names one or two, so a full name is most often three characters.\n\n"
        "Titles follow the surname rather than precede it — 杜先生 is Mr. Du, "
        "林老師 is Teacher Lin. Calling someone by their full name is normal at a "
        "first meeting; close friends switch to the given name alone, or double the "
        "last syllable (安安) as a nickname.\n\n"
        "您貴姓？ is the polite way to ask a surname, used with older people, "
        "customers, or anyone in a formal setting. Answer with the plain 我姓…, "
        "since 貴 is a courtesy you extend to others and never to yourself.\n\n"
        "Pronunciation note: 不 is fourth tone (bù), but before another fourth tone "
        "it shifts to second tone — 不是 is read bú shì, not bù shì."
    ),
)