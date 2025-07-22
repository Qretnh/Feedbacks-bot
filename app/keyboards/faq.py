from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_faq_keyboard(questions):
    items = [
        [
            InlineKeyboardButton(
                text=questions[i].question,
                callback_data="faq_question|" + str(questions[i].id),
            )
        ]
        for i in range(len(questions))
    ]
    items.append([InlineKeyboardButton(text="Назад в меню", callback_data="start")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=items)
    return keyboard


back_from_question = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data="faq_answer")],
    ]
)
