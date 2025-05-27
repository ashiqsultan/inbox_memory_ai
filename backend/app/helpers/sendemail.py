import requests
import os
from typing import Optional


POSTMARK_API_URL = "https://api.postmarkapp.com/email"
POSTMARK_SERVER_TOKEN: str = os.getenv("POSTMARK_SERVER_TOKEN", "")


def sendemail(
    to_email: str,
    subject: str,
    html_body: str,
) -> None:
    """
    Send email using Postmark API

    Args:
        to_email (str): Recipient email address
        subject (str): Email subject
        html_body (str): HTML content of the email

    Raises:
        Exception: If the API request fails
    """
    from_email: str = "support@kbhelper.com"
    message_stream: str = "outbound"

    headers: dict[str, str] = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-Postmark-Server-Token": POSTMARK_SERVER_TOKEN,
    }

    payload: dict[str, str] = {
        "From": from_email,
        "To": to_email,
        "Subject": subject,
        "HtmlBody": html_body,
        "MessageStream": message_stream,
    }

    response = requests.post(
        POSTMARK_API_URL, headers=headers, json=payload, verify=False
    )

    if response.status_code != 200:
        raise Exception(f"Failed to send email: {response.text}")


if __name__ == "__main__":
    # Test HTML content
    email_content = """
    <html>
        <body>
            <h1>Test Email from Inbox Memory AI</h1>
            <p>This is a test email sent using the Postmark API.</p>
            <p>If you received this email, the email service is working correctly!</p>
        </body>
    </html>
    """

    try:
        sendemail(
            to_email="ashiqdrive@gmail.com",
            subject="Inbox Memory AI - Email Test",
            html_body=email_content,
        )
        print("Test email sent successfully!")
    except Exception as e:
        print(f"Failed to send test email: {str(e)}")
