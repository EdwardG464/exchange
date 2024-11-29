from abc import abstractmethod, ABC
from sqlalchemy import select, insert
from sqlalchemy.orm import Session


class AbstractRepository(ABC):
    @abstractmethod
    def add_one(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    def get_one(self, filters: dict):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: Session):
        self.session = session

    def add_one(self, data: dict):
        stmt = insert(self.model).values(**data).returning(self.model)
        res = self.session.execute(stmt).scalar()
        self.session.commit()
        return res

    def get_one(self, filters: dict):
        stmt = select(self.model).filter_by(**filters)
        res = self.session.execute(stmt).scalar()
        return res