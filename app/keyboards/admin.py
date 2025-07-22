from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

admin_menu_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="⚙️ Настройка F.A.Q.", callback_data="admin|FAQ|")],
        [
            InlineKeyboardButton(
                text="⚙️ Настройка Отзывы", callback_data="admin|topics|"
            )
        ],
        [InlineKeyboardButton(text="📨 Рассылка", callback_data="broadcast")],
    ]
)


def admin_menu_faq_keyboard(questions):
    keyboard = [
        [
            InlineKeyboardButton(
                text=f"❌ {item.question}", callback_data=f"admin|topic|d|{item.id}"
            )
        ]
        for item in questions
    ]
    keyboard.append(
        [
            InlineKeyboardButton(
                text="Добавить новый вопрос", callback_data="admin|FAQ|new"
            )
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def admin_menu_topic_keyboard(questions):
    keyboard = [
        [
            InlineKeyboardButton(
                text=f"❌ {item.text}", callback_data=f"admin|topic|d|{item.id}"
            )
        ]
        for item in questions
    ]
    keyboard.append(
        [
            InlineKeyboardButton(
                text="Добавить новую тему", callback_data="admin|topic|new"
            )
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
