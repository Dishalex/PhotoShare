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


class ImageModel(ImageBase):
    id: int
    url: str
    public_id: str
    user_id: int