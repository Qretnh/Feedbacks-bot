from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def confirm_broadcast_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Отправить", callback_data="broadcast_confirm"
                )
            ],
            [InlineKeyboardButton(text="❌ Отмена", callback_data="broadcast_cancel")],
        ]
    )
