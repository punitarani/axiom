import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import (
    NUMERIC,
    TIMESTAMP,
    BigInteger,
    Boolean,
    CheckConstraint,
    ForeignKey,
    Index,
    Integer,
    String,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from axiom.db.client import Base
from axiom.db.models.enums import SecurityStatus


class OptionQuote(Base):
    __tablename__ = "option_quotes"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    option_contract_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("option_contracts.id", ondelete="CASCADE"),
        nullable=False,
    )
    timestamp: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, primary_key=True
    )
    bid_price: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    bid_size: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    ask_price: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    ask_size: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    last_price: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    last_size: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    mark_price: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    daily_high: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    daily_low: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    daily_open: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    prev_close: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    daily_volume: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    open_interest: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    net_change: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    net_change_percent: Mapped[Optional[float]] = mapped_column(
        NUMERIC(8, 4), nullable=True
    )
    implied_volatility: Mapped[Optional[float]] = mapped_column(
        NUMERIC(8, 4), nullable=True
    )
    delta: Mapped[Optional[float]] = mapped_column(NUMERIC(8, 6), nullable=True)
    gamma: Mapped[Optional[float]] = mapped_column(NUMERIC(8, 6), nullable=True)
    theta: Mapped[Optional[float]] = mapped_column(NUMERIC(8, 6), nullable=True)
    vega: Mapped[Optional[float]] = mapped_column(NUMERIC(8, 6), nullable=True)
    rho: Mapped[Optional[float]] = mapped_column(NUMERIC(8, 6), nullable=True)
    theoretical_value: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    intrinsic_value: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    time_value: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    underlying_price: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    is_in_the_money: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
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

    option_contract = relationship("OptionContract", back_populates="option_quotes")

    __table_args__ = (
        CheckConstraint(
            "(ask_price IS NULL OR bid_price IS NULL OR ask_price >= bid_price)",
            name="ck_option_quote_ask_gte_bid",
        ),
        CheckConstraint("bid_size >= 0", name="ck_option_quote_bid_size_non_negative"),
        CheckConstraint("ask_size >= 0", name="ck_option_quote_ask_size_non_negative"),
        CheckConstraint(
            "last_size >= 0", name="ck_option_quote_last_size_non_negative"
        ),
        CheckConstraint(
            "daily_volume >= 0", name="ck_option_quote_daily_volume_non_negative"
        ),
        CheckConstraint(
            "open_interest >= 0", name="ck_option_quote_open_interest_non_negative"
        ),
        Index(
            "ix_option_quote_contract_timestamp",
            "option_contract_id",
            "timestamp",
        ),
        Index(
            "ix_option_quote_timestamp_brin",
            "timestamp",
            postgresql_using="brin",
        ),
        {"postgresql_partition_by": "RANGE (timestamp)"},
    )
