from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def topic_keyboard(topics):
    topic_buttons = [
        [
            InlineKeyboardButton(
                text=topic.text, callback_data=f"feedback_topic|{topic.id}"
            )
        ]
        for topic in topics
    ]
    back_button = [[InlineKeyboardButton(text="Назад в меню", callback_data="start")]]
    return InlineKeyboardMarkup(inline_keyboard=topic_buttons + back_button)


def stars_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⭐️", callback_data="feedback_stars|1")],
            [InlineKeyboardButton(text="⭐️⭐️", callback_data="feedback_stars|2")],
            [InlineKeyboardButton(text="⭐️⭐️⭐️", callback_data="feedback_stars|3")],
            [InlineKeyboardButton(text="⭐️⭐️⭐️⭐️", callback_data="feedback_stars|4")],
            [InlineKeyboardButton(text="⭐️⭐️⭐️⭐️⭐️", callback_data="feedback_stars|5")],
            [InlineKeyboardButton(text="❌ Отмена", callback_data="feedback_cancel")],
        ]
    )


def want_comment_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✍️ Да, добавить комментарий",
                    callback_data="feedback_comment|yes",
                )
            ],
            [
                InlineKeyboardButton(
                    text="🚫 Нет, отправить без комментария",
                    callback_data="feedback_comment|no",
                )
            ],
            [InlineKeyboardButton(text="❌ Отмена", callback_data="feedback_cancel")],
        ]
    )
