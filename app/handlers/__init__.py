from aiogram import Dispatcher

from app.handlers.admin.faq import router as admin_faq_router
from app.handlers.admin.functions import router as admin_functions_router
from app.handlers.admin.topics import router as admin_topics_router
from app.handlers.faq.questions import router as faq_questions_router
from app.handlers.feedback.feedbacks_and_manager import (
    router as feedbacks_and_manager_router,
)
from app.handlers.functions import router as functions_router
from app.handlers.menu.base import router as menu_router


def include_all_routers(dp: Dispatcher):
    dp.include_routers(
        menu_router,
        admin_faq_router,
        faq_questions_router,
        feedbacks_and_manager_router,
        functions_router,
        admin_functions_router,
        admin_topics_router,
    )
