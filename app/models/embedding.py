from app.extensions.database.models import BaseSQLAlchemyModel
import sqlalchemy as sa
import pgvector.sqlalchemy as pgsa
from sqlalchemy.orm import Mapped, mapped_column


class Embedding(BaseSQLAlchemyModel):
    __tablename__ = "embedding"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, autoincrement=True)
    embedding: Mapped[list[float]] = mapped_column(pgsa.Vector(1536), nullable=False)
    content: Mapped[str] = mapped_column(sa.String, nullable=False)
