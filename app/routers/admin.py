from fastapi import APIRouter, Depends, HTTPException, Path, status
from app.models import Todos, Users
from app.database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from app.routers.auth import get_current_user
from app.database import get_db


router = APIRouter(
    prefix='/admin',
    tags=['admin']
)


db_dependancy = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]



def authenticate_as_admin(user):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    if user.get("user_role") != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

@router.get("/todo", status_code=status.HTTP_200_OK)
def read_all_todos(user: user_dependency, db: db_dependancy):
    authenticate_as_admin(user)
    return db.query(Todos).all()


@router.get("/users", status_code=status.HTTP_200_OK)
def read_all_users(user: user_dependency, db: db_dependancy):
    authenticate_as_admin(user)
    return db.query(Users).all()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(user: user_dependency, db: db_dependancy, todo_id: int = Path(gt=0)):
    authenticate_as_admin(user)
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found.')
    db.query(Todos).filter(Todos.id == todo_id).delete()

    db.commit()


@router.delete("/user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user: user_dependency, db: db_dependancy, user_id: int = Path(gt=0)):
    authenticate_as_admin(user)
    
    user_model = db.query(Users).filter(Users.id == user_id).first()

    if user_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid user ID.")
    
    db.delete(user_model)
    db.commit()