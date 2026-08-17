# Copyright (c) 2026 Wilkend. All rights reserved.
# Hantalk - proprietary software. See LICENSE at the repository root.
# Unauthorized copying, modification, or redistribution is prohibited.

"""Lesson view — ekran 02 nan handoff la.

5 tab: Dialogue · Vocab · Syntax · Activities · Notes.
Flutter counterpart: lib/screens/lesson/lesson_screen.dart
"""

import flet as ft

from app import theme
from controls.grammar_table import grammar_table
from data.lessons.all_lessons import get_lesson
from models.dialogue import DialogueLine
from models.lesson import Lesson
from models.vocabulary_entry import VocabularyEntry


def _app_bar(page: ft.Page, lesson: Lesson) -> ft.Control:
    async def go_back(e):
        await page.push_route("/home")

    return ft.Row(
        spacing=4,
        height=52,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Container(
                padding=ft.Padding.all(8),
                border_radius=999,
                on_click=go_back,
                content=ft.Icon(ft.Icons.ARROW_BACK, size=24,
                                color=theme.TEXT),
            ),
            ft.Column(
                expand=True,
                spacing=0,
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Text(
                        lesson.traditional,
                        font_family=theme.FONT_ZH,
                        size=19,
                        weight=ft.FontWeight.W_500,
                        color=theme.TEXT,
                        max_lines=1,
                        overflow=ft.TextOverflow.ELLIPSIS,
                    ),
                    ft.Text(
                        f"Lesson {lesson.number} · {lesson.english}",
                        size=11,
                        color=theme.TEXT_MUTED,
                        max_lines=1,
                        overflow=ft.TextOverflow.ELLIPSIS,
                    ),
                ],
            ),
            ft.Container(
                padding=ft.Padding.all(8),
                border_radius=999,
                content=ft.Icon(ft.Icons.BOOKMARK_BORDER, size=24,
                                color=theme.TEXT_SECONDARY),
            ),
            ft.Container(
                padding=ft.Padding.all(8),
                border_radius=999,
                content=ft.Icon(ft.Icons.MORE_VERT, size=24,
                                color=theme.TEXT_SECONDARY),
            ),
        ],
    )


# ── Tab 1 · Dialogue ────────────────────────────────────────────


def _chip(text: str) -> ft.Control:
    return ft.Container(
        padding=ft.Padding.symmetric(vertical=6, horizontal=10),
        bgcolor=theme.SURFACE_VARIANT,
        border=ft.Border.all(1, theme.OUTLINE),
        border_radius=8,
        content=ft.Text(text, size=11, color=theme.TEXT_SECONDARY),
    )


def _bubble(page: ft.Page, line: DialogueLine, index: int,
            lesson_number: int) -> ft.Control:
    """Yon bul chat. Tap → ekran fonetik la."""
    async def open_phonetic(e):
        await page.push_route(f"/phonetic/{lesson_number}/{index}")

    avatar = ft.Container(
        width=38,
        height=38,
        border_radius=999,
        alignment=ft.Alignment.CENTER,
        bgcolor=theme.PRIMARY_CONTAINER if line.is_left else theme.DIVIDER,
        content=ft.Text(
            line.avatar,
            font_family=theme.FONT_ZH,
            size=16,
            weight=ft.FontWeight.W_500,
            color=theme.ON_PRIMARY_DEEP if line.is_left
            else theme.TEXT_SECONDARY,
        ),
    )

    bubble = ft.Container(
        width=264,
        on_click=open_phonetic,
        bgcolor=theme.SURFACE_VARIANT,
        padding=ft.Padding.symmetric(vertical=12, horizontal=14),
        border_radius=ft.BorderRadius(
            top_left=18,
            top_right=18,
            bottom_left=6 if line.is_left else 18,
            bottom_right=18 if line.is_left else 6,
        ),
        content=ft.Column(
            spacing=0,
            controls=[
                ft.Text(
                    line.traditional,
                    font_family=theme.FONT_ZH,
                    size=24,
                    weight=ft.FontWeight.W_500,
                    color=theme.TEXT,
                ),
                ft.Container(height=4),
                ft.Text(line.pinyin, size=12, color=theme.TEXT_MUTED),
                ft.Container(height=6),
                ft.Text(line.english, size=13, color=theme.TEXT_SECONDARY),
            ],
        ),
    )

    controls = [avatar, bubble] if line.is_left else [bubble, avatar]
    return ft.Row(
        spacing=10,
        vertical_alignment=ft.CrossAxisAlignment.START,
        alignment=ft.MainAxisAlignment.START if line.is_left
        else ft.MainAxisAlignment.END,
        controls=controls,
    )


