from fastapi import Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.user_schemas import UserSchema
from libgravatar import Gravatar

from src.database.db import get_db
from src.entity.models import User


async def get_user_by_email(email: str, db: AsyncSession = Depends(get_db)):
    """
    The get_user_by_email function takes an email address and returns the user object associated with that email.
    If no such user exists, it returns None.

    :param email: str: Specify the email of the user we want to retrieve
    :param db: AsyncSession: Get the database session
    :return: A single user
    :doc-author: Trelent
    """
    stmt = select(User).filter_by(email=email)
    user = await db.execute(stmt)
    user = user.scalar_one_or_none()
    return user


async def create_user(body: UserSchema, db: AsyncSession = Depends(get_db)):
    """
    The create_user function creates a new user in the database.

    :param body: UserSchema: Validate the request body
    :param db: AsyncSession: Get the database session
    :return: The newly created user
    :doc-author: Trelent
    """
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as err:
        print(err)

    new_user = User(**body.model_dump(), avatar=avatar)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: AsyncSession):
    """
    The update_token function updates the refresh token for a user.

    :param user: User: Identify the user to update
    :param token: str | None: Set the refresh token for a user
    :param db: AsyncSession: Pass the database session to the function
    :return: The user object
    :doc-author: Trelent
    """
    user.refresh_token = token
    await db.commit()


async def confirmed_email(email: str, db: AsyncSession):
    """
    The confirmed_email function takes an email address and a database connection as arguments.
    It then queries the database for the user with that email address, sets their confirmed field to True,
    and commits those changes to the database.

    :param email: str: Specify the email address of the user to confirm
    :param db: AsyncSession: Pass the database session into the function
    :return: Nothing
    :doc-author: Trelent
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    await db.commit()


async def update_avatar_url(email: str, url: str | None, db: AsyncSession) -> User:
    """
    The update_avatar_url function updates the avatar URL for a user.

    :param email: str: Specify the email of the user whose avatar url is to be updated
    :param url: str | None: Specify that the url parameter can either be a string or none
    :param db: AsyncSession: Pass in the database session
    :return: The updated user
    :doc-author: Trelent
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    await db.commit()
    await db.refresh(user)
    return user



async def get_total_users_count(session: AsyncSession):
    # Executing an asynchronous query to the database to get the total count of users
    count = await session.execute(select(func.count(User.id)))
    total_count = count.scalar()
    return total_count