from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, StringConstraints
from typing_extensions import Annotated


class AddPostData(BaseModel):
    """
        Add post data model
    """
    text: Annotated[str, StringConstraints(strip_whitespace=True, min_length=5)]


class PostResponse(BaseModel):
    """
        Post response model
    """
    id: UUID
    created_at: datetime
    updated_at: datetime | None
    text: str
    user_id: UUID
