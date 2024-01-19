from sqlalchemy.future import select
from src.entity.models import Comment, User
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime


async def create_comment(db: AsyncSession, image_id: int, comment_text: str, user: User):
    comment = Comment(comment=comment_text, image_id=image_id, user_id=user.id)
    db.add(comment)
    await db.commit()
    await db.refresh(comment)  # Оновлення об'єкта коментаря після збереження
    return comment


async def update_comment(db: AsyncSession, comment_id: int, text: str, user: User):
    comment = await db.execute(select(Comment).filter(Comment.id == comment_id))
    comment = comment.scalar()

    if not comment:
        return None

    if user.role.name == "user" and comment.user_id != user.id:
        return None

    comment.comment = text
    comment.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(comment)

    return comment


async def delete_comment(db: AsyncSession, comment_id: int, user: User):
    comment = await db.execute(select(Comment).filter(Comment.id == comment_id))
    comment_ = comment.scalar()

    if not comment_:
        return False

    if user.role.name == "user" and comment_.user_id == user.id:
        return False

    if user.role.name == "admin" or user.role.name == "moderator":
        await db.delete(comment_)
        await db.commit()
        return True