def _tab_dialogue(page: ft.Page, lesson: Lesson) -> ft.Control:
    d = lesson.dialogue
    if d is None:
        return ft.Text("Pa gen dyalòg pou leson sa a.",
                       color=theme.TEXT_MUTED)

    return ft.Column(
        spacing=18,
        controls=[
            ft.Row(
                spacing=8,
                controls=[
                    _chip(f"Scene · {d.scene_en}"),
                    _chip(f"{len(d.lines)} lines"),
                ],
            ),
            *[
                _bubble(page, line, i, lesson.number)
                for i, line in enumerate(d.lines)
            ],
        ],
    )


# ── Tab 2 · Vocab ───────────────────────────────────────────────


def _vocab_row(entry: VocabularyEntry) -> ft.Control:
    return ft.Container(
        padding=ft.Padding.symmetric(vertical=12, horizontal=4),
        border=ft.Border.only(bottom=ft.BorderSide(1, theme.DIVIDER)),
        content=ft.Row(
            spacing=14,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    width=64,
                    content=ft.Text(
                        entry.traditional,
                        font_family=theme.FONT_ZH,
                        size=28,
                        weight=ft.FontWeight.W_500,
                        color=theme.TEXT,
                    ),
                ),
                ft.Column(
                    expand=True,
                    spacing=0,
                    controls=[
                        ft.Text(f"{entry.pinyin} · {entry.pos}",
                                size=12, color=theme.TEXT_MUTED),
                        ft.Text(entry.english, size=14, color=theme.TEXT),
                    ],
                ),
                ft.Icon(ft.Icons.VOLUME_UP, size=22, color=theme.PRIMARY),
            ],
        ),
    )


def _tab_vocab(page: ft.Page, lesson: Lesson) -> ft.Control:
    async def open_cards(e):
        await page.push_route(f"/vocab/{lesson.number}")

    return ft.Column(
        spacing=2,
        controls=[
            *[_vocab_row(v) for v in lesson.vocabulary],
            ft.Container(height=10),
            ft.Button(
                "Study as flashcards",
                icon=ft.Icons.STYLE,
                on_click=open_cards,
                width=10_000,
                height=48,
                bgcolor=theme.PRIMARY,
                color=theme.WHITE,
            ),
        ],
    )


# ── Tab 4 · Activities ──────────────────────────────────────────


def _activity(icon: str, title: str, subtitle: str, on_click) -> ft.Control:
    return ft.Container(
        bgcolor=theme.SURFACE,
        border_radius=16,
        padding=ft.Padding.all(15),
        on_click=on_click,
        content=ft.Row(
            spacing=14,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Icon(icon, size=24, color=theme.PRIMARY),
                ft.Column(
                    expand=True,
                    spacing=0,
                    controls=[
                        ft.Text(title, size=15,
                                weight=ft.FontWeight.W_600, color=theme.TEXT),
                        ft.Text(subtitle, size=12, color=theme.TEXT_MUTED),
                    ],
                ),
                ft.Icon(ft.Icons.CHEVRON_RIGHT, size=22,
                        color=theme.TEXT_MUTED),
            ],
        ),
    )


