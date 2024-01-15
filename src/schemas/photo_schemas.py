from typing import List, Optional

from pydantic import BaseModel


class TagBase(BaseModel):
    tag_name: str


class TagCreate(TagBase):
    pass


class TagResponse(TagBase):
    id: int

    class Config:
        orm_mode = True


class ImageBase(BaseModel):
    url: str
    public_id: str
    description: str
    user_id: int
    tags: List[TagCreate] = []  # Змінено на List[TagCreate]

    class Config:
        orm_mode = True


class ImageCreate(ImageBase):
    pass


class ImageUpdate(ImageBase):
    pass


class ImageResponse(ImageBase):
    id: int
    tags: List[TagResponse] = []

    class Config:
        orm_mode = True
