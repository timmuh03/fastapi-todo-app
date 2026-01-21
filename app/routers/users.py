from fastapi import APIRouter, Depends, HTTPException, Path, status
from pydantic import BaseModel, Field
from app.models import Users
from app.database import get_db
from typing import Annotated
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.routers.auth import get_current_user



router = APIRouter(
    prefix='/user',
    tags=['user']
)


db_dependancy = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')



class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)



def authenticate_user(user):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed.")

@router.get("/", status_code=status.HTTP_200_OK)
def get_user(db: db_dependancy, user: user_dependency):
    authenticate_user(user)
    
    return db.query(Users).filter(Users.id == user.get('id')).first()


@router.put("/", status_code=status.HTTP_204_NO_CONTENT)
def change_password(db: db_dependancy, user: user_dependency, user_verification: UserVerification):
    authenticate_user(user)

    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Error on password change")
    
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    
    db.add(user_model)
    db.commit()


@router.put("/{phone_number}", status_code=status.HTTP_204_NO_CONTENT)
def update_phone_number(db: db_dependancy, user:user_dependency, phone_number: str):
    authenticate_user(user)
    
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    user_model.phone_number = phone_number

    db.add(user_model)
    db.commit()