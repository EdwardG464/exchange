from app.db.models import User
from .base_repository import Repository


class UserRepository(Repository):
    model = User