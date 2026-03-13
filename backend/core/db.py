from typing import Generator

from sqlmodel import create_engine, Session, SQLModel

from core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    echo=False,
    connect_args=
    {"check_same_thread": False}
    if settings.DATABASE_URL.startswith("sqlite")
    else {}
)


def init_db() -> None:
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
