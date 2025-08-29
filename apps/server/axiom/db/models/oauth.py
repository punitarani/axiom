from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import UUID, Column, DateTime, String

from axiom.db.client import Base


class OAuthState(Base):
    __tablename__ = "oauth_states"

    id = Column(UUID, primary_key=True, default=uuid4)
    user_id = Column(String, index=True, unique=True)
    state = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
