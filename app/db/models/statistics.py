from sqlalchemy import BigInteger, Column, DateTime, String

from app.db.base import Base


class FeedbackStatistics(Base):
    __tablename__ = "feedback_statistics"

    time = Column(String, primary_key=True)
    counter = Column(BigInteger, default=0)


class FAQStatistics(Base):
    __tablename__ = "FAQ_statistics"

    time = Column(String, primary_key=True)
    counter = Column(BigInteger, default=0)


class BroadcastStatistics(Base):
    __tablename__ = "broadcast_statistics"

    time = Column(String, primary_key=True)
    counter = Column(BigInteger, default=0)


class AppealsStatistics(Base):
    __tablename__ = "appeals_statistics"

    time = Column(String, primary_key=True)
    counter = Column(BigInteger, default=0)
