import logging
from fastapi import APIRouter, Depends
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
from typing import Optional, List
from . import crud_book
from . import crud_audio
from backend.app.app.api import deps
from sqlalchemy.orm import Session
from ..models import models
import json


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
    

def save_audio_to_s3(book_id: int, file_name: str, db: Session):
    s3_url = []
    
    try:
        # Convert text to audio
        text_list = crud_book.Book.extract_text_from_pdf_in_db(book_id=book_id, db=db)
        audio_streams = crud_audio.Audio.create_audio_stream(text_list)
        user_id = db.query(models.Books.user_id).filter(models.Books.book_id == book_id).first()[0]

        # Upload the audio file to S3 with the specified file name
        s3 = boto3.client('s3', aws_access_key_id=DB.aws_access_key_id, aws_secret_access_key=DB.aws_secret_access_key, region_name=DB.region)
        for i, audio_stream in enumerate(audio_streams, start=1):
            part_file_name = f"{file_name}_part{i}.mp3"

            # Reset the position of BytesIO to the beginning
            audio_stream.seek(0)


            s3.upload_fileobj(audio_stream, DB.bucket_name, part_file_name)
            # Generate the S3 URL
            url = f'https://{DB.bucket_name}.s3.amazonaws.com/{part_file_name}'
            s3_url.append(url)

        audio_file_str = json.dumps(s3_url)
        db_file = models.Audio(user_id=user_id, book_id=book_id, audio_file=audio_file_str)
        print(db_file)
        db.add(db_file)
        db.commit()
        db.refresh(db_file)

        return s3_url

    except NoCredentialsError as e:
        print("Credentials not available.")
        raise e
    except Exception as e:
        print(f"Error uploading to S3: {e}")
        raise e




def delete_audio_from_s3(audio_id: int, db: Session):
    s3_url = db.query(models.Audio.audio_file).filter(models.Audio.audio_id == audio_id).first()
    parts = s3_url.replace("https://", "").split("/")
    object_key = "/".join(parts[1:])
    try:
        # Create an S3 client
        s3 = boto3.client(
            's3',
            aws_access_key_id=DB.aws_access_key_id,
            aws_secret_access_key=DB.aws_secret_access_key,
            region_name=DB.region
        )

        # Delete the object
        s3.delete_object(Bucket=DB.bucket_name, Key=object_key)
        print(f"Object '{object_key}' deleted from S3 bucket '{DB.bucket_name}'.")

    except NoCredentialsError as e:
        print("Credentials not available.")
        raise e
    except Exception as e:
        print(f"Error deleting object from S3: {e}")
        raise e


def delete_book_from_s3(book_id: int, db: Session):
    s3_url = db.query(models.Books.book_file).filter(models.Books.book_id == book_id).first()[0]
    print(s3_url)
    parts = s3_url.replace("https://", "").split("/")
    object_key = "/".join(parts[1:])
    try:
        # Create an S3 client
        s3 = boto3.client(
            's3',
            aws_access_key_id=DB.aws_access_key_id,
            aws_secret_access_key=DB.aws_secret_access_key,
            region_name=DB.region
        )

        # Delete the object
        s3.delete_object(Bucket=DB.bucket_name, Key=object_key)
        print(f"Object '{object_key}' deleted from S3 bucket '{DB.bucket_name}'.")

    except NoCredentialsError as e:
        print("Credentials not available.")
        raise e
    except Exception as e:
        print(f"Error deleting object from S3: {e}")
        raise e


