import uuid
from datetime import datetime, timezone

from sqlalchemy import TIMESTAMP, Boolean, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from axiom.db.client import Base


class Exchange(Base):
    __tablename__ = "exchanges"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    code: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    mic_code: Mapped[str] = mapped_column(String(4), unique=True, nullable=False)
    timezone: Mapped[str] = mapped_column(String(50), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="USD")
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

    securities = relationship("Security", back_populates="exchange")

    __table_args__ = (
        UniqueConstraint("code", name="uq_exchange_code"),
        UniqueConstraint("mic_code", name="uq_exchange_mic_code"),
    )
