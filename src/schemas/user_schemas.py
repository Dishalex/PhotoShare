from datetime import datetime
from pydantic import BaseModel, Field, EmailStr
from pydantic_settings import SettingsConfigDict
from typing import Optional

from src.entity.models import Role


class UserSchema(BaseModel):
    model_config = SettingsConfigDict(from_attributes=True)
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=6, max_length=8)
    first_name: str
    last_name: str
    sex: Optional[str]
    role: Role


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    first_name: str | None
    last_name: str | None
    sex: str | None
    role: Role
    avatar: str | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class RequestEmail(BaseModel):
    email: EmailStr