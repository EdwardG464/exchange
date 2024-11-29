from app.db.models import User
from .base_repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    model = User