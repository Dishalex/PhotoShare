from fastapi import APIRouter, Body, HTTPException, Depends, status, Path, Query
from datetime import datetime
from sqlalchemy.orm import Session

from src.entity.models import Comment, Role, User
from src.database.db import get_db

from src.services.auth_service import get_current_user
# потібна функція get_current_user

router = APIRouter(prefix='/comments', tags=['comments'])


# Роут для створення коментарів
@router.post("/")
async def create_comment(photo_id: int, text: str, current_user: User = Depends(get_current_user),
                         db: Session = Depends(get_db)):
    comment = Comment(text=text, photo_id=photo_id, user_id=current_user.id)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


# Роут для редагування коментарів
@router.put("/{comment_id}/")
async def update_comment(comment_id: int, text: str, current_user: User = Depends(get_current_user),
                         db: Session = Depends(get_db)):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()

    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Permission denied")

    comment.text = text
    comment.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(comment)

    return comment


# Роут для видалення коментарів
@router.delete("/{comment_id}/")
async def delete_comment(comment_id: int, current_user: User = Depends(get_current_user),
                         db: Session = Depends(get_db)):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()

    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if current_user.role == "user" and comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Permission denied")

    db.delete(comment)
    db.commit()

    return {"message": "Comment deleted successfully"}
