from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.config.config import get_settings


def get_faq_keyboard(questions, current_page):
    settings = get_settings()
    questions_per_page = settings.PAGE_SIZE
    total_pages = (len(questions) + questions_per_page - 1) // questions_per_page
    page_questions = questions[
        current_page * questions_per_page : (current_page + 1) * questions_per_page
    ]

    buttons = [
        [InlineKeyboardButton(text=q.question, callback_data=f"faq_answer_{q.id}")]
        for q in page_questions
    ]

    nav_buttons = []
    if current_page > 0:
        nav_buttons.append(
            InlineKeyboardButton(text="⬅️", callback_data="faq_prev_page")
        )
    if current_page < total_pages - 1:
        nav_buttons.append(
            InlineKeyboardButton(text="➡️", callback_data="faq_next_page")
        )

    if nav_buttons:
        buttons.append(nav_buttons)

    buttons.append([InlineKeyboardButton(text="Назад в меню", callback_data="start")])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


back_from_question = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data="faq_answer")],
    ]
)
