import logging
import boto3
from botocore.exceptions import ClientError
import os
from io import BytesIO
from boto3.session import Session as Boto3Session
import boto3
from botocore.exceptions import NoCredentialsError
from fastapi import UploadFile, HTTPException
from dotenv import load_dotenv
import os

load_dotenv(".env")



class DB:
    aws_access_key_id = os.getenv("aws_access_key_id")
    aws_secret_access_key = os.getenv("aws_secret_access_key")
    region = os.getenv("region")
    bucket_name = os.getenv("bucket_name")

# print(DB.aws_access_key_id)
# print(DB.aws_secret_access_key)
# print(DB.bucket_name)
# print(DB.region)




def upload_to_s3(file: UploadFile):
        s3_url = None  # Initialize with a default value
        try:
            s3 = boto3.client(
                's3',
                aws_access_key_id=DB.aws_access_key_id,
                aws_secret_access_key=DB.aws_secret_access_key,
                region_name=DB.region
            )
            
            # Upload the file
            s3.upload_fileobj(file.file, DB.bucket_name, file.filename)
            

            # Generate the S3 URL
            s3_url = f'https://{DB.bucket_name}.s3.amazonaws.com/{file.filename}'

        except NoCredentialsError as e:
            print("Credentials not available")
            # Handle the case where credentials are not available or incorrect
            raise e
        except Exception as e:
            print(f"Error uploading to S3: {e}")
            # Handle other exceptions

        return s3_url


def download_from_s3(s3_url: str):
    # Parse the S3 URL to extract bucket name and object key
    parts = s3_url.replace("https://", "").split("/")
    object_key = "/".join(parts[1:])

    # Download the file from S3
    try:
        s3 = boto3.client(
                's3',
                aws_access_key_id=DB.aws_access_key_id,
                aws_secret_access_key=DB.aws_secret_access_key,
                region_name=DB.region
            )
        response = s3.get_object(Bucket=DB.bucket_name, Key=object_key)
        content = response["Body"].read()
        return BytesIO(content)
    except NoCredentialsError as e:
        print("Credentials not available.")
        raise e
    except Exception as e:
        print(f"Error downloading from S3: {e}")
        raise e
