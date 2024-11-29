
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool


TEST_DATABASE_URL = "sqlite://"

engine = create_engine(url=TEST_DATABASE_URL,
                       poolclass=StaticPool,
                       connect_args={"check_same_thread": False})

test_session_maker = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def override_get_db() -> Session:
    session = test_session_maker()
    try:
        yield session
    finally:
        session.close()
