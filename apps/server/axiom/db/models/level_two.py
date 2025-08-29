import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import (
    TIMESTAMP,
    BigInteger,
    CheckConstraint,
    ForeignKey,
    Index,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from axiom.db.client import Base
from axiom.db.models.enums import InstrumentType, OrderSide


class LevelTwo(Base):
    __tablename__ = "level_two_quotes"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    security_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("securities.id", ondelete="CASCADE"),
        nullable=False,
    )
    timestamp: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, primary_key=True
    )
    instrument_type: Mapped[InstrumentType] = mapped_column(
        String(10), nullable=False, default=InstrumentType.EQUITY
    )
    side: Mapped[OrderSide] = mapped_column(String(3), nullable=False)
    price_level: Mapped[int] = mapped_column(BigInteger, nullable=False)
    size: Mapped[int] = mapped_column(BigInteger, nullable=False)
    order_count: Mapped[int] = mapped_column(Integer, nullable=False)
    level_index: Mapped[int] = mapped_column(Integer, nullable=False)
    market_maker_id: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    mic_id: Mapped[Optional[str]] = mapped_column(String(4), nullable=True)
    quote_time: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    security = relationship("Security", back_populates="level_two_quotes")

    __table_args__ = (
        UniqueConstraint(
            "security_id",
            "timestamp",
            "side",
            "price_level",
            name="uq_level_two_security_timestamp_side_price",
        ),
        CheckConstraint("price_level > 0", name="ck_level_two_price_level_positive"),
        CheckConstraint("size > 0", name="ck_level_two_size_positive"),
        CheckConstraint("order_count > 0", name="ck_level_two_order_count_positive"),
        CheckConstraint(
            "level_index >= 0", name="ck_level_two_level_index_non_negative"
        ),
        Index(
            "ix_level_two_security_timestamp",
            "security_id",
            "timestamp",
        ),
        Index(
            "ix_level_two_timestamp_brin",
            "timestamp",
            postgresql_using="brin",
        ),
        {"postgresql_partition_by": "RANGE (timestamp)"},
    )
