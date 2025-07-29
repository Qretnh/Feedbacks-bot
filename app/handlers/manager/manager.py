from aiogram import F, Router
from aiogram.types import CallbackQuery
from fluentogram import TranslatorRunner
from sqlalchemy.ext.asyncio import AsyncSession

import app.keyboards.menu as menu_keyboards
from app.config.config import get_settings
from app.db.models.statistics import AppealsStatistics
from app.utils.db.statistics import update_statistics

router = Router(name="Router for manager communication")


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
    await update_statistics(session, AppealsStatistics)
    await callback.answer()
