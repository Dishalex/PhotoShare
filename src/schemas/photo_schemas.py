from typing import List, Optional

from pydantic import BaseModel, Field, HttpUrl
from fastapi import UploadFile, File


class TagBase(BaseModel):
    tag_name: str


class TagCreate(TagBase):
    pass


class TagResponse(TagBase):
    id: int

    class Config:
        from_attributes = True  # Замість orm_mode


class ImageBase(BaseModel):
    file: UploadFile = File(...)
    url: HttpUrl
    public_id: str
    description: str
    user_id: int = 1
    tags: List[TagCreate] = []

    class Config:
        from_attributes = True  # Замість orm_mode


class ImageUpload(ImageBase):
    file: UploadFile = File(...)


class ImageUpdate(ImageBase):
    pass


class ImageResponse(ImageBase):
    id: int
    tags: List[TagResponse] = []

    class Config:
        from_attributes = True  # Замість orm_mode
