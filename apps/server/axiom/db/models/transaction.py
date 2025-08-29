import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import (
    NUMERIC,
    TIMESTAMP,
    CheckConstraint,
    ForeignKey,
    Index,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from axiom.db.client import Base
from axiom.db.models.enums import TransactionType


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    account_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("accounts.id", ondelete="CASCADE"),
        nullable=False,
    )

    provider: Mapped[str] = mapped_column(String(20), nullable=False, default="schwab")
    provider_transaction_id: Mapped[str] = mapped_column(String(64), nullable=False)

    # Classification
    type: Mapped[TransactionType] = mapped_column(String(32), nullable=False)
    symbol: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)

    # Monetary amounts (use NUMERIC for exactness)
    quantity: Mapped[Optional[float]] = mapped_column(NUMERIC(20, 8), nullable=True)
    price: Mapped[Optional[float]] = mapped_column(NUMERIC(20, 8), nullable=True)
    amount: Mapped[Optional[float]] = mapped_column(NUMERIC(20, 8), nullable=True)
    fees: Mapped[Optional[float]] = mapped_column(NUMERIC(20, 8), nullable=True)

    transaction_time: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    account = relationship("Account", back_populates="transactions")

    __table_args__ = (
        UniqueConstraint(
            "provider",
            "provider_transaction_id",
            name="uq_transaction_provider_id",
        ),
        CheckConstraint("quantity IS NULL OR quantity >= 0", name="ck_txn_qty_nonneg"),
        Index(
            "ix_transaction_account_time",
            "account_id",
            "transaction_time",
        ),
        Index(
            "ix_transaction_time_brin",
            "transaction_time",
            postgresql_using="brin",
        ),
    )
