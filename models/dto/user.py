from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserResponse(BaseModel):
    """
        User Response model
    """
    id: UUID
    created_at: datetime
    updated_at: datetime | None
    email: EmailStr
