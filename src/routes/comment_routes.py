from fastapi import APIRouter, Body, HTTPException, Depends, status, Path, Query
from datetime import datetime
from sqlalchemy.ext.asyncio  import AsyncSession

from src.entity.models import Comment, Role, User
from src.database.db import get_db

from src.services.auth_service import auth_service 
from src.repository import comments
# потібна функція get_current_user

router = APIRouter(prefix='/comments', tags=['comments'])


# Роут для створення коментарів
@router.post("/")
async def create_comment(photo_id: int, text: str, current_user: User = Depends(auth_service.get_current_user),
                         db: AsyncSession = Depends(get_db)):
    comment = await comments.create_comment(db, photo_id=photo_id, text=text, user_id=current_user.id)
    return comment


# Роут для редагування коментарів
@router.put("/{comment_id}/")
async def update_comment(comment_id: int, text: str, current_user: User = Depends(auth_service.get_current_user),
                         db: AsyncSession = Depends(get_db)):
    updated_comment = await comments.update_comment(db, comment_id=comment_id, text=text, user_id=current_user.id)

    if not updated_comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if updated_comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Permission denied")

    return updated_comment

# Роут для видалення коментарів
@router.delete("/{comment_id}/")
async def delete_comment(comment_id: int, current_user: User = Depends(auth_service.get_current_user),
                         db: AsyncSession = Depends(get_db)):

    if current_user.role == "user":
        raise HTTPException(status_code=403, detail="Permission denied")

    await comments.delete_comment(db, comment_id=comment_id, user_id=current_user.id)

    return {"message": "Comment deleted successfully"}
