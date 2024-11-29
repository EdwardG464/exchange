from pydantic import BaseModel, ConfigDict
from datetime import datetime


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str


class UserCreate(UserBase):
    password: str


class UserFromDB(UserBase):
    id: int
    created_at: datetime