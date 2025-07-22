from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from fluentogram import TranslatorRunner
from sqlalchemy.ext.asyncio import AsyncSession

import app.keyboards.menu as menu_keyboards
from app.config.config import get_settings
from app.keyboards.feedback import stars_keyboard, topic_keyboard, want_comment_keyboard
from app.utils.db.feedback import add_feedback
from app.utils.db.topic import get_feedback_topics

router = Router(name="Router for feedbacks and manager communication")


class FeedbackStates(StatesGroup):
    choosing_topic = State()
    choosing_stars = State()
    choosing_comment = State()
    writing_comment = State()


async def send_feedback_result(update, data: dict, i18n: TranslatorRunner):
    topic = data.get("topic")
    stars = data.get("stars")
    comment = data.get("comment", "Комментарий не добавлен.")

    text = i18n.feedback.answer(topic=topic, stars=stars, comment=comment)
    if type(update) == CallbackQuery:
        await update.message.answer(text, parse_mode="Markdown")

    if stars <= 3:
        if type(update) == CallbackQuery:
            await update.message.answer(i18n.feedback.bad())
        else:
            await update.answer(i18n.feedback.bad())
    else:
        if type(update) == CallbackQuery:
            await update.message.answer(i18n.feedback.good())
        else:
            await update.answer(i18n.feedback.good())


@router.callback_query(F.data.startswith("to_manager"))
async def get_question(
    callback: CallbackQuery, i18n: TranslatorRunner, session: AsyncSession
):
    await callback.message.answer(i18n.manager())
    settings = get_settings()
    SUPPORT_CHAT_ID = settings.SUPPORT_CHAT_ID
    await callback.bot.send_message(
        SUPPORT_CHAT_ID, i18n.service(user=callback.from_user.username)
    )
    await callback.answer()
    await callback.message.edit_text(
        i18n.welcome(), reply_markup=menu_keyboards.welcome
    )


@router.callback_query(F.data.startswith("to_feedback"))
async def menu_feedback(
    callback: CallbackQuery,
    i18n: TranslatorRunner,
    state: FSMContext,
    session: AsyncSession,
):
    await state.set_state(FeedbackStates.choosing_topic)
    topics = await get_feedback_topics(session=session)
    await callback.message.edit_text(
        i18n.feedback.choose(), reply_markup=topic_keyboard(topics)
    )
    await callback.answer()


@router.callback_query(F.data == "feedback_cancel")
async def cancel_feedback(
    callback: CallbackQuery, i18n: TranslatorRunner, state: FSMContext
):
    await state.clear()
    await callback.message.edit_text(i18n.feedback.cancel())
    await callback.answer()


@router.callback_query(F.data.startswith("feedback_topic|"))
async def choose_topic(
    callback: CallbackQuery, i18n: TranslatorRunner, state: FSMContext
):
    topic = callback.data.split("|")[1]
    await state.update_data(topic=topic)
    await state.set_state(FeedbackStates.choosing_stars)
    await callback.message.edit_text(
        i18n.feedback.select(), reply_markup=stars_keyboard(), parse_mode="Markdown"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("feedback_stars|"))
async def choose_stars(
    callback: CallbackQuery, i18n: TranslatorRunner, state: FSMContext
):
    stars = int(callback.data.split("|")[1])
    await state.update_data(stars=stars)
    await state.set_state(FeedbackStates.choosing_comment)
    await callback.message.edit_text(
        i18n.feedback.comment(),
        reply_markup=want_comment_keyboard(),
        parse_mode="Markdown",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("feedback_comment|"))
async def want_comment(
    callback: CallbackQuery,
    i18n: TranslatorRunner,
    state: FSMContext,
    session: AsyncSession,
):
    choice = callback.data.split("|")[1]
    data = await state.get_data()
    user_id = callback.from_user.id
    stars = data.get("stars")
    comment = None
    settings = get_settings()
    FEEDBACK_CHAT_ID = settings.FEEDBACK_CHAT_ID

    if choice == "yes":
        await state.set_state(FeedbackStates.writing_comment)
        await callback.message.edit_text(
            i18n.feedback.write.comment(), parse_mode="Markdown"
        )
    else:
        await add_feedback(session=session, user_id=user_id, stars=stars, text=comment)

        try:
            await send_feedback_result(callback, data, i18n)
            await callback.bot.send_message(
                FEEDBACK_CHAT_ID,
                i18n.admin.new.feedback(
                    user_id=user_id, stars=stars, text=comment or "Без комментария."
                ),
            )
        except Exception as e:
            pass

        await state.clear()
        await callback.message.reply(
            i18n.get("welcome"), reply_markup=menu_keyboards.welcome
        )
    await callback.answer()


@router.message(FeedbackStates.writing_comment)
async def receive_comment(
    message: Message, state: FSMContext, i18n: TranslatorRunner, session: AsyncSession
):
    await state.update_data(comment=message.text)
    data = await state.get_data()
    settings = get_settings()
    FEEDBACK_CHAT_ID = settings.FEEDBACK_CHAT_ID

    user_id = message.from_user.id
    stars = data.get("stars")
    comment = data.get("comment")

    await add_feedback(session=session, user_id=user_id, stars=stars, text=comment)

    try:
        await send_feedback_result(message, data, i18n)
        await message.bot.send_message(
            FEEDBACK_CHAT_ID,
            i18n.admin.new.feedback(
                user_id=user_id, stars=stars, text=comment or "Без комментария."
            ),
        )
    except Exception as e:
        pass

    await state.clear()
    await message.reply(i18n.get("welcome"), reply_markup=menu_keyboards.welcome)
