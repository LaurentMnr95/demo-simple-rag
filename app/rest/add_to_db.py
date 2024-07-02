from fastapi import Depends
from pydantic import BaseModel

from app.dependencies import get_db
from app.models.embedding import Embedding
from app.service.embed import embed_text, get_embeddings
from . import router
from sqlalchemy.orm import Session
from typing_extensions import Self


@router.get("/")
def read_root():
    return {"Hello": "World"}


class EmbeddingInput(BaseModel):
    text: str


class EmbeddingOutput(BaseModel):
    id: int
    embedding: list[float]
    content: str

    @classmethod
    def from_embedding(cls, embedding: Embedding) -> Self:
        return cls(
            id=embedding.id,
            embedding=embedding.embedding,
            content=embedding.content,
        )


@router.post("/embeds")
async def ep_embed_string(embed: EmbeddingInput, session: Session = Depends(get_db)):
    # TODO: Implement embedding logic
    embedding = embed_text(embed.text, session)
    return EmbeddingOutput.from_embedding(embedding)


@router.get("/embeds")
async def ep_get_embeddings(session: Session = Depends(get_db)):
    embedding_service_output = get_embeddings(session)
    return [EmbeddingOutput.from_embedding(embed) for embed in embedding_service_output]
