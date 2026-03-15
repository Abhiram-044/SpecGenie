import boto3
from app.core.config import settings
import uuid

s3 = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY,
    aws_secret_access_key=settings.AWS_SECRET_KEY,
    region_name="ap-south-1"
)

async def upload_profile_picture(file):
    file_key = f"profile-picture/{uuid.uuid4()}-{file.filename}"

    s3.upload_fileobj(
        file.file,
        settings.AWS_S3_BUCKET,
        file_key,
        ExtraArgs={
            "ContentType": file.content_type
        }
    )

    return file_key

async def delete_object(key):
    s3.delete_object(
        Bucket=settings.AWS_S3_BUCKET,
        Key=key
    )

async def upload_signature(file):
    file_key = f"declaration-signature/{uuid.uuid4()}-{file.filename}"

    s3.upload_fileobj(
        file.file,
        settings.AWS_S3_BUCKET,
        file_key,
        ExtraArgs={
            "ContentType": file.content_type
        }
    )

    return file_key

async def generate_signed_url(key: str):
    return s3.generate_presigned_url(
        "get_object",
        Params={
            "Bucket": settings.AWS_S3_BUCKET,
            "Key": key
        },
        ExpiresIn=86400
    )