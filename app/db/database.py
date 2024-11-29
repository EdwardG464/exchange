from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base

from app.core.config import settings


DATABASE_URL = settings.get_database_url

engine = create_engine(DATABASE_URL, echo=True)

sync_session_maker = sessionmaker(engine, autoflush=False, autocommit=False)

Base = declarative_base()


def get_db() -> Session:
    session = sync_session_maker()
    try:
        yield session
    finally:
        session.close()