from app.helpers.sendemail import sendemail


def send_otp_email(user_email: str, otp_code: str) -> None:
    """
    Sends an OTP (One-Time Password) email to users for verification.

    Args:
        user_email: The email address of the user
        otp_code: The six-digit OTP code to send
    """
    subject = "Your Inbox Memory AI Verification Code"

    otp_html: str = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
        <h1 style="color: #2c3e50;">Verification Code</h1>
        <p>Hi there!</p>
        <p>Here's your verification code for Inbox Memory AI:</p>
        
        <div style="background-color: #f8f9fa; border: 2px solid #e9ecef; border-radius: 8px; padding: 20px; text-align: center; margin: 20px 0;">
            <h2 style="color: #2c3e50; font-size: 32px; letter-spacing: 8px; margin: 0; font-family: 'Courier New', monospace;">
                {otp_code}
            </h2>
        </div>
        
        <p><strong>Important:</strong></p>
        <ul>
            <li>This code will expire in 10 minutes</li>
            <li>Don't share this code with anyone</li>
            <li>If you didn't request this code, please ignore this email</li>
        </ul>
        
        <p style="color: #7f8c8d; font-size: 0.9em; margin-top: 30px;">
            This is an automated message from Inbox Memory AI
        </p>
    </div>
    """
    sendemail(user_email, subject, otp_html)
