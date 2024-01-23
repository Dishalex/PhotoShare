from fastapi import HTTPException, status
from sqlalchemy import func, desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.repository import ratings as repository_ratings

from src.entity.models import Image, User, Tag, Rating
from src.routes.tags import create_tag
from src.schemas.photo_schemas import (
    ImageChangeSizeModel,
    ImageAddResponse,
    ImageModel,
    ImageTransformModel,
    ImageProfile,
    CommentByUser,
    ImagesByFilter,
    ImageQRResponse,
)
from src.schemas.tag_schemas import TagModel
from src.conf import messages
from src.services.cloudinary_service import CloudImage, image_cloudinary

import qrcode
from io import BytesIO


async def add_image(
    db: AsyncSession, url: str, public_id: str, user: User, description: str
) -> Image | None:
    if not user:
        return None
    image = Image(
        url=url, public_id=public_id, user_id=user.id, description=description
    )
    db.add(image)
    await db.commit()
    await db.refresh(image)
    return image


async def delete_image(db: AsyncSession, image_id: int) -> Image | None:
    result = await db.execute(select(Image).filter(Image.id == image_id))
    image = result.scalar()

    if image:
        image_cloudinary.delete_img(image.public_id)
        await db.delete(image)
        await db.commit()

    return image


async def update_desc(db: AsyncSession, image_id: int, description: str) -> Image | None:
    image = await db.execute(select(Image).filter(Image.id == image_id))
    image = image.scalar()
    if image:
        image.description = description
        await db.commit()
        await db.refresh(image)
    return image


async def get_image_by_id(db: AsyncSession, image_id: int) -> Image | None:
    image = await db.execute(select(Image).filter(Image.id == image_id))
    return image.scalar()


async def change_size_image(
    body: ImageChangeSizeModel, db: AsyncSession, user: User
) -> ImageAddResponse:
    image = await db.execute(select(Image).filter(Image.id == body.id))
    image = image.scalar()

    if image is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=messages.IMAGE_NOT_FOUND
        )
    if image.user_id != user.id:
        raise HTTPException(status_code=403, detail=messages.NOT_ALLOWED)

    url, public_id = await image_cloudinary.change_size(image.public_id, body.width)
    new_image = Image(
        url=url, public_id=public_id, user_id=user.id, description=image.description
    )
    db.add(new_image)
    await db.commit()
    await db.refresh(new_image)
    image_model = ImageModel(
        id=new_image.id,
        url=new_image.url,
        public_id=new_image.public_id,
        user_id=new_image.user_id,
    )
    return ImageAddResponse(image=image_model, detail=messages.IMAGE_RESIZED_ADDED)


async def fade_edges_image(
    body: ImageTransformModel, db: AsyncSession, user: User
) -> ImageAddResponse:
    image = await db.execute(select(Image).filter(Image.id == body.id))
    image = image.scalar()

    if image is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=messages.IMAGE_NOT_FOUND
        )
    if image.user_id != user.id:
        raise HTTPException(status_code=403, detail=messages.NOT_ALLOWED)

    url, public_id = await image_cloudinary.fade_edges_image(public_id=image.public_id)

    new_image = Image(
        url=url, public_id=public_id, user_id=user.id, description=image.description
    )
    db.add(new_image)
    await db.commit()
    await db.refresh(new_image)

    image_model = ImageModel(
        id=new_image.id,
        url=new_image.url,
        public_id=new_image.public_id,
        user_id=new_image.user_id,
    )

    return ImageAddResponse(image=image_model, detail=messages.IMAGE_FADE_ADDED)


async def black_white_image(
    body: ImageTransformModel, db: AsyncSession, user: User
) -> ImageAddResponse:
    image = await db.execute(select(Image).filter(Image.id == body.id))
    image = image.scalar()

    if image is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=messages.IMAGE_NOT_FOUND
        )
    if image.user_id != user.id:
        raise HTTPException(status_code=403, detail=messages.NOT_ALLOWED)

    url, public_id = await image_cloudinary.make_black_white_image(
        public_id=image.public_id
    )

    new_image = Image(
        url=url, public_id=public_id, user_id=user.id, description=image.description
    )

    db.add(new_image)
    await db.commit()
    await db.refresh(new_image)

    image_model = ImageModel(
        id=new_image.id,
        url=new_image.url,
        public_id=new_image.public_id,
        user_id=new_image.user_id,
    )

    return ImageAddResponse(image=image_model, detail=messages.BLACK_WHITE_ADDED)


async def get_all_images(
    db: AsyncSession,
    current_user: User,
    keyword: str = None,
    tag: str = None,
) -> ImagesByFilter:
    query = select(Image)
    if keyword:
        query = query.filter(Image.description.ilike(f"%{keyword}%"))
    if tag:
        query = query.filter(Image.tags.any(Tag.tag_name == tag))
    
    query = query.order_by(desc(Image.created_at))
    result = await db.execute(query)
    images = []
    async for image in result:
        tags = []
        comments = []
        async for comment in image.comments:
            new_comment = CommentByUser(
                user_id=comment.user_id, comment=comment.comment
            )
            comments.append(new_comment)
        async for tag in image.tags:
            new_tag = tag.tag_name
            tags.append(new_tag)
        rating = await repository_ratings.calculate_rating(image.id, db, current_user)
        new_rating = rating["average_rating"]
        new_image = ImageProfile(
            url=image.url,
            description=image.description,
            average_rating=new_rating,
            tags=tags,
            comments=comments,
        )
        images.append(new_image)
    all_images = ImagesByFilter(images=images)
    return all_images


async def create_qr(body: ImageTransformModel, db: AsyncSession, user: User) -> ImageQRResponse:
    image = await db.execute(select(Image).filter(Image.id == body.id))
    image = image.scalar()

    if image is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=messages.IMAGE_NOT_FOUND
        )
    if image.qr_url:
        return ImageQRResponse(image_id=image.id, qr_code_url=image.qr_url)

    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(image.url)
    qr.make(fit=True)

    qr_code_img = BytesIO()
    qr.make_image(fill_color="black", back_color="white").save(qr_code_img)

    qr_code_img.seek(0)

    new_public_id = CloudImage.generate_name_image(user.email)

    upload_file = CloudImage.upload_image(qr_code_img, new_public_id)

    qr_code_url = CloudImage.get_url_for_image(new_public_id, upload_file)

    image.qr_url = qr_code_url

    db.commit()

    return ImageQRResponse(image_id=image.id, qr_code_url=qr_code_url)


async def add_tag(db: AsyncSession, user: User, image_id: int, tag_name: str) -> dict:
    image = await db.execute(select(Image).filter(Image.id == image_id))
    image = image.scalar()

    if image is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=messages.IMAGE_NOT_FOUND
        )
    if image.user_id != user.id:
        raise HTTPException(status_code=403, detail=messages.NOT_ALLOWED)
    if len(image.tags) >= 5:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=messages.ONLY_FIVE_TAGS
        )
    tag = await db.execute(select(Tag).filter(Tag.tag_name == tag_name.lower()))
    tag = tag.scalar()

    if tag is None:
        tag_model = TagModel(tag_name=tag_name)
        tag = await create_tag(tag_model, db)

    image.tags.append(tag)

    await db.commit()
    await db.refresh(image)

    return {"message": "Tag successfully added", "tag": tag.tag_name}
