import boto3
from io import BytesIO
import boto3
from botocore.exceptions import NoCredentialsError
from fastapi import UploadFile
from dotenv import load_dotenv
import os
from sqlalchemy.orm import Session
from ...models import models


load_dotenv(".env")


class DB:
    aws_access_key_id = os.getenv("aws_access_key_id")
    aws_secret_access_key = os.getenv("aws_secret_access_key")
    region = os.getenv("region")
    bucket_name = os.getenv("bucket_name")


s3 = boto3.client(
    "s3",
    aws_access_key_id=DB.aws_access_key_id,
    aws_secret_access_key=DB.aws_secret_access_key,
    region_name=DB.region,
)


def upload_book_to_s3(file: UploadFile):
    s3_url = None  # Initialize with a default value
    try:

        # Upload the file
        s3.upload_fileobj(file.file, DB.bucket_name, file.filename)

        # Generate the S3 URL
        s3_url = f"https://{DB.bucket_name}.s3.amazonaws.com/{file.filename}"

    except NoCredentialsError as e:
        print("Credentials not available")
        # Handle the case where credentials are not available or incorrect
        raise e
    except Exception as e:
        print(f"Error uploading to S3: {e}")
        # Handle other exceptions

    return s3_url


def download_object_from_s3(s3_url: str):
    # Parse the S3 URL to extract bucket name and object key
    parts = s3_url.replace("https://", "").split("/")
    object_key = "/".join(parts[1:])
    # Download the file from S3
    try:
        response = s3.get_object(Bucket=DB.bucket_name, Key=object_key)
        content = response["Body"].read()
        return BytesIO(content)
    except NoCredentialsError as e:
        print("Credentials not available.")
        raise e
    except Exception as e:
        print(f"Error downloading from S3: {e}")
        raise e


def delete_book_from_s3(book_id: int, db: Session):
    s3_url = (
        db.query(models.Books.book_file)
        .filter(models.Books.book_id == book_id)
        .first()[0]
    )
    print(s3_url)
    parts = s3_url.replace("https://", "").split("/")
    object_key = "/".join(parts[1:])
    try:
        # Delete the object
        s3.delete_object(Bucket=DB.bucket_name, Key=object_key)
        print(f"Object '{object_key}' deleted from S3 bucket '{DB.bucket_name}'.")

    except NoCredentialsError as e:
        print("Credentials not available.")
        raise e
    except Exception as e:
        print(f"Error deleting object from S3: {e}")
        raise e
