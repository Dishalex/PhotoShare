from sqlalchemy import select, extract, between
from sqlalchemy.ext.asyncio  import AsyncSession
from datetime import datetime, timedelta, date

from src.entity.models import Image



async def add_image(db: AsyncSession, url: str, public_id: str, description: str):
   
    image = Image(
        url=url,
        public_id=public_id,
#        user_id=user.id,
        description=description
    )
    db.add(image)
    await db.commit()
    await db.refresh(image)
    return image

