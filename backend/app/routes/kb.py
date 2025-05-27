from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from app.helpers.jwt_helper import verify_jwt
from app.database.database import Database
from app.ai.qa_agent import qa_agent, AnswerOutputFormat
from app.service.get_kb import get_kb

router = APIRouter(prefix="/kb", tags=["kb"])


class QuestionRequest(BaseModel):
    question: str


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
    # Get Authorization header
    authorization = request.headers.get("Authorization")

    if not authorization:
        raise HTTPException(status_code=400, detail="Authorization header is required")

    # Check if it starts with "Bearer "
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=400, detail="Authorization header must start with 'Bearer '")

    # Extract the token (remove "Bearer " prefix)
    session_token = authorization[7:]  # Remove "Bearer " (7 characters)

    if not session_token:
        raise HTTPException(status_code=400, detail="Token is required")

    # Verify JWT token
    payload = verify_jwt(session_token)

    if payload is None:
        raise HTTPException(status_code=400, detail="Invalid or expired session_token")

    return payload


@router.get("/")
async def get_kb_list(request: Request):
    """
    Get list of all emails for the authenticated user.
    Returns only id, subject, and created_at columns.
    """
    # Validate session token
    payload = validate_session_token(request)

    # Get user_id from JWT payload
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=400, detail="user_id not found in token")

    try:
        # Query emails table for the specific user
        query = """
            SELECT id, subject, created_at 
            FROM emails 
            WHERE user_id = $1 
            ORDER BY created_at DESC
        """
        emails = await Database.fetch(query, user_id)

        # Convert records to list of dictionaries
        email_list = []
        for email in emails:
            email_list.append(
                {
                    "id": str(email["id"]),
                    "subject": email["subject"],
                    "created_at": (
                        email["created_at"].isoformat() if email["created_at"] else None
                    ),
                }
            )

        return {"emails": email_list}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.get("/{kb_id}")
async def get_kb_by_id(request: Request, kb_id: str):
    """
    Get a specific email by ID for the authenticated user.
    Returns all fields from the email record.
    """
    # Validate session token
    payload = validate_session_token(request)

    # Get user_id from JWT payload
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=400, detail="user_id not found in token")

    try:
        # Query emails table for the specific email and user
        query = """
            SELECT id, user_id, subject, content_html, content_text, created_at
            FROM emails 
            WHERE id = $1 AND user_id = $2
        """
        email = await Database.fetchrow(query, kb_id, user_id)

        if not email:
            raise HTTPException(status_code=404, detail="Email not found")

        # Convert record to dictionary
        email_data = {
            "id": str(email["id"]),
            "user_id": str(email["user_id"]),
            "subject": email["subject"],
            "content_html": email["content_html"],
            "content_text": email["content_text"],
            "created_at": (
                email["created_at"].isoformat() if email["created_at"] else None
            ),
        }

        return email_data

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.post("/qa")
async def qa_kb(request: Request, question_request: QuestionRequest):
    """
    RAG based question answering
    """
    # Validate session token
    payload = validate_session_token(request)

    # Get user_id from JWT payload
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=400, detail="user_id not found in token")

    try:
        question: str = question_request.question
        knowledgebase: str = await get_kb(question, str(user_id))
        answer: AnswerOutputFormat = await qa_agent(question, knowledgebase)

        return {
            "answer": answer.answer,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"QA processing error: {str(e)}")
