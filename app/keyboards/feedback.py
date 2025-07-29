from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.config.config import get_settings


def topic_keyboard(topics, current_page):
    settings = get_settings()
    topics_per_page = settings.PAGE_SIZE
    total_pages = (len(topics) + topics_per_page - 1) // topics_per_page

    page_topics = topics[
        current_page * topics_per_page : (current_page + 1) * topics_per_page
    ]

    buttons = [
        [
            InlineKeyboardButton(
                text=topic.text, callback_data=f"feedback_topic|{topic.id}"
            )
        ]
        for topic in page_topics
    ]

    nav_buttons = []
    if current_page > 0:
        nav_buttons.append(
            InlineKeyboardButton(text="⬅️", callback_data="feedback_prev_page")
        )
    if current_page < total_pages - 1:
        nav_buttons.append(
            InlineKeyboardButton(text="➡️", callback_data="feedback_next_page")
        )

    if nav_buttons:
        buttons.append(nav_buttons)

    buttons.append([InlineKeyboardButton(text="Назад в меню", callback_data="start")])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


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
