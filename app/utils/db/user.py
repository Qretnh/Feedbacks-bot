from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User


async def add_user(session: AsyncSession, id: int, username: str):
    stmt = insert(User).values(id=id, username=username)
    stmt = stmt.on_conflict_do_nothing(index_elements=["id"])
    await session.execute(stmt)
    await session.commit()
