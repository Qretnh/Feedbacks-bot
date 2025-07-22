from sqlalchemy import delete, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.FAQ import FAQ


async def get_faq_questions(session: AsyncSession):
    stmt = select(FAQ)
    res = await session.execute(stmt)
    return res.scalars().all()


async def add_question_to_faq(session: AsyncSession, question: str, answer: str):
    stmt = insert(FAQ).values(question=question, answer=answer).on_conflict_do_nothing()
    await session.execute(stmt)
    await session.commit()


async def delete_question_from_faq(session: AsyncSession, question_id: int):
    stmt = delete(FAQ).where(FAQ.id == int(question_id))
    await session.execute(stmt)
    await session.commit()
