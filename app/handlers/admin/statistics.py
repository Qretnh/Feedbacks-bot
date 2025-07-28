from datetime import datetime

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from fluentogram import TranslatorRunner
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.statistics import (
    AppealsStatistics,
    BroadcastStatistics,
    FAQStatistics,
    FeedbackStatistics,
)
from app.keyboards.admin import (
    back_to_admin,
)
from app.utils.db.statistics import fetch_statistics_for_model

router = Router(name="router for statistics")


@router.callback_query(F.data == "admin|statistics")
async def admin_statistics(
    callback: CallbackQuery,
    session: AsyncSession,
    state: FSMContext,
    i18n: TranslatorRunner,
):
    current_month = datetime.now().strftime("%B %Y")

    faq_stat = await fetch_statistics_for_model(session, FAQStatistics)
    feedback_stat = await fetch_statistics_for_model(session, FeedbackStatistics)
    broadcast_stat = await fetch_statistics_for_model(session, BroadcastStatistics)
    appeals_stat = await fetch_statistics_for_model(session, AppealsStatistics)

    message = (
        f"📊 {'Статистика за ' + current_month}\n"
        f"{'─────────────────'}\n"
        f"❓ {'Открыто F.A.Q.:'} {faq_stat}\n"
        f"📩 {'Обработано отзывов:'} {feedback_stat}\n"
        f"📢 {'Отправлено рассылок:'} {broadcast_stat}\n"
        f"🗣 {'Обращений:'} {appeals_stat}\n"
        f"{'─────────────────'}\n"
        f"🔢 {'Всего:'} {faq_stat + feedback_stat + broadcast_stat + appeals_stat} действий"
    )

    try:
        await callback.message.edit_text(text=message, reply_markup=back_to_admin)
    except:
        await callback.message.answer(text=message, reply_markup=back_to_admin)

    await callback.answer()
