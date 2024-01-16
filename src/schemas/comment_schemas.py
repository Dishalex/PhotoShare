import datetime
from pydantic import BaseModel, Field


class CommentModel(BaseModel):
    comment: str = Field(default='default text', min_length=1, max_length=255)


class CommentResponse(BaseModel):
    id: int
    user_id: int
    image_id: int
    comment: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True
