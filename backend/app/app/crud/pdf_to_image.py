from pdf2image import convert_from_bytes
from .s3.s3_image import upload_image_to_s3

from fastapi import UploadFile, HTTPException


def convert_pdf_to_image(file: UploadFile):

    pages = convert_from_bytes(file.file.read())
    first_page_image = pages[0]

    try:

        filename = file.filename + ".png"
        print(filename)

        #     # Upload the image to S3
        url = upload_image_to_s3(first_page_image, filename)

        return url

    except Exception as e:
        # Handle exceptions (e.g., file size exceeds limit)
        raise HTTPException(status_code=500, detail=f"Error saving file: {e}")
