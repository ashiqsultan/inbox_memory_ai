from datetime import datetime
import html


def generate_qa_email_html(question: str, answer: str):
    """
    Generate only the HTML content without sending email.

    Args:
        question (str): The question that was asked
        answer (str): The AI's response

    Returns:
        str: HTML content ready to be used
    """
    html_template = """<!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Inbox Memory AI</title>
    <style>
        body {{font-family: Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f9f9f9;
        }}
        .container {{
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 24px;
        }}
        .content {{
            padding: 30px;
        }}
        .question-section {{
            background-color: #f8f9fa;
            border-left: 4px solid #667eea;
            padding: 20px;
            margin-bottom: 25px;
            border-radius: 0 4px 4px 0;
        }}
        .question-label {{
            font-weight: bold;
            color: #667eea;
            text-transform: uppercase;
            font-size: 12px;
            letter-spacing: 1px;
            margin-bottom: 10px;
        }}
        .question-text {{
            font-size: 16px;
            color: #333;
            margin: 0;
        }}
        .answer-section {{
            background-color: #fff;
            border-left: 4px solid #28a745;
            padding: 20px;
            margin-bottom: 25px;
            border-radius: 0 4px 4px 0;
        }}
        .answer-label {{
            font-weight: bold;
            color: #28a745;
            text-transform: uppercase;
            font-size: 12px;
            letter-spacing: 1px;
            margin-bottom: 10px;
        }}
        .answer-text {{
            font-size: 16px;
            color: #333;
            margin: 0;
            white-space: pre-line;
        }}
        .footer {{
            background-color: #f8f9fa;
            padding: 10px;
            text-align: center;
            border-top: 1px solid #e9ecef;
            font-size: 14px;
            color: #6c757d;
        }}
        .timestamp {{
            font-style: italic;
            color: #6c757d;
            font-size: 12px;
            text-align: right;
            margin-top: 16px;
        }}
    </style></head><body>
    <div class="container">
        <div class="header">
            <h1>Inbox Memory AI</h1>
        </div>
        
        <div class="content">
            <div class="question-section">
                <div class="question-label">Question</div>
                <p class="question-text">{question}</p>
            </div>
            
            <div class="answer-section">
                <div class="answer-label">AI Response</div>
                <p class="answer-text">{answer}</p>
            </div>
        </div>
        
        <div class="footer">
            <p>Generated on {timestamp}</p>
        </div>
    </div></body></html>"""

    # Escape HTML characters and format the content
    escaped_question = html.escape(question)
    escaped_answer = html.escape(answer)
    timestamp = datetime.now().strftime("%Y-%m-%d at %H:%M:%S")

    formatted_email: str = html_template.format(
        question=escaped_question, answer=escaped_answer, timestamp=timestamp
    )

    return formatted_email


# Example usage:
if __name__ == "__main__":
    # Example 1: Generate HTML only
    question = "What is machine learning?"
    answer = "Machine learning is a subset of artificial intelligence that enables computers to learn and make decisions from data without being explicitly programmed for every task."

    html_content: str = generate_qa_email_html(question, answer)

    # Save to file for testing
    with open("ai_response_email.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    print("HTML email generated successfully!")
