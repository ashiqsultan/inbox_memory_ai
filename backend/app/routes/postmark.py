from fastapi import APIRouter, Request, BackgroundTasks, HTTPException
import json
from app.service.email.create import create_email
from app.service.get_user_by_email import get_user_by_email
from app.ai.classify_email import classify_email, OutputFormat
from typing import Any
from app.helpers.remove_links import remove_links
from app.background_jobs.email_processor import add_email_processing_task
from app.ai.qa_agent import qa_agent, AnswerOutputFormat
from app.service.get_kb import get_kb
from app.helpers.sendemail import sendemail
from app.helpers.generate_qa_email_html import generate_qa_email_html
from app.helpers.send_welcome_email import send_welcome_email


router: APIRouter = APIRouter()


@router.post("/postmark")
async def handle_postmark_webhook(
    request: Request, background_tasks: BackgroundTasks
) -> Any:
    """Handle inbound email webhooks from Postmark"""
    try:

        json_data: Any = await request.json()

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

        user_data = await get_user_by_email(sender_email)

        if not user_data:
            print(f"New user detected: {sender_email}")
            send_welcome_email(sender_email)
            return {"message": "Welcome email sent to new user"}

        user_id = user_data["id"]

        text_body_without_links: str = remove_links(text_body)

        text_first_500_chars: str = text_body_without_links[:500]

        classify_answer: OutputFormat = await classify_email(text_first_500_chars)

        if classify_answer.action == "SAVE":
            email_ref_id = await create_email(
                user_id, email_subject, text_body, html_body, is_forwarded=False
            )

            add_email_processing_task(
                background_tasks,
                user_id,
                email_ref_id,
                str(email_subject),
                str(text_body_without_links),
            )
            print("Background task started for subject: ", email_subject)
            return {"message": "Okay"}
        elif classify_answer.action == "QA":
            question: str = text_body
            knowledgebase: str = await get_kb(question, str(user_id))
            answer: AnswerOutputFormat = await qa_agent(text_body, knowledgebase)
            answer_html: str = generate_qa_email_html(question, answer)
            truncated_question = question[:50] + ("..." if len(question) > 50 else "")
            answer_email_subject: str = f"Inbox Memory AI Answer: {truncated_question}"
            sendemail(sender_email, answer_email_subject, answer_html)
            return {"message": "Okay"}

        raise HTTPException(status_code=500, detail="Something went wrong")

    except Exception as e:
        print(f"Error processing Postmark webhook")
        print(e)
        return {"status": "error", "message": "Failed to process email"}
