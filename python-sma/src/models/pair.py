from datetime import datetime

from sqlalchemy import FLOAT, INTEGER, TIMESTAMP, VARCHAR, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base


class Pair(Base):
    """
    Model for the 'pair' table in the database.
    """

    __tablename__ = "pair"
    __schema__ = "public"

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, unique=True)
    pair: Mapped[str] = mapped_column(VARCHAR(10))
    timestamp: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    mms_20: Mapped[float] = mapped_column(FLOAT, nullable=True)
    mms_50: Mapped[float] = mapped_column(FLOAT, nullable=True)
    mms_200: Mapped[float] = mapped_column(FLOAT, nullable=True)

    __table_args__ = (UniqueConstraint("pair", "timestamp", name="unique_pair_timestamp"),)
