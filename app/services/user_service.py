from fastapi import HTTPException
from passlib.hash import pbkdf2_sha256
from fastapi.security import OAuth2PasswordRequestForm

from app.repositories.base_repository import AbstractRepository
from app.api.schemas.user import UserCreate
from app.db.models import User
from app.core.security import create_jwt


class UserService:
    def __init__(self, user_repo: AbstractRepository):
        self.user_repo = user_repo

    def add_user(self, user: UserCreate) -> User:
        user_db = self.user_repo.get_one({"username": user.username})
        if user_db:
            raise HTTPException(status_code=400, detail="User with username already exists")
        user.password = pbkdf2_sha256.hash(user.password)
        new_user = self.user_repo.add_one(user.model_dump())
        return new_user

    def get_user(self, filters: dict) -> User | None:
        user_db = self.user_repo.get_one(filters)
        return user_db

    def get_jwt(self, user_data: OAuth2PasswordRequestForm) -> str:
        user_db: User = self.user_repo.get_one({"username": user_data.username})
        if user_db is None or not pbkdf2_sha256.verify(user_data.password, user_db.password):
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"})
        data_for_jwt = {"sub": user_db.username}
        return create_jwt(data_for_jwt)