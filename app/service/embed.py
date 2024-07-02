from fastapi import openapi
import openai
from openai.types.create_embedding_response import CreateEmbeddingResponse
from sqlalchemy import select

from app.models.embedding import Embedding
from sqlalchemy.orm import Session


def embed_text(embed: str, session: Session) -> Embedding:
    # TODO: Implement embedding logic
    client = openai.OpenAI(api_key="xxxx")

    output: CreateEmbeddingResponse = client.embeddings.create(
        input=embed, model="text-embedding-3-small"
    )
    embedding_value = output.data[0].embedding

    embedding = Embedding(embedding=embedding_value, content=embed)
    session.add(embedding)
    session.commit()
    session.refresh(embedding)
    return embedding


def get_embeddings(session: Session) -> list[Embedding]:
    # TODO: Implement embedding logic
    return list(session.scalars(select(Embedding)).all())
