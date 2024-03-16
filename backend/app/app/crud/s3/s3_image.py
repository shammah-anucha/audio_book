import boto3
import boto3
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv
import os
from PIL import Image
import io
import tempfile


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


def upload_image_to_s3(image: Image, filename):
    s3_url = None  # Initialize with a default value
    # try:
    # Save the image to a BytesIO buffer
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format=image.format)
    imgByteArr = imgByteArr.getvalue()

    temp_file = tempfile.TemporaryFile()
    try:
        temp_file.write(imgByteArr)
        temp_file.seek(0)
        # Upload the image buffer to S3
        s3.upload_fileobj(temp_file, DB.bucket_name, filename)
        # Generate the S3 URL for the uploaded image
        s3_url = f"https://{DB.bucket_name}.s3.amazonaws.com/{filename}"

    except NoCredentialsError as e:
        print("Credentials not available")
        # Handle the case where credentials are not available or incorrect
        raise e
    except Exception as e:
        print(f"Error uploading image to S3: {e}")
        # Handle other exceptions

    finally:
        temp_file.close()

    return s3_url
