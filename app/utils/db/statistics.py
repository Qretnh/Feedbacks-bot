from datetime import datetime

from sqlalchemy import insert, select, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.statistics import (
    BroadcastStatistics,
    FAQStatistics,
    FeedbackStatistics,
)


async def update_statistics(session: AsyncSession, model) -> int:
    """
    Обновляет статистику для указанной модели
    :param session: AsyncSession
    :param model: Одна из моделей (FeedbackStatistics, FAQStatistics, BroadcastStatistics)
    :return: Текущее значение счетчика
    """
    current_month = datetime.utcnow().strftime("%Y-%m")

    try:
        # Пытаемся обновить существующую запись
        stmt = (
            update(model)
            .where(model.time == current_month)
            .values(counter=model.counter + 1)
            .returning(model.counter)
        )
        result = (await session.execute(stmt)).scalar_one()
        await session.commit()
        return result

    except NoResultFound:
        try:
            # Создаем новую запись, если не нашли
            stmt = (
                insert(model)
                .values(time=current_month, counter=1)
                .returning(model.counter)
            )
            result = (await session.execute(stmt)).scalar_one()
            await session.commit()
            return result
        except Exception:
            await session.rollback()
            raise

    except Exception:
        await session.rollback()
        raise


async def fetch_statistics_for_model(
    session: AsyncSession, model, time_period: str = None
) -> int:
    """
    Получает или инициализирует статистику для одной модели

    :param session: AsyncSession
    :param model: Модель статистики (FeedbackStatistics/FAQStatistics/BroadcastStatistics)
    :param time_period: Период в формате 'YYYY-MM' (если None - берется текущий месяц)
    :return: Текущее значение счетчика
    """
    current_time = time_period if time_period else datetime.utcnow().strftime("%Y-%m")

    try:
        # Пытаемся получить существующую запись
        stmt = select(model.counter).where(model.time == current_time)
        result = (await session.execute(stmt)).scalar_one_or_none()

        if result is not None:
            return result

        stmt = (
            insert(model).values(time=current_time, counter=0).returning(model.counter)
        )
        result = (await session.execute(stmt)).scalar_one()
        await session.commit()
        return result

    except Exception as e:
        await session.rollback()
        return 0
