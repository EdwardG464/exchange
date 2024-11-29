from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.schemas.user import UserCreate, UserFromDB
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.core.security import get_user_from_token
from app.db.database import get_db

user_router = APIRouter(prefix="/auth", tags=['User'])


@user_router.post('/register/')
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    UserService(UserRepository(db)).add_user(user)
    return {"message": "User successfully created"}


@user_router.post('/login/')
def login(user_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    jwt = UserService(UserRepository(db)).get_jwt(user_data)
    return {"access_token": jwt, "token_type": "bearer"}


@user_router.get('/about_me/', response_model=UserFromDB)
def about_me(sub: str = Depends(get_user_from_token), db: Session = Depends(get_db)):
    user_db = UserService(UserRepository(db)).get_user({"username": sub})
    return user_db