from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from fluentogram import TranslatorRunner
from sqlalchemy.ext.asyncio import AsyncSession

from app.keyboards.faq import back_from_question, get_faq_keyboard
from app.utils.db.faq import get_faq_questions

router = Router(name="Router for admin work")


@router.message(Command("faq"))
@router.callback_query(F.data == "to_faq")
@router.callback_query(F.data == "faq_answer")
async def faq(update, i18n: TranslatorRunner, session: AsyncSession):
    questions = await get_faq_questions(session)
    if type(update) == Message:
        await update.answer(
            i18n.faq(), parse_mode="Markdown", reply_markup=get_faq_keyboard(questions)
        )

    else:
        await update.message.edit_text(
            text=i18n.faq(),
            parse_mode="Markdown",
            reply_markup=get_faq_keyboard(questions),
        )
        await update.answer()


@router.callback_query(F.data.startswith("faq_question|"))
async def get_question(
    callback: CallbackQuery, i18n: TranslatorRunner, session: AsyncSession
):
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
