# Copyright (c) 2026 Wilkend. All rights reserved.
# Hantalk - proprietary software. See LICENSE at the repository root.
# Unauthorized copying, modification, or redistribution is prohibited.

"""Lesson 2 — 早安，你好嗎？ / Good Morning, How Are You?

Focus: greetings, 很 + adjective, 也.
Original Hantalk content.
"""

from models.dialogue import Dialogue, DialogueLine
from models.grammar_pattern import GrammarPattern
from models.lesson import Lesson
from models.vocabulary_entry import VocabularyEntry


LESSON_02 = Lesson(
    number=2,
    traditional="早安，你好嗎？",
    english="Good Morning, How Are You?",
    progress=0.35,
    dialogue=Dialogue(
        scene="教室",
        scene_en="In the classroom",
        lines=[
            DialogueLine(
                speaker="李明",
                avatar="明",
                traditional="老師早！",
                pinyin="lǎoshī zǎo!",
                english="Good morning, teacher!",
                is_left=True,
            ),
            DialogueLine(
                speaker="陳老師",
                avatar="師",
                traditional="早，李明。你好嗎？",
                pinyin="zǎo, Lǐ Míng. nǐ hǎo ma?",
                english="Morning, Li Ming. How are you?",
                is_left=False,
            ),
            DialogueLine(
                speaker="李明",
                avatar="明",
                traditional="我很好，謝謝老師。您呢？",
                pinyin="wǒ hěn hǎo, xièxie lǎoshī. nín ne?",
                english="I'm well, thank you. And you?",
                is_left=True,
            ),
            DialogueLine(
                speaker="陳老師",
                avatar="師",
                traditional="我也很好。今天很忙嗎？",
                pinyin="wǒ yě hěn hǎo. jīntiān hěn máng ma?",
                english="I'm well too. Are you busy today?",
                is_left=False,
            ),
            DialogueLine(
                speaker="李明",
                avatar="明",
                traditional="不太忙。",
                pinyin="bú tài máng.",
                english="Not too busy.",
                is_left=True,
            ),
            DialogueLine(
                speaker="陳老師",
                avatar="師",
                traditional="那很好。明天見！",
                pinyin="nà hěn hǎo. míngtiān jiàn!",
                english="That's good. See you tomorrow!",
                is_left=False,
            ),
        ],
    ),
    vocabulary=[
        VocabularyEntry(
            traditional="早",
            pinyin="zǎo",
            pos="greeting",
            english="morning (short greeting)",
            example_zh="老師早！",
            example_pinyin="lǎoshī zǎo!",
            example_en="Good morning, teacher!",
        ),
        VocabularyEntry(
            traditional="老師",
            pinyin="lǎoshī",
            pos="noun",
            english="teacher",
            example_zh="他是我的中文老師。",
            example_pinyin="tā shì wǒ de Zhōngwén lǎoshī",
            example_en="He is my Chinese teacher.",
        ),
        VocabularyEntry(
            traditional="謝謝",
            pinyin="xièxie",
            pos="verb",
            english="thank you",
            example_zh="謝謝你的幫忙。",
            example_pinyin="xièxie nǐ de bāngmáng",
            example_en="Thank you for your help.",
        ),
        VocabularyEntry(
            traditional="很",
            pinyin="hěn",
            pos="adverb",
            english="very (links subject to adjective)",
            example_zh="今天很熱。",
            example_pinyin="jīntiān hěn rè",
            example_en="It's hot today.",
        ),
        VocabularyEntry(
            traditional="忙",
            pinyin="máng",
            pos="adj",
            english="busy",
            example_zh="我這個星期很忙。",
            example_pinyin="wǒ zhè ge xīngqí hěn máng",
            example_en="I'm very busy this week.",
        ),
        VocabularyEntry(
            traditional="今天",
            pinyin="jīntiān",
            pos="noun",
            english="today",
            example_zh="今天是星期一。",
            example_pinyin="jīntiān shì xīngqíyī",
            example_en="Today is Monday.",
        ),
        VocabularyEntry(
            traditional="明天",
            pinyin="míngtiān",
            pos="noun",
            english="tomorrow",
            example_zh="明天我不上課。",
            example_pinyin="míngtiān wǒ bú shàngkè",
            example_en="I don't have class tomorrow.",
        ),
        VocabularyEntry(
            traditional="見",
            pinyin="jiàn",
            pos="verb",
            english="to see (used in farewells)",
            example_zh="明天見！",
            example_pinyin="míngtiān jiàn!",
            example_en="See you tomorrow!",
        ),
    ],
    patterns=[
        GrammarPattern(
            title="Pattern 1",
            formula="主語 + 很 + 形容詞",
            explanation=(
                "Chinese adjectives act as verbs, so there is no 是 before "
                "them. 很 fills that slot. Without 很 the sentence sounds "
                "like a comparison, not a statement."
            ),
            headers=["Subject", "很", "Adjective"],
            rows=[
                ["我", "很", "好"],
                ["今天", "很", "忙"],
                ["台北", "很", "熱"],
            ],
        ),
        GrammarPattern(
            title="Pattern 2",
            formula="主語 + 也 + 很 + 形容詞",
            explanation=(
                "也 means 'also' and always sits directly before the verb "
                "or 很 — never at the end of the sentence the way English "
                "'too' does."
            ),
            headers=["Subject", "也", "很", "Adjective"],
            rows=[
                ["我", "也", "很", "好"],
                ["他", "也", "很", "忙"],
                ["台南", "也", "很", "熱"],
            ],
        ),
    ],
    culture_note=(
        "老師 is used as a title on its own — students say 老師早 and 謝謝老師 "
        "rather than using the teacher's name. The same holds for 醫生, 經理 "
        "and other professions.\n\n"
        "您 is the respectful form of 你. In Taiwan it is common toward "
        "teachers, elders and customers, but using it with a classmate would "
        "sound stiff or sarcastic.\n\n"
        "早 alone is the everyday morning greeting between people who see "
        "each other daily. 早安 is slightly more formal and is what you hear "
        "on the radio or read in a message."
    ),
)
