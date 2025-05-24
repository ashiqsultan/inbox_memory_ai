from typing import Optional
import asyncpg
from app.database.database import Database


class UserNotFoundError(Exception):
    """Exception raised when user is not found"""
    pass


async def get_user_by_id_service(user_id: str) -> asyncpg.Record:
    """
    Service function to get a user by their ID
    
    Args:
        user_id: User's UUID
        
    Returns:
        asyncpg.Record: The user record
        
    Raises:
        UserNotFoundError: If user with this ID is not found
    """
    user = await Database.fetchrow(
        "SELECT id, email, name, created_at, updated_at FROM users WHERE id = $1", 
        user_id
    )
    
    if not user:
        raise UserNotFoundError(f"User with ID {user_id} not found")
    
    return user 