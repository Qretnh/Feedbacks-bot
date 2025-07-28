from aiogram import Dispatcher

from app.handlers.admin.broadcast import router as admin_broadcast_router
from app.handlers.admin.faq import router as admin_faq_router
from app.handlers.admin.menu import router as admin_menu_router
from app.handlers.admin.statistics import router as admin_statistics_router
from app.handlers.admin.topics import router as admin_topics_router
from app.handlers.faq.questions import router as faq_questions_router
from app.handlers.feedback.feedback import router as feedbacks_and_manager_router
from app.handlers.functions import router as functions_router
from app.handlers.manager.manager import router as manager_router
from app.handlers.menu.base import router as menu_router


def include_all_routers(dp: Dispatcher):
    dp.include_routers(
        menu_router,
        admin_faq_router,
        faq_questions_router,
        feedbacks_and_manager_router,
        functions_router,
        admin_menu_router,
        admin_topics_router,
        manager_router,
        admin_statistics_router,
        admin_broadcast_router,
    )
