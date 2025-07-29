from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from fluentogram import TranslatorRunner
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.statistics import FAQStatistics
from app.keyboards.faq import back_from_question, get_faq_keyboard
from app.utils.db.faq import get_faq_questions
from app.utils.db.statistics import update_statistics

router = Router(name="Router for admin work")


@router.message(Command("faq"))
@router.callback_query(F.data == "to_faq")
@router.callback_query(F.data == "faq_answer")
async def faq(update, i18n: TranslatorRunner, session: AsyncSession, state: FSMContext):
    data = await state.get_data()
    current_page = data.get("faq_page", 0)
    questions = await get_faq_questions(session)

    if isinstance(update, Message):
        await update.answer(
            i18n.faq(),
            parse_mode="Markdown",
            reply_markup=get_faq_keyboard(questions, current_page),
        )
    else:
        await update.message.edit_text(
            text=i18n.faq(),
            parse_mode="Markdown",
            reply_markup=get_faq_keyboard(questions, current_page),
        )
        await update.answer()


@router.callback_query(F.data.startswith("faq_next_page"))
async def faq_next_page(
    callback: CallbackQuery,
    i18n: TranslatorRunner,
    session: AsyncSession,
    state: FSMContext,
):
    data = await state.get_data()
    current_page = data.get("faq_page", 0)
    await state.update_data(faq_page=current_page + 1)
    await faq(callback, i18n, session, state)


@router.callback_query(F.data.startswith("faq_prev_page"))
async def faq_prev_page(
    callback: CallbackQuery,
    i18n: TranslatorRunner,
    session: AsyncSession,
    state: FSMContext,
):
    data = await state.get_data()
    current_page = data.get("faq_page", 0)
    await state.update_data(faq_page=max(0, current_page - 1))
    await faq(callback, i18n, session, state)


@router.callback_query(F.data.startswith("faq_question|"))
async def get_question(
    callback: CallbackQuery, i18n: TranslatorRunner, session: AsyncSession
):
    await update_statistics(session, FAQStatistics)
    question_id = callback.data[13:]
    questions = await get_faq_questions(session)
    asked_question = None
    for question in questions:
        if str(question.id) == question_id:
            asked_question = question
    await callback.message.edit_text(
        i18n.faq.question(
            question=asked_question.question, answer=asked_question.answer
        ),
        reply_markup=back_from_question,
        parse_mode="HTML",
    )
    await callback.answer()
