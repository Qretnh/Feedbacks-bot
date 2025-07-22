from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

welcome = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="📚 Частые вопросы", callback_data="to_faq")],
        [InlineKeyboardButton(text="💬 Оставить отзыв", callback_data="to_feedback")],
        [
            InlineKeyboardButton(
                text="👨‍💼 Связь с менеджером", callback_data="to_manager"
            )
        ],
        [InlineKeyboardButton(text="🛠 Возможности бота", callback_data="to_functions")],
    ],
    resize_keyboard=True,
)
back_to_start = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Вернуться назад", callback_data="start")]
    ]
)
