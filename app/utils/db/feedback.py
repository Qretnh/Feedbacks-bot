from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.feedback import Feedback


async def add_feedback(
    session: AsyncSession, user_id: int, stars: int, text: str | None
):
    feedback = Feedback(user_id=user_id, stars=stars, text=text)
    session.add(feedback)
    await session.commit()
