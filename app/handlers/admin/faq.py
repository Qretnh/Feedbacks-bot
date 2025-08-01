from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from fluentogram import TranslatorRunner
from sqlalchemy.ext.asyncio import AsyncSession

from app.keyboards.admin import admin_menu_faq_keyboard
from app.utils.db.faq import (
    add_question_to_faq,
    delete_question_from_faq,
    get_faq_questions,
)

router = Router(name="Router for admin work")


class AdminFAQ(StatesGroup):
    enter_question = State()
    enter_answer = State()


@router.callback_query(F.data == "admin|FAQ|")
async def admin_faq_menu(
    callback: CallbackQuery,
    session: AsyncSession,
    state: FSMContext,
    i18n: TranslatorRunner,
):
    questions = await get_faq_questions(session)
    data = await state.get_data()
    current_page = data.get("admin_faq_page", 0)

    await callback.message.edit_text(
        text=i18n.admin.choose.faq(),
        reply_markup=admin_menu_faq_keyboard(questions, current_page),
    )
    await callback.answer()


@router.callback_query(F.data == "admin_faq_next_page")
async def admin_faq_next_page(
    callback: CallbackQuery,
    i18n: TranslatorRunner,
    session: AsyncSession,
    state: FSMContext,
):
    data = await state.get_data()
    current_page = data.get("admin_faq_page", 0)
    await state.update_data(admin_faq_page=current_page + 1)
    await admin_faq_menu(callback, session, state, i18n)


@router.callback_query(F.data == "admin_faq_prev_page")
async def admin_faq_prev_page(
    callback: CallbackQuery,
    i18n: TranslatorRunner,
    session: AsyncSession,
    state: FSMContext,
):
    data = await state.get_data()
    current_page = data.get("admin_faq_page", 0)
    await state.update_data(admin_faq_page=max(0, current_page - 1))
    await admin_faq_menu(callback, session, state, i18n)


@router.callback_query(F.data == "admin|FAQ|new")
async def faq_add_question(
    callback: CallbackQuery,
    i18n: TranslatorRunner,
    session: AsyncSession,
    state: FSMContext,
):
    await callback.message.answer(text=i18n.admin.faq.add.question())
    await state.set_state(AdminFAQ.enter_question)
    await callback.answer()


@router.message(AdminFAQ.enter_question)
async def faq_add_answer(
    message: Message, i18n: TranslatorRunner, session: AsyncSession, state: FSMContext
):
    await state.update_data(new_question=message.text)
    await message.answer(text=i18n.admin.faq.add.answer(question=message.text))
    await state.set_state(AdminFAQ.enter_answer)


@router.message(AdminFAQ.enter_answer)
async def add_new_faq(
    message: Message, i18n: TranslatorRunner, session: AsyncSession, state: FSMContext
):
    data = await state.get_data()
    question = data["new_question"]
    answer = message.text
    await add_question_to_faq(session, question, answer)
    await state.clear()
    await message.answer(text=i18n.admin.faq.successfully.added())


@router.callback_query(F.data.startswith("admin|FAQ|d|"))
async def admin_delete_faq(
    callback: CallbackQuery,
    i18n: TranslatorRunner,
    session: AsyncSession,
    state: FSMContext,
):
    id = int(callback.data.split("|")[3])
    await delete_question_from_faq(session, id)
    await callback.answer(text=i18n.admin.faq.successfully.deleted())
