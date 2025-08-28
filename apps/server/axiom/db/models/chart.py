import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import (
    TIMESTAMP,
    BigInteger,
    Boolean,
    CheckConstraint,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from axiom.db.client import Base
from axiom.db.models.enums import InstrumentType, Timeframe


class Chart(Base):
    __tablename__ = "charts"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    security_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("securities.id", ondelete="CASCADE"),
        nullable=False,
    )
    timestamp: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False
    )
    timeframe: Mapped[Timeframe] = mapped_column(String(10), nullable=False)
    instrument_type: Mapped[InstrumentType] = mapped_column(
        String(10), nullable=False, default=InstrumentType.EQUITY
    )
    open_price: Mapped[int] = mapped_column(BigInteger, nullable=False)
    high_price: Mapped[int] = mapped_column(BigInteger, nullable=False)
    low_price: Mapped[int] = mapped_column(BigInteger, nullable=False)
    close_price: Mapped[int] = mapped_column(BigInteger, nullable=False)
    volume: Mapped[int] = mapped_column(BigInteger, nullable=False)
    trade_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    vwap: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    is_regular_hours: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    security = relationship("Security", back_populates="charts")

    __table_args__ = (
        UniqueConstraint(
            "security_id",
            "timestamp",
            "timeframe",
            name="uq_chart_security_timestamp_timeframe",
        ),
        CheckConstraint("open_price > 0", name="ck_chart_open_price_positive"),
        CheckConstraint("high_price > 0", name="ck_chart_high_price_positive"),
        CheckConstraint("low_price > 0", name="ck_chart_low_price_positive"),
        CheckConstraint("close_price > 0", name="ck_chart_close_price_positive"),
        CheckConstraint(
            "high_price >= low_price", name="ck_chart_high_greater_than_low"
        ),
        CheckConstraint("volume >= 0", name="ck_chart_volume_non_negative"),
        {"postgresql_partition_by": "RANGE (timestamp)"},
    )
