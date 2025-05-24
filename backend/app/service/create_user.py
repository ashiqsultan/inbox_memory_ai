from typing import Optional
import asyncpg
from app.database.database import Database


class UserCreationError(Exception):
    """Exception raised when user creation fails"""
    pass


class UserAlreadyExistsError(Exception):
    """Exception raised when a user with the same email already exists"""
    pass


async def create_user_service(email: str, name: str) -> asyncpg.Record:
    """
    Service function to create a new user
    
    Args:
        email: User's email address
        name: User's name
        
    Returns:
        asyncpg.Record: The created user record
        
    Raises:
        UserAlreadyExistsError: If user with this email already exists
        UserCreationError: If user creation fails
    """
    # Check if user with this email already exists
    existing_user = await Database.fetchrow(
        "SELECT id FROM users WHERE email = $1", email
    )
    
    if existing_user:
        raise UserAlreadyExistsError("User with this email already exists")
    
    # Create new user
    created_user = await Database.execute_and_return(
        """
        INSERT INTO users (email, name)
        VALUES ($1, $2)
        RETURNING id, email, name, created_at, updated_at
        """,
        email,
        name,
    )
    
    if not created_user:
        raise UserCreationError("Failed to create user")
    
    return created_user
