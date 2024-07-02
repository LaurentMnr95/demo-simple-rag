from app.extensions.database.models import BaseSQLAlchemyModel
import sqlalchemy as sa
import pgvector.sqlalchemy as pgsa
from sqlalchemy.orm import Mapped, mapped_column


class Example(BaseSQLAlchemyModel):
    __tablename__ = "example"
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(sa.String, nullable=False)
