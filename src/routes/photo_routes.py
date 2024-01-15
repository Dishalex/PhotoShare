from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.database.db import get_db
from src.entity.models import User, Image, Tag, Comment, TransformedImage
from src.schemas.photo_schemas import ImageCreate, ImageResponse, ImageUpdate

photo_routes = APIRouter()


@photo_routes.post("/images/", response_model=ImageResponse)
async def create_image(image_data: ImageCreate, db: AsyncSession = Depends(get_db)):
    # Перевірка наявності тегів та їх створення
    tags = []
    for tag_data in image_data.tags:
        existing_tag = await db.query(Tag).filter(Tag.tag_name == tag_data.tag_name).first()
        if existing_tag:
            tags.append(existing_tag)
        else:
            new_tag = Tag(**tag_data.dict())
            db.add(new_tag)
            tags.append(new_tag)

    # Створення нового зображення та додавання тегів до зображення
    image = Image(**image_data.dict(exclude={"tags"}))  # Виключити теги з даних зображення
    image.tags.extend(tags)

    db.add(image)
    await db.commit()
    await db.refresh(image)
    return image

@photo_routes.get("/images/{image_id}", response_model=ImageResponse)
async def read_image(image_id: int, db: AsyncSession = Depends(get_db)):
    image = await db.get(Image, image_id, options=selectinload(Image.tags))
    if image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    return image


@photo_routes.put("/images/{image_id}", response_model=ImageResponse)
async def update_image(image_id: int, image_data: ImageUpdate, db: AsyncSession = Depends(get_db)):
    image = await db.get(Image, image_id)
    if image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    for field, value in image_data.dict(exclude_unset=True).items():
        setattr(image, field, value)
    await db.commit()
    await db.refresh(image)
    return image


@photo_routes.delete("/images/{image_id}", response_model=ImageResponse)
async def delete_image(image_id: int, db: AsyncSession = Depends(get_db)):
    image = await db.get(Image, image_id)
    if image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    db.delete(image)
    await db.commit()
    return image


@photo_routes.get("/images/", response_model=list[ImageResponse])
async def list_images(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    images = await db.query(Image).offset(skip).limit(limit).all()
    return images
