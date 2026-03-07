from datetime import datetime, timezone
from pydantic import EmailStr, Field

from app.models.base import MongoBaseModel

class User(MongoBaseModel):
    email: EmailStr
    username: str
    hashed_password: str
    latest_session_id: str | None
    is_active: bool = False
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )