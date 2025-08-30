import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import TIMESTAMP, Boolean, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from axiom.db.client import Base


class StreamSubscription(Base):
    __tablename__ = "stream_subscriptions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[str] = mapped_column(String(64), nullable=False)
    symbol: Mapped[str] = mapped_column(String(32), nullable=False)
    stream_type: Mapped[str] = mapped_column(String(16), nullable=False)

    # For L2, identify the book if needed (e.g., NYSE, NASDAQ)
    book: Mapped[Optional[str]] = mapped_column(String(16), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    __table_args__ = (
        UniqueConstraint(
            "user_id", "symbol", "stream_type", "book", name="uq_stream_sub_unique"
        ),
        Index("ix_stream_sub_user_type_symbol", "user_id", "stream_type", "symbol"),
    )
