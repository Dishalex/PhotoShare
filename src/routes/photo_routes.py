import pathlib
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Body
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from src.database.db import get_db
from src.entity.models import Image, Tag
from src.schemas.photo_schemas import ImageUpload, ImageModel, ImageUpdate
from src.services.cloudinary_service import CloudImage
from src.repository import photos as repository_image

router = APIRouter(prefix='/images', tags=['images'])

UPLOADS_DIR = "uploads"
MAX_FILE_SIZE = 1_000_000


@router.post("/", response_model=ImageModel, status_code=status.HTTP_201_CREATED)
async def upload_image(
    email: EmailStr,
    description: str = None,
    file: UploadFile = File(),
    db: AsyncSession = Depends(get_db)
):

    public_id = CloudImage.generate_name_image(email)
    upload_file = CloudImage.upload_image(file.file, public_id)
    src_url = CloudImage.get_url_for_image(public_id, upload_file)
    image = await repository_image.add_image(db, src_url, public_id, description)
    return image





@router.get("/{image_id}", response_model=ImageModel)
async def read_image(image_id: int, db: AsyncSession = Depends(get_db)):
    image = await db.get(Image, image_id, options=selectinload(Image.tags))
    if image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    return image


@router.put("/{image_id}", response_model=ImageModel)
async def update_image(image_id: int, image_data: ImageUpdate, db: AsyncSession = Depends(get_db)):
    image = await db.get(Image, image_id)
    if image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    for field, value in image_data.dict(exclude_unset=True).items():
        setattr(image, field, value)
    await db.commit()
    await db.refresh(image)
    return image


@router.delete("/{image_id}", response_model=ImageModel)
async def delete_image(image_id: int, db: AsyncSession = Depends(get_db)):
    image = await db.get(Image, image_id)
    if image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    db.delete(image)
    await db.commit()
    return image


@router.get("/", response_model=list[ImageModel])
async def list_images(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    images = await db.query(Image).offset(skip).limit(limit).all()
    return images
