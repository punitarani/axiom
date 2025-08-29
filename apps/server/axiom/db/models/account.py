import uuid
from datetime import datetime, timezone

from sqlalchemy import TIMESTAMP, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from axiom.db.client import Base


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    account_hash: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    account_number: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)

    nickname: Mapped[str | None] = mapped_column(String(100), nullable=True)
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

    transactions = relationship("Transaction", back_populates="account")

    __table_args__ = (
        UniqueConstraint("account_hash", name="uq_account_hash"),
        UniqueConstraint("account_number", name="uq_account_number"),
    )
