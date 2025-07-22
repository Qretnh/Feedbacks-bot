from aiogram import F, Router
from aiogram.types import CallbackQuery
from fluentogram import TranslatorRunner
from sqlalchemy.ext.asyncio import AsyncSession

from app.keyboards.menu import back_to_start

router = Router(name="Router for admin work")


@router.callback_query(F.data == "to_functions")
async def get_question(
    callback: CallbackQuery, i18n: TranslatorRunner, session: AsyncSession
):

    await callback.message.edit_text(i18n.functions(), reply_markup=back_to_start)
    await callback.answer()
