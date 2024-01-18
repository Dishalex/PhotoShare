from pydantic import BaseModel, Field, EmailStr

from src.entity.models import Role


class UserSchema(BaseModel):
    username: str = Field(min_length=3, max_lenght=50)
    email: EmailStr
    password: str = Field(min_length=6, max_lenght=8)


class UserResponse(BaseModel):
    id: int = 1
    username: str
    email: EmailStr
    avatar: str
    avatar: str
    role: Role


    class Config:
        from_attributes = True


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class RequestEmail(BaseModel):
    email: EmailStr