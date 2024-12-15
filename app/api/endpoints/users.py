from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.schemas.user import UserCreate, UserFromDB
from app.core.security import get_user_from_token
from app.db.database import get_async_session
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from sqlalchemy.orm import Session


user_router = APIRouter(prefix="/auth", tags=['User'])



@user_router.post("/register")
async def create_new_user(user: UserCreate, db: AsyncSession = Depends(get_async_session)):
    await UserService(UserRepository(db)).add_user(user)
    return {"message": "User successfully created"}


@user_router.post("/login")
async def login(user_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: AsyncSession = Depends(get_async_session)):
    jwt = await UserService(UserRepository(db)).get_jwt(user_data)
    return {"access_token": jwt, "token_type": "bearer"}


@user_router.get("/about_me", response_model=UserFromDB)
async def about_me(sub: str = Depends(get_user_from_token), db: AsyncSession = Depends(get_async_session)):
    user_db = await UserService(UserRepository(db)).get_user({"username": sub})
    return user_db