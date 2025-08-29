import uuid
from datetime import date, datetime, timezone
from typing import Optional

from sqlalchemy import (
    NUMERIC,
    TIMESTAMP,
    BigInteger,
    Boolean,
    CheckConstraint,
    Date,
    ForeignKey,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from axiom.db.client import Base
from axiom.db.models.enums import AssetSubType, AssetType


class Security(Base):
    __tablename__ = "securities"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    symbol: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    cusip: Mapped[Optional[str]] = mapped_column(String(9), unique=True, nullable=True)
    ssid: Mapped[Optional[int]] = mapped_column(BigInteger, unique=True, nullable=True)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    exchange_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("exchanges.id", ondelete="CASCADE"),
        nullable=False,
    )
    asset_type: Mapped[AssetType] = mapped_column(String(20), nullable=False)
    asset_sub_type: Mapped[Optional[AssetSubType]] = mapped_column(
        String(10), nullable=True
    )
    sector: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    industry: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    market_cap: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    shares_outstanding: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    is_shortable: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    is_hard_to_borrow: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    htb_rate: Mapped[Optional[float]] = mapped_column(NUMERIC(8, 4), nullable=True)
    has_options: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    listing_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    delisting_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    exchange = relationship("Exchange", back_populates="securities")
    charts = relationship("Chart", back_populates="security")
    level_one_quotes = relationship("LevelOne", back_populates="security")
    level_two_quotes = relationship("LevelTwo", back_populates="security")
    option_contracts = relationship(
        "OptionContract", back_populates="underlying_security"
    )

    __table_args__ = (
        UniqueConstraint("symbol", name="uq_security_symbol"),
        UniqueConstraint("cusip", name="uq_security_cusip"),
        UniqueConstraint("ssid", name="uq_security_ssid"),
        CheckConstraint("market_cap >= 0", name="ck_security_market_cap_positive"),
        CheckConstraint(
            "shares_outstanding >= 0", name="ck_security_shares_outstanding_positive"
        ),
    )
