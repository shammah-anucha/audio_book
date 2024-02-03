# HOW TO GUIDE
Follow these steps to use the application.

## 1. Install poetry
Poetry is used to manage all project dependencies. Install the dependencies and devDependencies needed.

#### How to install:
```sh
pip install poetry
```
## 2. Activate poetry environment:

#### How to:
```
poetry shell
```

## 3. Install all project dependences

The dependencies are all the libraries and frameworks that the application needs to function properly.

#### How to install:
```
poetry install
```

## 4. Run the uvicorn server with:

```
poetry run uvicorn backend.app.app.main:app --reload
```

## 5.  Connect to the fastapi docs:

This is an interactive API docs to test the endpoints of your Get, Post, Push and Delete on your localhost.

#### How to connect:
On your browser, connect to the url:

http://127.0.0.1:8000/docs#/

## 6. Using the class DB in the s3 module:

 Please ask the admin for the access.

## 7. Connecting to the AWS database:

Please ask the admin for the config.py file

## 8. Migrating to the database using alembic.

To migrate with alembic, use the following command:

```
alembic revision --autogenerate -m "initial"
alembic upgrade head
```