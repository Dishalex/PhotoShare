import hashlib
import datetime
from typing import Tuple

import cloudinary
import cloudinary.uploader
from src.conf.config import config


class CloudImage:
    cloudinary.config(
        cloud_name=config.CLD_NAME,
        api_key=config.CLD_API_KEY,
        api_secret=config.CLD_API_SECRET,
        secure=True,
    )

    @staticmethod
    def generate_name_image(email: str) -> str:
        name = hashlib.sha256(email.encode("utf-8")).hexdigest()[:12]
        time = datetime.datetime.now()
        return f"photo_share/{name}{time}"

    @staticmethod
    def upload_image(file, public_id: str) -> dict:
        upload_file = cloudinary.uploader.upload(file, public_id=public_id)
        return upload_file

    @staticmethod
    def get_url_for_image(public_id, upload_file) -> str:
        src_url = cloudinary.CloudinaryImage(public_id).build_url(
            version=upload_file.get("version")
        )
        return src_url
       
    def delete_img(self, public_id: str):
        cloudinary.uploader.destroy(public_id, resource_type="image")
        return f"{public_id} deleted"

    @staticmethod
    async def change_size(public_id: str, width: int) -> Tuple[str, str]:
        img = cloudinary.CloudinaryImage(public_id).image(
            transformation=[{"width": width, "crop": "pad"}]
        )
        url = img.split('"')
        upload_image = cloudinary.uploader.upload(url[1], folder="photo_share")
        return upload_image["url"], upload_image["public_id"]

    @staticmethod
    async def fade_edges_image(public_id: str, effect: str = "vignette") -> str:
        img = cloudinary.CloudinaryImage(public_id).image(effect=effect)
        url = img.split('"')
        upload_image = cloudinary.uploader.upload(url[1], folder="photo_share")
        return upload_image["url"], upload_image["public_id"]
    
    @staticmethod
    async def make_black_white_image(public_id: str, effect: str = "art:audrey"
    ) -> str:
        img = cloudinary.CloudinaryImage(public_id).image(effect=effect)
        url = img.split('"')
        upload_image = cloudinary.uploader.upload(url[1], folder="photo_share")
        return upload_image["url"], upload_image["public_id"]


image_cloudinary = CloudImage()