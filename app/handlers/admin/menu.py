from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from fluentogram import TranslatorRunner

from app.config.config import get_settings
from app.keyboards.admin import (
    admin_menu_keyboard,
)

router = Router(name="Router for admin")


@router.callback_query(F.data == "back_to_admin")
@router.message(Command("admin"))
async def admin_callback(update, i18n: TranslatorRunner, state: FSMContext):
    settings = get_settings()
    admin_ids = [
        int(id_str.strip())
        for id_str in settings.ADMIN_IDS.split(",")
        if id_str.strip()
    ]
    if type(update) == Message:
        if update.from_user.id not in admin_ids:
            await update.answer(i18n.admin.permissions.error())
            return
        await update.answer(i18n.admin.menu(), reply_markup=admin_menu_keyboard)
    else:
        if update.from_user.id not in admin_ids:
            await update.message.answer(i18n.admin.permissions.error())
            return
        await update.message.answer(i18n.admin.menu(), reply_markup=admin_menu_keyboard)
        await update.answer()
        await state.clear()
