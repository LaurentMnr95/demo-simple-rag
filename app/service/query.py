from fastapi import openapi
import openai
from openai.types.create_embedding_response import CreateEmbeddingResponse
from sqlalchemy import select

from app.models.embedding import Embedding
from sqlalchemy.orm import Session


def _build_answer_prompt(query: str, context: list[str]) -> str:
    context_str = "\n\n".join(context)
    query_answer_prompt = f"""
    You are a helpful assistant that provides information about the given query.
    The query is:  {query}
    You are given the following contexts to answer the query:
    {context_str}
    Answer the query only if the context is relevant to the query. Do not mention the context if it is not relevant.
    """
    return query_answer_prompt


def _build_hypothetical_answer(query: str) -> str:
    query_answer_prompt = f"""
    You are a helpful assistant that provides information about the given query.
    The query is:  {query}
    You have to give an hypothetical answer to the query. We don't matter if the answer is correct or not. Just give an answer.
    Your answer:"""
    return query_answer_prompt


def answer_query(query: str, secssion: Session) -> str:
    # TODO: Implement embedding logic
    client = openai.OpenAI(api_key="xxx")

    hyp_answer_prompt = _build_hypothetical_answer(query)
    output_completion_hyp = client.chat.completions.create(
        messages=[{"role": "system", "content": hyp_answer_prompt}],
        model="gpt-3.5-turbo",
        temperature=0.5,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
    )
    hyp_answer = output_completion_hyp.choices[0].message.content
    print(hyp_answer)
    if not hyp_answer:
        return "Sorry, I could not answer the query."
    output: CreateEmbeddingResponse = client.embeddings.create(
        input=hyp_answer, model="text-embedding-3-small"
    )
    embedding_value = output.data[0].embedding
    query_select = (
        select(Embedding)
        .order_by(Embedding.embedding.l2_distance(embedding_value))
        .limit(10)
    )
    embeddings = session.scalars(query_select).all()
    context = [embedding.content for embedding in embeddings]
    print(context)
    prompt = _build_answer_prompt(query, context)
    print(prompt)
    output_completion = client.chat.completions.create(
        messages=[{"role": "system", "content": prompt}],
        model="gpt-3.5-turbo",
        temperature=0.5,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
    )
    return output_completion.choices[0].message.content  # noqa
