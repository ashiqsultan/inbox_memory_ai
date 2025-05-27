import jwt
from datetime import datetime, timedelta
from typing import Optional
import os

# JWT configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", None)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  #  1 day


def generate_jwt(email: str) -> str:
    """
    Generate a JWT token with email in the payload

    Args:
        email (str): User's email address

    Returns:
        str: JWT token
    """
    # Create payload
    payload = {
        "email": email,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        "iat": datetime.utcnow(),
        "type": "access_token",
    }

    # Generate token
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_jwt(token: str) -> Optional[dict]:
    """
    Verify and decode a JWT token

    Args:
        token (str): JWT token to verify

    Returns:
        Optional[dict]: Decoded payload if valid, None if invalid
    """
    try:
        # Decode and verify token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        # Token has expired
        return None
    except jwt.InvalidTokenError:
        # Token is invalid
        return None
