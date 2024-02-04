import boto3
import os
from botocore.exceptions import NoCredentialsError
from fastapi import HTTPException
from dotenv import load_dotenv
from .. import crud_book
from .. import crud_audio
from sqlalchemy.orm import Session
from ...models import models
import json


load_dotenv(".env")





class DB:
    aws_access_key_id = os.getenv("aws_access_key_id")
    aws_secret_access_key = os.getenv("aws_secret_access_key")
    region = os.getenv("region")
    bucket_name = os.getenv("bucket_name")

s3 = boto3.client(
                's3',
                aws_access_key_id=DB.aws_access_key_id,
                aws_secret_access_key=DB.aws_secret_access_key,
                region_name=DB.region
            )



def save_audio_to_s3(book_id: int, file_name: str, db: Session):
    db_book = crud_book.Book.get_book_id(db=db, id=book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    s3_url = []
    
    try:
        # Convert text to audio
        text_list = crud_book.Book.extract_text_from_pdf_in_db(book_id=book_id, db=db)
        audio_streams = crud_audio.Audio.create_audio_stream(text_list)
        print(audio_streams)
        user_id = db.query(models.Books.user_id).filter(models.Books.book_id == book_id).first()[0]

        # Upload the audio file to S3 with the specified file name
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
    s3_url = db.query(models.Audio.audio_file).filter(models.Audio.audio_id == audio_id).first()[0]
    s3_url = json.loads(s3_url)
    # print(s3_url)
    
    
    for url in s3_url:
        # print(url)
        parts = url.replace("https://", "").split("/")
        object_key = "/".join(parts[1:])
        # print(parts)
        # print(object_key)
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





