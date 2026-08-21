# Copyright (c) 2026 Wilkend. All rights reserved.
# Hantalk - proprietary software. See LICENSE at the repository root.
# Unauthorized copying, modification, or redistribution is prohibited.

import asyncio

import flet as ft

from app import theme
from data.lessons.all_lessons import get_lesson
from models.session import Session

REVEAL_DELAY = 0.55
"""How many seconds a correct answer stays shown before the next question."""


def _progress_bar(fill: ft.Container) -> ft.Control:
    """The progress bar — a Stack with a fill that grows.

    WHY `scale_x` AND NOT `width`

      To animate a width in pixels, we'd need to know the screen width —
      which isn't available when we build the View. A `Scale` anchored to
      the left works with any width, without us measuring anything.
    """
    return ft.Stack(
        height=10,
        controls=[
            ft.Container(
                left=0, right=0, top=0, bottom=0,
                bgcolor=theme.TRACK,
                border_radius=999,
            ),
            fill,
        ],
    )


def exercise_view(page: ft.Page, lesson_number: int) -> ft.View:
    lesson = get_lesson(lesson_number)

    state = {
        "session": Session.for_lesson(lesson),
        "locked": False,   # block taps while the feedback is showing
        "done": False,
    }

    # ── Controls that live for the whole session ─────────────────

    progress_fill = ft.Container(
        left=0, right=0, top=0, bottom=0,
        gradient=theme.grad_energy(),
        border_radius=999,
        scale=ft.Scale(scale_x=0.0, alignment=ft.Alignment.CENTER_LEFT),
        animate_scale=ft.Animation(duration=320,
                                   curve=ft.AnimationCurve.EASE_OUT),
    )

    counter = ft.Text("", size=theme.SIZE_SMALL, color=theme.TEXT_MUTED)

    instruction = ft.Text(
        "", size=theme.SIZE_LABEL, weight=ft.FontWeight.W_700,
        color=theme.TEXT_MUTED,
    )
    prompt = ft.Text(
        "", size=theme.SIZE_ZH, weight=ft.FontWeight.W_500,
        color=theme.TEXT, text_align=ft.TextAlign.CENTER,
    )
    hint = ft.Text(
        "", size=theme.SIZE_BODY, color=theme.TEXT_MUTED,
        text_align=ft.TextAlign.CENTER, visible=False,
    )

    def _make_option(i: int):
        label = ft.Text(
            "", size=theme.SIZE_H3, color=theme.TEXT,
            text_align=ft.TextAlign.CENTER, weight=ft.FontWeight.W_500,
        )
        box = ft.Container(
            content=label,
            alignment=ft.Alignment.CENTER,
            bgcolor=theme.SURFACE,
            border=ft.Border.all(2, theme.OUTLINE),
            border_radius=theme.RADIUS_MD,
            padding=ft.Padding.symmetric(vertical=16, horizontal=14),
            animate=ft.Animation(duration=140,
                                 curve=ft.AnimationCurve.EASE_OUT),
            animate_scale=ft.Animation(duration=110,
                                       curve=ft.AnimationCurve.EASE_OUT),
            scale=1.0,
            on_click=None,          # wired up below
        )
        return box, label

    options = [_make_option(i) for i in range(4)]

    answer_text = ft.Text(
        "", size=theme.SIZE_H2, weight=ft.FontWeight.W_700,
        color=theme.SUCCESS_TEXT,
    )

    question = ft.Column(
        expand=True,
        spacing=0,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Container(height=8),
            instruction,
            ft.Container(height=22),
            prompt,
            ft.Container(height=10),
            hint,
            ft.Container(expand=True),
            ft.Column(spacing=10, controls=[box for box, _ in options]),
            ft.Container(height=8),
        ],
    )

    body = ft.Container(
        expand=True,
        padding=ft.Padding.symmetric(horizontal=theme.PAD_PAGE, vertical=10),
        content=question,
    )

    # ── The feedback sheet (only when you're wrong) ───────────

    def on_continue(e):
        advance()
        page.update()

    feedback = ft.Container(
        left=0, right=0, bottom=0,
        offset=ft.Offset(0, 1),          # hidden below the screen
        animate_offset=ft.Animation(duration=240,
                                    curve=ft.AnimationCurve.EASE_OUT),
        bgcolor=theme.SURFACE,
        border=ft.Border.only(top=ft.BorderSide(1, theme.OUTLINE)),
        padding=ft.Padding.only(left=20, right=20, top=16, bottom=24),
        content=ft.Column(
            tight=True,
            spacing=12,
            controls=[
                ft.Row(
                    spacing=8,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Icon(ft.Icons.CLOSE, size=20, color=theme.ERROR),
                        ft.Text("The correct answer is:", size=theme.SIZE_BODY,
                                color=theme.TEXT_SECONDARY),
                    ],
                ),
                answer_text,
                ft.Container(
                    bgcolor=theme.PRIMARY,
                    border_radius=theme.RADIUS_SM,
                    padding=ft.Padding.symmetric(vertical=14),
                    alignment=ft.Alignment.CENTER,
                    on_click=on_continue,
                    content=ft.Text("Continue", size=theme.SIZE_H3,
                                    weight=ft.FontWeight.W_700,
                                    color=theme.WHITE),
                ),
            ],
        ),
    )

    # ── Paint (draw) a question ────────────────────────────────────

    def paint_question() -> None:
        session = state["session"]
        exercise = session.current
        if exercise is None:
            return
        meta = exercise.meta

        instruction.value = meta.instruction
        prompt.value = exercise.prompt
        prompt.size = meta.prompt_size
        prompt.font_family = (theme.FONT_ZH_SERIF if meta.prompt_zh
                              else theme.FONT_UI)

        hint.value = exercise.hint
        hint.visible = bool(exercise.hint)

        counter.value = session.position
        progress_fill.scale = ft.Scale(
            scale_x=session.progress, alignment=ft.Alignment.CENTER_LEFT
        )

        for i, (box, label) in enumerate(options):
            if i < len(exercise.options):
                box.visible = True
                box.bgcolor = theme.SURFACE
                box.border = ft.Border.all(2, theme.OUTLINE)
                box.scale = 1.0
                label.value = exercise.options[i]
                label.color = theme.TEXT
                label.font_family = (theme.FONT_ZH if meta.options_zh
                                     else theme.FONT_UI)
                label.size = 22 if meta.options_zh else theme.SIZE_H3
            else:
                box.visible = False

    # ── End of session ────────────────────────────────────────

    def show_summary() -> None:
        """The loop needs an END — that's where the reward lands."""
        session = state["session"]
        state["done"] = True
        counter.value = ""
        progress_fill.scale = ft.Scale(
            scale_x=1.0, alignment=ft.Alignment.CENTER_LEFT
        )

        async def restart(e):
            state["session"] = Session.for_lesson(lesson)
            state["done"] = False
            state["locked"] = False
            body.content = question
            paint_question()
            page.update()

        async def back(e):
            await page.push_route(f"/unit/{lesson_number}")

        def _button(label: str, bg: str, fg: str, handler) -> ft.Control:
            return ft.Container(
                bgcolor=bg,
                border_radius=theme.RADIUS_SM,
                padding=ft.Padding.symmetric(vertical=14, horizontal=20),
                alignment=ft.Alignment.CENTER,
                on_click=handler,
                content=ft.Text(label, size=theme.SIZE_H3,
                                weight=ft.FontWeight.W_700, color=fg),
            )

        body.content = ft.Column(
            expand=True,
            spacing=0,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Icon(ft.Icons.CHECK_CIRCLE, size=84, color=theme.SUCCESS),
                ft.Container(height=16),
                ft.Text("Session complete!", size=theme.SIZE_TITLE,
                        weight=ft.FontWeight.W_700, color=theme.TEXT),
                ft.Container(height=6),
                ft.Text(f"{session.planned} exercises · {session.accuracy}% correct",
                        size=theme.SIZE_BODY, color=theme.TEXT_SECONDARY),
                ft.Text(
                    "No mistakes at all" if not session.mistakes
                    else f"{session.mistakes} mistakes — every one came back",
                    size=theme.SIZE_SMALL, color=theme.TEXT_MUTED,
                ),
                ft.Container(height=28),
                _button("Start again", theme.PRIMARY, theme.WHITE, restart),
                ft.Container(height=10),
                _button("Back to the unit", theme.SURFACE_VARIANT,
                        theme.TEXT, back),
            ],
        )

    # ── Advance ───────────────────────────────────────────────

    def advance() -> None:
        feedback.offset = ft.Offset(0, 1)
        state["locked"] = False
        if state["session"].is_done:
            show_summary()
        else:
            paint_question()

    # ── Answer ───────────────────────────────────────────────

    def make_pick(i: int):
        async def handler(e):
            if state["locked"] or state["done"]:
                return
            session = state["session"]
            exercise = session.current
            if exercise is None or i >= len(exercise.options):
                return

            state["locked"] = True
            box, label = options[i]
            correct = session.answer(exercise.options[i])

            if correct:
                box.bgcolor = theme.SUCCESS
                box.border = ft.Border.all(2, theme.SUCCESS)
                box.scale = 1.03
                label.color = theme.WHITE
                page.update()

                # A single wait, not a loop — this has nothing to do
                # with a Python-driven animation.
                await asyncio.sleep(REVEAL_DELAY)
                advance()
                page.update()
            else:
                box.bgcolor = theme.ERROR
                box.border = ft.Border.all(2, theme.ERROR)
                label.color = theme.WHITE

                # Show the correct answer right away — never leave the
                # user searching for it.
                for j, (other_box, _) in enumerate(options):
                    if (j < len(exercise.options)
                            and exercise.options[j] == exercise.answer):
                        other_box.border = ft.Border.all(2, theme.SUCCESS)

                answer_text.value = exercise.answer
                answer_text.font_family = (theme.FONT_ZH
                                           if exercise.meta.options_zh
                                           else theme.FONT_UI)
                feedback.offset = ft.Offset(0, 0)
                page.update()

        return handler

    for i, (box, _) in enumerate(options):
        box.on_click = make_pick(i)

    # ── The screen ─────────────────────────────────────────────

    async def quit_session(e):
        await page.push_route(f"/unit/{lesson_number}")

    header = ft.Container(
        bgcolor=theme.SURFACE,
        padding=ft.Padding.only(left=8, right=20, top=14, bottom=14),
        content=ft.Row(
            spacing=12,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    padding=ft.Padding.all(8),
                    border_radius=999,
                    on_click=quit_session,
                    content=ft.Icon(ft.Icons.CLOSE, size=24, color=theme.TEXT),
                ),
                ft.Container(expand=True, content=_progress_bar(progress_fill)),
                counter,
            ],
        ),
    )

    if state["session"].is_empty:
        body.content = ft.Column(
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
            controls=[
                ft.Icon(ft.Icons.EDIT_NOTE, size=64, color=theme.TEXT_MUTED),
                ft.Text("This lesson does not have enough content yet",
                        size=theme.SIZE_H2, weight=ft.FontWeight.W_600,
                        color=theme.TEXT),
                ft.Text("Write the vocabulary and the exercises appear on their own.",
                        size=theme.SIZE_BODY, color=theme.TEXT_MUTED,
                        text_align=ft.TextAlign.CENTER),
            ],
        )
    else:
        paint_question()

    return ft.View(
        route=f"/exercise/{lesson_number}",
        padding=0,
        spacing=0,
        bgcolor=theme.BACKGROUND,
        controls=[
            ft.Stack(
                expand=True,
                controls=[
                    ft.Container(
                        left=0, top=0, right=0, bottom=0,
                        content=ft.Column(
                            expand=True, spacing=0,
                            controls=[header, body],
                        ),
                    ),
                    feedback,
                ],
            )
        ],
    )
