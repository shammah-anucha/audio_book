from backend.app.app.tests.endpoints.test_crud_user import client
import pytest
from unittest.mock import MagicMock
import io
from fastapi import UploadFile
from sqlalchemy.orm import Session


from unittest.mock import Mock

# Create a mock PDF file
mock_pdf = MagicMock()

import io
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from starlette.datastructures import UploadFile
from backend.app.app.main import app


# Fixture to create a test client

pdf_content = b"Mock PDF Content"


# Test function for the create_Book endpoint
# def test_create_Book():
#     pdf_path = "/Users/shammahanucha/Documents/Apps/audio book/backend/app/app/api/api_v1/endpoints/The-Frog-Prince-Landscape-Book-CKF-FKB.pdf"

#     # Path to a sample PDF file for testing

#     response = client.post(
#         "/api/v1/uploadbook",
#         data={"user_id": 1},
#         files={"file": (pdf_content)},
#     )

#     # Assert that the response status code is 200
#     assert response.status_code == 200

# Optionally, you can check the response content or JSON
# content = response.json()
# assert "some_expected_value" in content


# def test_create_Book():
#     pdf_file = MagicMock()

#     response = client.post(
#         "/api/v1/Books/uploadbook", data={"user_id": 1}, files={"file": pdf_file}
#     )

#     # Assert that the response status code is 200
#     assert response.status_code == 200


# # Assert that the response JSON matches the expected format
# result = response.json()
# assert "book_id" in result
# assert result["user_id"] == 1
# assert result["book_name"] == "test.pdf"
# assert result["book_file"] == "mocked_s3_url"


# Run the test using pytest
# pytest -v test_file.py


# # Add a custom attribute to represent the name of the PDF
# mock_pdf.name = "example.pdf"
# def test_create_book():
#     # Mock the database session to avoid actual database interaction

#     # Create a mock PDF file for testing
#     pdf_content = b"Mock PDF Content"
#     pdf_file = UploadFile(filename="test.pdf", file=io.BytesIO(pdf_content))

#     # Perform the request to the endpoint
#     response = client.post(
#         "/api/v1/uploadbook",
#         data={"user_id": 1},
#         files={"file": ("test.pdf", pdf_file)},
#     )
#     print(response)
# Assert that the response status code is 200
# assert response.status_code == 200
# assert response.json() == {
#     "book_id": 1,
#     "book_name": "test.pdf",
#     "book_file": "https://myaudiobookapp.s3.amazonaws.com/test.pdf",
# }


# def test_create_book():
#     response = client.post("/api/v1/Book/uploadbook", json=book_db)
#     assert response.status_code == 200, response.text
# data = response.json()
# assert "user_id" in data


# def test_create_book():

#     # Create a mock PDF file for testing
#     pdf_content = b"Mock PDF Content"
#     pdf_file = UploadFile(filename="test.pdf", file=io.BytesIO(pdf_content))

#     book_db = {
#         # "book_id": 1,
#         "user_id": 1,
#         # "book_file": "https://myaudiobookapp.s3.amazonaws.com/test.pdf",
#     }

#     # Perform the request to the endpoint
#     response = client.post("/api/v1/Books/uploadbook", data=book_db, files=pdf_file)

#     # Assert that the response status code is 200
#     assert response.status_code == 200


# def test_read_user():
#     user_id = 1  # Replace with the actual user ID you want to retrieve

#     response = client.get(f"/api/v1/users/{user_id}")
#     assert response.status_code == 200, response.text
#     data = response.json()
#     assert data["user_id"] == user_id


# @pytest.mark.parametrize(
#     "params, expected_length",
#     [
#         ("/api/v1/users/", None),  # No parameters, expect a list
#         ("/api/v1/users/?skip=1&limit=5", 5),  # Skip and limit parameters
#         (
#             "/api/v1/users/?skip=-1&limit=0",
#             0,
#         ),  # Invalid parameters, expect an empty list
#         (
#             "/api/v1/users/?limit=1000",
#             1000,
#         ),  # Large limit, expect a list with length <= 1000
#     ],
# )
# def test_read_users(params, expected_length):
#     response = client.get(params)
#     assert response.status_code == 200, response.text
#     data = response.json()
#     assert isinstance(data, list)
#     if expected_length is not None:
#         assert len(data) <= expected_length


# @pytest.mark.parametrize(
#     "user_id, status_code, detail",
#     [
#         (1, 200, "Delete Successful"),  # Valid user ID, expect successful deletion
#         (999, 404, "User not found"),  # Invalid user ID, expect 404 error
#     ],
# )
# def test_delete_user(user_id, status_code, detail):
#     response = client.delete(f"/api/v1/users/{user_id}")
#     assert response.status_code == status_code, response.text
#     data = response.json()
#     if status_code == 200:
#         assert data == detail
#     else:
#         assert data["detail"] == detail


# def test_upload_file():
#     test_file = "The-Frog-Prince-Landscape-Book-CKF-FKB.pdf"
#     data = {"user_id": 1}
#     files = {
#         "file": UploadFile(
#             filename="The-Frog-Prince-Landscape-Book-CKF-FKB.pdf",
#             file=io.BytesIO(pdf_content),
#         ),
#     }
#     response = client.post("/api/v1/Books/uploadbook", data=data, files=files)
#     assert response.status_code == 200, response.text


def test_create_book():
    # Mock the database session to avoid actual database interaction
    mock_pdf = MagicMock(name="The-Frog-Prince-Landscape-Book-CKF-FKB.pdf")
    mock_pdf.name = "The-Frog-Prince-Landscape-Book-CKF-FKB.pdf"

    # Perform the request to the endpoint
    response = client.post(
        f"/api/v1/Books/uploadbook/",  # Assuming user_id is NOT a path parameter
        data={"user_id": 1},
        files={
            "file": (
                "The-Frog-Prince-Landscape-Book-CKF-FKB.pdf",
                open(mock_pdf.name, "rb"),
                "application/pdf",
            )
        },
    )

    # Assert that the response status code is 200
    assert response.status_code == 200
