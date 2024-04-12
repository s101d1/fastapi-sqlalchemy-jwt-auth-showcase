from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from .base import Base


class User(Base):
    """
        User model
    """
    __tablename__ = "users"

    email = mapped_column(String(255), unique=True, nullable=False)
    password = mapped_column(String(60), nullable=False)
    posts: Mapped[List["Post"]] = relationship("Post", passive_deletes=True)

    def __repr__(self) -> str:
        return (f"User("
                f"id={self.id!r}"
                f", created_at={self.created_at!r}"
                f", updated_at={self.updated_at!r}"
                f", email={self.email!r}"
                f")")
