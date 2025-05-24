from typing import Optional
import asyncpg
from app.database.database import Database


class UserNotFoundError(Exception):
    """Exception raised when user is not found"""
    pass


async def get_user_by_email_service(email: str) -> asyncpg.Record:
    """
    Service function to get a user by their email address
    
    Args:
        email: User's email address
        
    Returns:
        asyncpg.Record: The user record
        
    Raises:
        UserNotFoundError: If user with this email is not found
    """
    user = await Database.fetchrow(
        "SELECT id, email, name, created_at, updated_at FROM users WHERE email = $1", 
        email
    )
    
    if not user:
        raise UserNotFoundError(f"User with email {email} not found")
    
    return user 