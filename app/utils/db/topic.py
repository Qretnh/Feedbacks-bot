from sqlalchemy import delete, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.feedback_topic import Topic


async def get_feedback_topics(session: AsyncSession):
    stmt = select(Topic)
    res = await session.execute(stmt)
    return res.scalars().all()


async def add_topic_to_feedback(session: AsyncSession, topic: str):
    stmt = insert(Topic).values(text=topic).on_conflict_do_nothing()
    await session.execute(stmt)
    await session.commit()


async def delete_topic_from_feedback(session: AsyncSession, topic_id: int):
    stmt = delete(Topic).where(Topic.id == topic_id)
    await session.execute(stmt)
    await session.commit()
