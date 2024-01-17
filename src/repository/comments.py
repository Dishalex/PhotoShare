
from sqlalchemy.ext.asyncio import AsyncSession
from src.entity.models import Comment
from datetime import datetime
from sqlalchemy import select, extract, between

async def create_comment(db: AsyncSession, photo_id: int, text: str, user_id: int) -> Comment:
    comment = Comment(text=text, photo_id=photo_id, user_id=user_id)
    db.add(comment)
    await db.commit()
    await db.refresh(comment)
    return comment


async def update_comment(db: AsyncSession, comment_id: int, text: str, user_id: int) -> Comment:
    comment = await db.execute(
        select(Comment).filter(Comment.id == comment_id).where(Comment.user_id == user_id)).first()

    if not comment:
        return None

    comment.text = text
    comment.updated_at = datetime.utcnow()

    await db.commit()
    await db.refresh(comment)

    return comment


async def delete_comment(db: AsyncSession, comment_id: int, user_id: int) -> None:
    comment = await db.execute(
        select(Comment).filter(Comment.id == comment_id)).first()

    if not comment:
        return None

    db.delete(comment)
    await db.commit()


