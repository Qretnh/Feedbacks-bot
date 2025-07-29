from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from fluentogram import TranslatorRunner
from sqlalchemy.ext.asyncio import AsyncSession

from app.keyboards.admin import admin_menu_topic_keyboard
from app.utils.db.topic import (
    add_topic_to_feedback,
    delete_topic_from_feedback,
    get_feedback_topics,
)

router = Router(name="Router for admin-feedback menu")


class AdminTopics(StatesGroup):
    add_topic = State()


@router.callback_query(F.data == "admin|topics|")
async def admin_feedback_menu(
    callback: CallbackQuery,
    session: AsyncSession,
    state: FSMContext,
    i18n: TranslatorRunner,
):
    topics = await get_feedback_topics(session)
    data = await state.get_data()
    current_page = data.get("admin_topics_page", 0)

    await callback.message.edit_text(
        text=i18n.admin.choose.topic(),
        reply_markup=admin_menu_topic_keyboard(topics, current_page),
    )
    await callback.answer()


@router.callback_query(F.data == "admin_topics_next_page")
async def admin_topics_next_page(
    callback: CallbackQuery,
    i18n: TranslatorRunner,
    session: AsyncSession,
    state: FSMContext,
):
    data = await state.get_data()
    current_page = data.get("admin_topics_page", 0)
    await state.update_data(admin_topics_page=current_page + 1)
    await admin_feedback_menu(callback, session, state, i18n)


@router.callback_query(F.data == "admin_topics_prev_page")
async def admin_topics_prev_page(
    callback: CallbackQuery,
    i18n: TranslatorRunner,
    session: AsyncSession,
    state: FSMContext,
):
    data = await state.get_data()
    current_page = data.get("admin_topics_page", 0)
    await state.update_data(admin_topics_page=current_page - 1)
    await admin_feedback_menu(callback, session, state, i18n)


@router.callback_query(F.data == "admin|topic|new")
async def feedback_admin_enter_topic(
    callback: CallbackQuery,
    i18n: TranslatorRunner,
    session: AsyncSession,
    state: FSMContext,
):
    await callback.message.answer(
        text="Добавление нового элемента в Отзывы\n\nВведите новую тему - так, как хотите, чтобы она выглядела у пользователя"
    )
    await state.set_state(AdminTopics.add_topic)
    await callback.answer()


@router.message(AdminTopics.add_topic)
async def feedback_add_new_topic(
    message: Message, i18n: TranslatorRunner, session: AsyncSession, state: FSMContext
):
    await add_topic_to_feedback(session=session, topic=message.text)
    await message.answer(text=i18n.admin.topic.added())
    await state.clear()


@router.callback_query(F.data.startswith("admin|topic|d|"))
async def admin_delete_topic(
    callback: CallbackQuery,
    i18n: TranslatorRunner,
    session: AsyncSession,
    state: FSMContext,
):
    id = int(callback.data.split("|")[3])
    await delete_topic_from_feedback(session, topic_id=id)
    await callback.answer(i18n.admin.topic.deleted())
