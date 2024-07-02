from fastapi import Depends
from pydantic import BaseModel

from app.dependencies import get_db
from app.models.embedding import Embedding
from app.service.embed import embed_text, get_embeddings
from app.service.query import answer_query
from . import router
from sqlalchemy.orm import Session
from typing_extensions import Self


@router.get("/")
def read_root():
    return {"Hello": "World"}


class QueryInput(BaseModel):
    query: str


class QueryOutput(BaseModel):
    response: str


@router.post("/query")
async def ep_post_query(
    embed: QueryInput, session: Session = Depends(get_db)
) -> QueryOutput:
    # TODO: Implement embedding logic
    embedding = answer_query(embed.query, session)
    return QueryOutput(response=embedding)
