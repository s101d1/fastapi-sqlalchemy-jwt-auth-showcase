from sqlalchemy import ForeignKey, Uuid
from sqlalchemy import Text
from sqlalchemy.orm import mapped_column, Mapped

from .base import Base


class Post(Base):
    """
        Post model
    """
    __tablename__ = "posts"

    text = mapped_column(Text, nullable=False)
    user_id: Mapped[Uuid] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    def __repr__(self) -> str:
        return (f"Post("
                f"id={self.id!r}"
                f", created_at={self.created_at!r}"
                f", updated_at={self.updated_at!r}"
                f", text={self.text!r}"
                f", user_id={self.user_id!r}"
                f")")
