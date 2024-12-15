from abc import ABC, abstractmethod

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, data: dict):
        raise NotImplementedError


    @abstractmethod
    async def get_one(self, filters: dict):
        raise NotImplementedError


class Repository(AbstractRepository):
    model = None


    def __init__(self, session: AsyncSession):
        self.session = session


    async def add_one(self, data: dict):
        stmt = insert(self.model).values(**data).returning(self.model)
        res = await self.session.execute(stmt)
        self.session.commit()
        return res.scalar_one()


    async def get_one(self, filters: dict):
        stmt = select(self.model).filter_by(**filters)
        res = await self.session.execute(stmt)
        return res.scalar()