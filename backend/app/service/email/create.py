from typing import Optional
from app.database.database import Database


class UserNotFoundError(Exception):
    """Exception raised when the specified user does not exist"""
    pass


async def create_email(
    user_id: str,
    subject: str,
    content_text: str,
    content_html: Optional[str],
    is_forwarded: bool = False,
) -> bool:
    try:
        # Check if user exists
        existing_user = await Database.fetchrow(
            "SELECT id FROM users WHERE id = $1", user_id
        )

        if not existing_user:
            raise UserNotFoundError("User with this ID does not exist")

        # Create new email
        await Database.execute(
            """
            INSERT INTO emails (user_id, subject, content_html, content_text, is_forwarded)
            VALUES ($1, $2, $3, $4, $5)
            """,
            user_id,
            subject,
            content_html,
            content_text,
            is_forwarded,
        )

        return True
    except Exception as e:
        print(f"Failed to create email: {e}")
        raise e
