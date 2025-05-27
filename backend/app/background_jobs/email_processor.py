import asyncio
import uuid
from uuid import UUID
from datetime import datetime
from fastapi import BackgroundTasks
from app.helpers.chunk_email_text import split_text_recursive
from app.gemini.get_embeddings import get_embeddings
from app.lance_db import TextEmbeddingSchema, add_record


async def process_email_background(
    user_id: UUID,
    email_ref_id: str,
    email_subject: str,
    text_body: str,
) -> None:
    """
    Background job function to process emails asynchronously.
    This function will run in the background without blocking the main request.
    """
    print("Hello world from background job!")
    print(f"Processing email for email_ref_id {email_ref_id}")
    print(f"Subject: {email_subject}")

    text_chunks = split_text_recursive(text_body)

    for index, chunk in enumerate(text_chunks):
        embedding = await get_embeddings(chunk)
        print(f"Embedding of index {index}: {embedding}")
        lance_item = TextEmbeddingSchema(
            id=str(uuid.uuid4()),
            email_ref_id=email_ref_id,
            vector=embedding,
            text=chunk,
            chunk_sequence=index,
            created_at=datetime.now(),
        )
        table_name = str(user_id)
        await add_record(table_name, [lance_item])
    print(f"Background processing completed for email {email_subject}")


def add_email_processing_task(
    background_tasks: BackgroundTasks,
    user_id: UUID,
    email_ref_id: str,
    email_subject: str,
    text_body: str,
) -> None:
    """
    Helper function to add the email processing task to FastAPI's background tasks.
    """
    background_tasks.add_task(
        process_email_background,
        user_id,
        email_ref_id,
        email_subject,
        text_body,
    )
