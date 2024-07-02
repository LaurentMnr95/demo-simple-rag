# models.py
from typing import Optional

import sqlalchemy as sa
from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql.expression import text

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


base_metadata = MetaData(naming_convention=convention)


class BaseSQLAlchemyModel(DeclarativeBase):
    metadata = base_metadata
