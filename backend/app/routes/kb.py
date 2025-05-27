from fastapi import APIRouter, Request, HTTPException
from app.helpers.jwt_helper import verify_jwt

router = APIRouter(prefix="/kb", tags=["kb"])


def validate_session_token(request: Request):
    """
    Helper function to validate session_token from request headers

    Args:
        request (Request): FastAPI request object

    Returns:
        dict: JWT payload if valid

    Raises:
        HTTPException: 400 if token is missing or invalid
    """
    # Get session_token from headers
    session_token = request.headers.get("session_token")

    if not session_token:
        raise HTTPException(status_code=400, detail="session_token header is required")

    # Verify JWT token
    payload = verify_jwt(session_token)

    if payload is None:
        raise HTTPException(status_code=400, detail="Invalid or expired session_token")

    return payload


@router.get("/")
async def get_kb_list(request: Request):
    # Validate session token
    payload = validate_session_token(request)

    # If token is valid, return hello world
    return {"message": "hello world", "user_email": payload.get("email")}


@router.get("/{kb_id}")
async def get_kb_by_id(request: Request, kb_id: str):
    # Validate session token
    payload = validate_session_token(request)

    # If token is valid, return hello world
    return {"message": "hello world", "user_email": payload.get("email")}
