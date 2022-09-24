from typing import Any, List
from pydantic import EmailStr

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from ...app.models.users import Users


class CRUDEmail(EmailStr):
    def get_available_emails(self, db: Session) -> List[EmailStr]:
        emails = []
        for email in db.query(Users.email).filter(Users.unavailabilities == None).all():
            email = "\n".join(list(email))
            emails.append(email)
        return emails


crud_email = CRUDEmail(EmailStr)