from pydantic import BaseModel, EmailStr, Field, field_validator
from pydantic_settings import SettingsConfigDict
from datetime import datetime


class TagModel(BaseModel):
    tag_name: str


class TagResponse(TagModel):
    model_config = SettingsConfigDict(from_attributes=True)
    id: int
    tag_name: str


class AddTag(BaseModel):
    detail: str = "Image tags has been updated"
