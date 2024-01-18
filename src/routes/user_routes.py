import pickle
import cloudinary
import cloudinary.uploader

from fastapi import APIRouter, Body, File, HTTPException, Depends, status, Path, Query, UploadFile
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.ext.asyncio  import AsyncSession
from src.database.db import get_db

from src.schemas.user_schemas import UserResponse
from src.entity.models import User
from src.conf.config import config
from src.services.auth_service import auth_service
from src.repository import users as repository_users


router = APIRouter(prefix='/users', tags=['users'])
cloudinary.config(cloud_name=config.CLD_NAME, api_key=config.CLD_API_KEY, api_secret=config.CLD_API_SECRET, secure=True)

@router.get("/me", response_model=UserResponse,
            description='No more than 3 requests per minute',
            dependencies=[Depends(RateLimiter(times=1, seconds=20))])
async def get_current_user(user: User = Depends(auth_service.get_current_user)):
    """
    The get_current_user function is a dependency that will be injected into the
        get_users function. It uses the Depends() class to inject it as a parameter, and
        then returns the user object if it exists.
    
    :param user: User: Specify the type of object that will be returned by the function
    :return: The user object
    :doc-author: Trelent
    """
    return user



@router.patch("/avatar", response_model=UserResponse,
            description='No more than 3 requests per minute',
            dependencies=[Depends(RateLimiter(times=1, seconds=20))])
async def get_current_user(file: UploadFile = File(),
                           user: User = Depends(auth_service.get_current_user),
                           db: AsyncSession = Depends(get_db)):
    """
    The get_current_user function is a dependency that will be called by the
        get_current_user endpoint. It takes in an optional file parameter, which
        is used to upload a new avatar image for the user. If no file parameter
        is provided, then it simply returns the current user object.
    
    :param file: UploadFile: Get the file that is being uploaded
    :param user: User: Get the current user
    :param db: AsyncSession: Get the database session
    :return: The current user, based on the token
    :doc-author: Trelent
    """
    public_id = f"Contacts_Hw_web/{user.email}"
    res = cloudinary.uploader.upload(file.file, public_id=public_id, overwrite=True)
    res_url = cloudinary.CloudinaryImage(public_id).build_url(width=250, height=250, crop="fill", version=res.get("version"))

    await repository_users.update_avatar_url(user.email, res_url, db)
    auth_service.cache.set(user.email, pickle.dumps(user))
    auth_service.cache.expire(user.email, 300)

    return user