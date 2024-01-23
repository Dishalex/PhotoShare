from typing import List
from pydantic import BaseModel, Field, HttpUrl

from src.schemas.comment_schemas import CommentByUser


class ImageModel(BaseModel):
    id: int
    url: str
    public_id: str
    user_id: int


class ImageProfile(BaseModel):
    url: str
    description: str | None
    average_rating: float | None
    tags: List[str] | None
    comments: List[CommentByUser] | None


class ImageAddResponse(BaseModel):
    image: ImageModel
    detail: str = "Image has been added"


class ImageDeleteResponse(BaseModel):
    detail: str = "Image has been deleted"


class ImageUpdateResponse(BaseModel):
    id: int
    description: str
    detail: str = "Image has been updated"


class ImageURLResponse(BaseModel):
    url: str


class ImageChangeSizeModel(BaseModel):
    id: int
    width: int = 200


class ImageTransformModel(BaseModel):
    id: int


class ImageQRResponse(BaseModel):
    image_id: int
    qr_code_url: str


class ImagesByFilter(BaseModel):
    images: List[ImageProfile]