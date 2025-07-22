from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message
from fluentogram import TranslatorRunner
from sqlalchemy.ext.asyncio import AsyncSession

import app.keyboards.menu as menu_keyboards
from app.utils.db.user import add_user

router = Router(name="Router for / commands")


@router.callback_query(F.data == "start")
@router.message(Command("start"))
async def start(update, i18n: TranslatorRunner, session: AsyncSession):

    if type(update) == Message:
        await add_user(session, update.from_user.id, update.from_user.username)
        await update.reply(i18n.welcome(), reply_markup=menu_keyboards.welcome)
    else:
        await add_user(
            session, update.message.from_user.id, update.message.from_user.username
        )
        await update.message.edit_text(
            i18n.welcome(), reply_markup=menu_keyboards.welcome
        )
        await update.answer()
