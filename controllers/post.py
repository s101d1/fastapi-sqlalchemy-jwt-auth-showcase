from uuid import UUID

from sqlalchemy import delete, select

from database import session
from models.dto.post import AddPostData
from models.post import Post


def get_posts(user_id: UUID):
    """
        Get user's posts handler
    """
    return session.scalars(select(Post).where(Post.user_id == user_id).order_by(Post.created_at.desc())).all()


def add_post(data: AddPostData, user_id: UUID):
    """
        Add new post handler
    """
    post = Post(text=data.text, user_id=user_id)
    session.add(post)
    session.commit()

    return {"message": "Post created", "post_id": post.id}


def delete_post(post_id: UUID, user_id: UUID):
    """
        Delete post handler
    """
    result = session.execute(delete(Post).where(Post.id == post_id, Post.user_id == user_id))
    session.commit()

    return {"deleted": result.rowcount > 0}
