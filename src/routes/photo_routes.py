import pathlib
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from src.database.db import get_db
from src.entity.models import Image, Tag
from src.schemas.photo_schemas import ImageUpload, ImageResponse, ImageUpdate

router = APIRouter(prefix='/images', tags=['images'])

UPLOADS_DIR = "uploads"
MAX_FILE_SIZE = 1_000_000


@router.post("/", response_model=ImageResponse)
async def upload_image(
        image_data: ImageUpload = Body(...),
        file: UploadFile = File(...),
        db: AsyncSession = Depends(get_db)
):
    # Перевірка кількості тегів
    if len(image_data.tags) > 5:
        raise HTTPException(status_code=400, detail="Максимальна кількість тегів - 5")

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

    # Завантаження файлу
    file_path = f"{UPLOADS_DIR}/{file.filename}"
    file_size = 0
    with open(file_path, "wb") as f:
        while True:
            chunk = await file.read(1024)
            if not chunk:
                break
            file_size += len(chunk)
            if file_size > MAX_FILE_SIZE:
                f.close()
                pathlib.Path(file_path).unlink()
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail=f"File size is over the limit: {MAX_FILE_SIZE}"
                )
            f.write(chunk)

    # Створення нового зображення та додавання тегів до зображення
    image = Image(**image_data.dict(exclude={"tags"}))
    image.file_path = file_path
    image.tags.extend(tags)

    db.add(image)
    await db.commit()
    await db.refresh(image)
    return image


@router.get("/{image_id}", response_model=ImageResponse)
async def read_image(image_id: int, db: AsyncSession = Depends(get_db)):
    image = await db.get(Image, image_id, options=selectinload(Image.tags))
    if image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    return image


@router.put("/{image_id}", response_model=ImageResponse)
async def update_image(image_id: int, image_data: ImageUpdate, db: AsyncSession = Depends(get_db)):
    image = await db.get(Image, image_id)
    if image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    for field, value in image_data.dict(exclude_unset=True).items():
        setattr(image, field, value)
    await db.commit()
    await db.refresh(image)
    return image


@router.delete("/{image_id}", response_model=ImageResponse)
async def delete_image(image_id: int, db: AsyncSession = Depends(get_db)):
    image = await db.get(Image, image_id)
    if image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    db.delete(image)
    await db.commit()
    return image


@router.get("/", response_model=list[ImageResponse])
async def list_images(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    images = await db.query(Image).offset(skip).limit(limit).all()
    return images
