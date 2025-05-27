from app.helpers.sendemail import sendemail


def send_welcome_email(user_email: str) -> None:
    """
    Sends a welcome email to new users with instructions on how to use Inbox Memory AI.

    Args:
        user_email: The email address of the new user
    """
    subject = "Welcome to Inbox Memory AI! 🎉"

    welcome_html = """
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
        <h1 style="color: #2c3e50;">Welcome to Inbox Memory AI! 🎉</h1>
        
        <p>Thank you for signing up! We're excited to help you build and interact with your personal knowledge base.</p>
        
        <h2 style="color: #34495e;">How Inbox Memory Works</h2>
        
        <h3 style="color: #34495e;">Building Your Knowledge Base</h3>
        <p>To save information to your knowledge base, simply forward any email to this address. Every forwarded email will be processed and stored in your personal knowledge base.</p>
        
        <h3 style="color: #34495e;">Accessing Your Knowledge</h3>
        <p>To interact with your saved knowledge:</p>
        <ol>
            <li>Simply send an email with your question</li>
            <li>Our AI will search through your knowledge base</li>
            <li>You'll receive a response based on your saved information</li>
        </ol>
        
        <h3 style="color: #34495e;">Quick Start Guide</h3>
        <ul style="list-style-type: none; padding-left: 0;">
            <li>✉️ <strong>To Save:</strong> Forward any email to this address</li>
            <li>❓ <strong>To Ask:</strong> Send an email with your question</li>
        </ul>
        
        <p style="margin-top: 20px;">Start building your knowledge base today by forwarding your first email!</p>
        
        <p style="color: #7f8c8d; font-size: 0.9em; margin-top: 30px;">
            PS: This is build for Dev.to Postmark Hackathon
        </p>
    </div>
    """
    sendemail(user_email, subject, welcome_html)
