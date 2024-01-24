from typing import List, Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.entity.models import Tag
from src.schemas.tag_schemas import TagModel


async def create_tag(body: TagModel, db: AsyncSession) -> Tag:
    """
    Create a new tag.

    This function creates a new tag based on the provided tag model.

    :param body: Tag model containing tag information.
    :type body: TagModel
    :param db: Database session.
    :type db: AsyncSession
    :return: Created tag.
    :rtype: Tag
    """
    tag = Tag(tag_name=body.tag_name.lower())
    db.add(tag)
    await db.commit()
    await db.refresh(tag)
    return tag


async def get_tag_by_id(tag_id: int, db: AsyncSession) -> Tag | None:
    """
    Get a tag by its ID.

    This function retrieves a tag based on its ID.

    :param tag_id: ID of the tag.
    :type tag_id: int
    :param db: Database session.
    :type db: AsyncSession
    :return: Tag if found, None otherwise.
    :rtype: Tag | None
    """
    result = await db.execute(select(Tag).filter(Tag.id == tag_id))
    tag = result.scalar()
    return tag


async def get_tag_by_name(tag_name: str, db: AsyncSession) -> Tag | None:
    """
    Get a tag by its name.

    This function retrieves a tag based on its name.

    :param tag_name: Name of the tag.
    :type tag_name: str
    :param db: Database session.
    :type db: AsyncSession
    :return: Tag if found, None otherwise.
    :rtype: Tag | None
    """
    result = await db.execute(select(Tag).filter(Tag.tag_name == tag_name))
    tag = result.scalar()
    return tag


async def get_tags(db: AsyncSession) -> List[Type[Tag]]:
    """
    Get all tags.

    This function retrieves all tags present in the database.

    :param db: Database session.
    :type db: AsyncSession
    :return: List of tags.
    :rtype: List[Type[Tag]]
    """
    result = await db.execute(select(Tag))
    tags = result.scalars().all()
    return tags


async def update_tag(tag_id: int, body: TagModel, db: AsyncSession) -> Tag | None:
    """
    Update a tag.

    This function updates the tag with the specified tag_id.

    :param tag_id: ID of the tag to be updated.
    :type tag_id: int
    :param body: TagModel containing the new tag information.
    :type body: TagModel
    :param db: Database session.
    :type db: AsyncSession
    :return: Updated tag.
    :rtype: Tag | None
    """
    result = await db.execute(select(Tag).filter(Tag.id == tag_id))
    tag = result.scalar()
    if not tag:
        return None
    tag.tag_name = body.tag_name.lower()
    await db.commit()
    return tag


async def remove_tag_by_id(tag_id: int, db: AsyncSession) -> Tag | None:
    """
    Remove a tag by ID.

    This function removes the tag with the specified tag_id.

    :param tag_id: ID of the tag to be removed.
    :type tag_id: int
    :param db: Database session.
    :type db: AsyncSession
    :return: Removed tag.
    :rtype: Tag | None
    """
    result = await db.execute(select(Tag).filter(Tag.id == tag_id))
    tag = result.scalar()
    if tag:
        db.delete(tag)
        await db.commit()
    return tag


async def remove_tag_by_name(tag_name: str, db: AsyncSession) -> Tag | None:
    """
    Remove a tag by name.

    This function removes the tag with the specified tag_name.

    :param tag_name: Name of the tag to be removed.
    :type tag_name: str
    :param db: Database session.
    :type db: AsyncSession
    :return: Removed tag.
    :rtype: Tag | None
    """
    result = await db.execute(select(Tag).filter(Tag.tag_name == tag_name))
    tag = result.scalar()
    if tag:
        db.delete(tag)
        await db.commit()
    return tag
