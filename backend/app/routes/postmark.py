from fastapi import APIRouter, Request
import json
from app.service.email.create import create_email
from app.service.get_user_by_email import get_user_by_email


router = APIRouter()


@router.post("/postmark")
async def handle_postmark_webhook(request: Request):
    """Handle inbound email webhooks from Postmark"""
    try:

        json_data = await request.json()

        print("=== Postmark Inbound Email Data ===")
        print(json.dumps(json_data, indent=2))
        print("=== End Postmark Data ===")

        sender_email = json_data.get("From", None)
        if not sender_email:
            raise ValueError("Sender email not found")

        email_subject = json_data.get("Subject", None)
        if not email_subject:
            raise ValueError("Subject not found")

        text_body = json_data.get("TextBody", None)
        if not text_body:
            raise ValueError("Text body not found")

        html_body = json_data.get("HtmlBody", None)

        # is_forwarded = TODO Need to use LLM to determine is forwarded

        user_data = await get_user_by_email(sender_email)
        user_id = user_data["id"]

        await create_email(
            user_id, email_subject, text_body, html_body, is_forwarded=False
        )

        return {"status": "success", "message": "Email received and processed"}

    except Exception as e:
        print(f"Error processing Postmark webhook")
        print(e)
        return {"status": "error", "message": "Failed to process email"}
