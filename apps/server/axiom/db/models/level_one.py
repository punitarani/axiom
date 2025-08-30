import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import (
    DDL,
    NUMERIC,
    TIMESTAMP,
    BigInteger,
    Boolean,
    CheckConstraint,
    ForeignKey,
    Index,
    Integer,
    String,
    event,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from axiom.db.client import Base
from axiom.db.models._partitions import ensure_partition_for_timestamp
from axiom.db.models.enums import InstrumentType, SecurityStatus


class LevelOne(Base):
    __tablename__ = "level_one_quotes"

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
    bid_price: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    bid_size: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    bid_mic_id: Mapped[Optional[str]] = mapped_column(String(4), nullable=True)
    ask_price: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    ask_size: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    ask_mic_id: Mapped[Optional[str]] = mapped_column(String(4), nullable=True)
    last_price: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    last_size: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    last_mic_id: Mapped[Optional[str]] = mapped_column(String(4), nullable=True)
    mark_price: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    spread: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    daily_high: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    daily_low: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    daily_open: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    prev_close: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    daily_volume: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    net_change: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    net_change_percent: Mapped[Optional[float]] = mapped_column(
        NUMERIC(8, 4), nullable=True
    )
    security_status: Mapped[Optional[SecurityStatus]] = mapped_column(
        String(20), nullable=True
    )
    quote_time: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    trade_time: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    is_realtime: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    security = relationship("Security", back_populates="level_one_quotes")

    __table_args__ = (
        CheckConstraint(
            "(ask_price IS NULL OR bid_price IS NULL OR ask_price >= bid_price)",
            name="ck_level_one_ask_gte_bid",
        ),
        CheckConstraint("bid_size >= 0", name="ck_level_one_bid_size_non_negative"),
        CheckConstraint("ask_size >= 0", name="ck_level_one_ask_size_non_negative"),
        CheckConstraint("last_size >= 0", name="ck_level_one_last_size_non_negative"),
        CheckConstraint(
            "daily_volume >= 0", name="ck_level_one_daily_volume_non_negative"
        ),
        Index(
            "ix_level_one_security_timestamp",
            "security_id",
            "timestamp",
        ),
        Index(
            "ix_level_one_timestamp_brin",
            "timestamp",
            postgresql_using="brin",
        ),
        {"postgresql_partition_by": "RANGE (timestamp)"},
    )


# Create DEFAULT partition at table create time (idempotent)
event.listen(
    LevelOne.__table__,
    "after_create",
    DDL(
        'CREATE TABLE IF NOT EXISTS "level_one_quotes_default" '
        'PARTITION OF "level_one_quotes" DEFAULT'
    ),
)


# Create daily partition right before insert (idempotent)
@event.listens_for(LevelOne, "before_insert")
def level_one_before_insert(mapper, connection, target):  # type: ignore[no-redef]
    ts = getattr(target, "timestamp", None) or datetime.now(timezone.utc)
    ensure_partition_for_timestamp(connection, "level_one_quotes", ts)
