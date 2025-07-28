from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.config.config import get_settings

admin_menu_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="⚙️ Настройка F.A.Q.", callback_data="admin|FAQ|")],
        [
            InlineKeyboardButton(
                text="⚙️ Настройка Отзывы", callback_data="admin|topics|"
            )
        ],
        [InlineKeyboardButton(text="📨 Рассылка", callback_data="broadcast")],
        [InlineKeyboardButton(text="📊 Статистика", callback_data="admin|statistics")],
    ]
)


def admin_menu_faq_keyboard(questions, current_page=0):
    settings = get_settings()
    questions_per_page = settings.PAGE_SIZE
    page_questions = questions[
        current_page * questions_per_page : (current_page + 1) * questions_per_page
    ]
    total_pages = (len(questions) + questions_per_page - 1) // questions_per_page

    keyboard = [
        [
            InlineKeyboardButton(
                text=f"❌ {q.question[:30]}{'...' if len(q.question) > 30 else ''}",
                callback_data=f"admin|FAQ|d|{q.id}",
            )
        ]
        for q in page_questions
    ]

    nav_buttons = []
    if current_page > 0:
        nav_buttons.append(
            InlineKeyboardButton(text="⬅️", callback_data="admin_faq_prev_page")
        )
    if current_page < total_pages - 1:
        nav_buttons.append(
            InlineKeyboardButton(text="➡️", callback_data="admin_faq_next_page")
        )

    if nav_buttons:
        keyboard.append(nav_buttons)

    keyboard.append(
        [InlineKeyboardButton(text="➕ Добавить вопрос", callback_data="admin|FAQ|new")]
    )
    keyboard.append(
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_admin")]
    )

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def admin_menu_topic_keyboard(topics, current_page=0):
    settings = get_settings()
    topics_per_page = settings.PAGE_SIZE
    page_topics = topics[
        current_page * topics_per_page : (current_page + 1) * topics_per_page
    ]
    total_pages = (len(topics) + topics_per_page - 1) // topics_per_page

    keyboard = [
        [
            InlineKeyboardButton(
                text=f"❌ {topic.text[:30]}{'...' if len(topic.text) > 30 else ''}",
                callback_data=f"admin|topic|d|{topic.id}",
            )
        ]
        for topic in page_topics
    ]

    nav_buttons = []
    if current_page > 0:
        nav_buttons.append(
            InlineKeyboardButton(text="⬅️", callback_data="admin_topics_prev_page")
        )
    if current_page < total_pages - 1:
        nav_buttons.append(
            InlineKeyboardButton(text="➡️", callback_data="admin_topics_next_page")
        )

    if nav_buttons:
        keyboard.append(nav_buttons)

    keyboard.append(
        [InlineKeyboardButton(text="➕ Добавить тему", callback_data="admin|topic|new")]
    )
    keyboard.append(
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_admin")]
    )

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


back_to_admin = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_admin")]
    ]
)
