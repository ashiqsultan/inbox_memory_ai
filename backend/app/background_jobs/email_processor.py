import asyncio
from fastapi import BackgroundTasks


async def process_email_background(
    user_id: int, email_subject: str, text_body: str
) -> None:
    """
    Background job function to process emails asynchronously.
    This function will run in the background without blocking the main request.
    """
    print("Hello world from background job!")
    print(f"Processing email for user {user_id}")
    print(f"Subject: {email_subject}")
    print(f"Body preview: {text_body[:100]}...")

    # Simulate some processing time
    await asyncio.sleep(2)

    print(f"Processing Completed")

    # TODO: Add actual email processing logic here:
    # 1. Chunk the Text ✂️
    # 2. Create a vector embedding for each text chunk
    # 3. Store the embedding in DB

    print(f"Background processing completed for user {user_id}")


def add_email_processing_task(
    background_tasks: BackgroundTasks, user_id: int, email_subject: str, text_body: str
) -> None:
    """
    Helper function to add the email processing task to FastAPI's background tasks.
    """
    background_tasks.add_task(
        process_email_background, user_id, email_subject, text_body
    )
