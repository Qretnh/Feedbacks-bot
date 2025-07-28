from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from fluentogram import TranslatorRunner
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.statistics import (
    BroadcastStatistics,
)
from app.db.models.user import User
from app.keyboards.other import confirm_broadcast_keyboard
from app.utils.db.statistics import update_statistics


class BroadcastStates(StatesGroup):
    waiting_for_text = State()
    waiting_for_photo = State()
    confirming = State()


router = Router(name="Router for broadcast")


@router.callback_query(F.data == "broadcast")
async def start_broadcast(
    callback: CallbackQuery, state: FSMContext, i18n: TranslatorRunner
):
    await state.set_state(BroadcastStates.waiting_for_text)
    await callback.message.answer(i18n.admin.broadcast.text())
    await callback.answer()


@router.message(BroadcastStates.waiting_for_text)
async def receive_broadcast_text(
    message: Message, state: FSMContext, i18n: TranslatorRunner
):
    await state.update_data(text=message.text)
    await state.set_state(BroadcastStates.waiting_for_photo)
    await message.answer(i18n.admin.broadcast.photo())


@router.message(BroadcastStates.waiting_for_photo, F.photo)
async def receive_broadcast_photo(message: Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    await state.update_data(photo=photo_id)
    data = await state.get_data()
    await message.answer("Предпросмотр:", reply_markup=confirm_broadcast_keyboard())
    await message.answer_photo(photo=photo_id, caption=data["text"])
    await state.set_state(BroadcastStates.confirming)


@router.message(BroadcastStates.waiting_for_photo)
async def skip_broadcast_photo(message: Message, state: FSMContext):
    await message.answer("Предпросмотр:", reply_markup=confirm_broadcast_keyboard())
    await message.answer((await state.get_data())["text"])
    await state.set_state(BroadcastStates.confirming)


@router.callback_query(F.data == "broadcast_cancel")
async def broadcast_cancel(
    callback: CallbackQuery, state: FSMContext, i18n: TranslatorRunner
):
    await state.clear()
    await callback.message.edit_text(i18n.admin.broadcast.cancel())
    await callback.answer()


@router.callback_query(F.data == "broadcast_confirm")
async def broadcast_send(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
    i18n: TranslatorRunner,
):
    data = await state.get_data()
    text = data.get("text")
    photo = data.get("photo")
    stmt = select(User.id)
    result = await session.execute(stmt)
    user_ids = result.scalars().all()

    sent_count = 0
    for user_id in user_ids:
        try:
            if photo:
                await callback.bot.send_photo(
                    chat_id=user_id, photo=photo, caption=text
                )
            else:
                await callback.bot.send_message(chat_id=user_id, text=text)
            sent_count += 1
        except Exception:
            continue

    await callback.message.edit_text(
        i18n.admin.broadcast.ended(sent_count=sent_count),
    )
    await update_statistics(session, BroadcastStatistics)
    await state.clear()
    await callback.answer()
