# db.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .database.models import BaseSQLAlchemyModel as BaseModel  # noqa
from app.config import env_config

engine = create_engine(
    env_config["SQLALCHEMY_DATABASE_URI_ADMIN"],  # type:ignore
)
DbSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
