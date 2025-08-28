import uuid
from datetime import date, datetime, timezone
from typing import Optional

from sqlalchemy import (
    TIMESTAMP,
    BigInteger,
    Boolean,
    CheckConstraint,
    Date,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from axiom.db.client import Base
from axiom.db.models.enums import (
    ContractType,
    ExerciseType,
    ExpirationType,
    SettlementType,
)


class OptionContract(Base):
    __tablename__ = "option_contracts"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    underlying_security_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("securities.id", ondelete="CASCADE"),
        nullable=False,
    )
    symbol: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    cusip: Mapped[Optional[str]] = mapped_column(String(9), unique=True, nullable=True)
    ssid: Mapped[Optional[int]] = mapped_column(BigInteger, unique=True, nullable=True)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    contract_type: Mapped[ContractType] = mapped_column(String(4), nullable=False)
    strike_price: Mapped[int] = mapped_column(BigInteger, nullable=False)
    expiration_date: Mapped[date] = mapped_column(Date, nullable=False)
    expiration_type: Mapped[Optional[ExpirationType]] = mapped_column(
        String(10), nullable=True
    )
    days_to_expiration: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    exercise_type: Mapped[Optional[ExerciseType]] = mapped_column(
        String(10), nullable=True
    )
    settlement_type: Mapped[Optional[SettlementType]] = mapped_column(
        String(10), nullable=True
    )
    multiplier: Mapped[int] = mapped_column(Integer, nullable=False, default=100)
    last_trading_day: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    is_penny_pilot: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_mini: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_non_standard: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )
    deliverables: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
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

    underlying_security = relationship("Security", back_populates="option_contracts")
    option_quotes = relationship("OptionQuote", back_populates="option_contract")

    __table_args__ = (
        UniqueConstraint("symbol", name="uq_option_contract_symbol"),
        UniqueConstraint("cusip", name="uq_option_contract_cusip"),
        UniqueConstraint("ssid", name="uq_option_contract_ssid"),
        CheckConstraint(
            "strike_price > 0", name="ck_option_contract_strike_price_positive"
        ),
        CheckConstraint(
            "multiplier > 0", name="ck_option_contract_multiplier_positive"
        ),
        CheckConstraint(
            "days_to_expiration >= 0",
            name="ck_option_contract_days_to_expiration_non_negative",
        ),
    )