def _tab_activities(page: ft.Page, lesson: Lesson) -> ft.Control:
    async def go(route):
        await page.push_route(route)

    speaker = "the second speaker"
    if lesson.dialogue and lesson.dialogue.lines:
        speaker = lesson.dialogue.lines[-1].speaker

    return ft.Column(
        spacing=12,
        controls=[
            _activity(
                ft.Icons.STYLE,
                "Flashcards",
                f"{len(lesson.vocabulary)} words · 3 mastered",
                lambda e: page.run_task(go, f"/vocab/{lesson.number}"),
            ),
            _activity(
                ft.Icons.MIC,
                "Speak the dialogue",
                f"Take the role of {speaker}",
                lambda e: page.run_task(go, "/practice"),
            ),
            _activity(
                ft.Icons.QUIZ,
                "Quick quiz",
                "10 questions · best 80%",
                None,
            ),
        ],
    )


# ── Tab 5 · Notes ───────────────────────────────────────────────


def _tab_notes(lesson: Lesson) -> ft.Control:
    return ft.Column(
        spacing=16,
        controls=[
            ft.Column(
                spacing=6,
                controls=[
                    ft.Text("Culture note", size=15,
                            weight=ft.FontWeight.W_600, color=theme.TEXT),
                    ft.Text(lesson.culture_note, size=14,
                            color=theme.TEXT_SECONDARY),
                ],
            ),
            ft.Divider(height=1, color=theme.DIVIDER),
            ft.Column(
                spacing=6,
                controls=[
                    ft.Text("Your notes", size=15,
                            weight=ft.FontWeight.W_600, color=theme.TEXT),
                    ft.Container(
                        border=ft.Border.all(1, theme.OUTLINE),
                        border_radius=14,
                        padding=ft.Padding.all(14),
                        height=96,
                        content=ft.Text("Tap to add a note…", size=14,
                                        color=theme.TEXT_MUTED),
                    ),
                ],
            ),
        ],
    )


# ── View ────────────────────────────────────────────────────────


def lesson_view(page: ft.Page, number: int) -> ft.View:
    lesson = get_lesson(number)

    def wrap(control: ft.Control) -> ft.Control:
        """Chak tab defile poukont li."""
        return ft.Container(
            padding=ft.Padding.only(left=20, right=20, top=18, bottom=24),
            content=ft.Column(
                scroll=ft.ScrollMode.AUTO,
                expand=True,
                controls=[control],
            ),
        )

    labels = ["Dialogue", "Vocab", "Syntax", "Activities", "Notes"]
    panels = [
        _tab_dialogue(page, lesson),
        _tab_vocab(page, lesson),
        ft.Column(
            spacing=20,
            controls=[grammar_table(p) for p in lesson.patterns],
        ),
        _tab_activities(page, lesson),
        _tab_notes(lesson),
    ]

    # Flet 0.85: Tabs se yon konteni; TabBar = tit yo, TabBarView = paj yo.
    tabs = ft.Tabs(
        length=len(labels),
        selected_index=0,
        expand=True,
        content=ft.Column(
            expand=True,
            spacing=0,
            controls=[
                ft.Container(
                    bgcolor=theme.SURFACE,
                    content=ft.TabBar(
                        indicator_color=theme.PRIMARY,
                        indicator_thickness=3,
                        label_color=theme.PRIMARY,
                        unselected_label_color=theme.TEXT_MUTED,
                        divider_color=theme.DIVIDER,
                        divider_height=1,
                        tabs=[ft.Tab(label=t) for t in labels],
                    ),
                ),
                ft.TabBarView(
                    expand=True,
                    controls=[wrap(p) for p in panels],
                ),
            ],
        ),
    )

    return ft.View(
        route=f"/lesson/{number}",
        padding=0,
        spacing=0,
        bgcolor=theme.BACKGROUND,
        controls=[
            ft.Container(
                bgcolor=theme.SURFACE,
                padding=ft.Padding.only(left=8, right=8, top=14),
                content=_app_bar(page, lesson),
            ),
            tabs,
        ],
    )
