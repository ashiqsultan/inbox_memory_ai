from app.gemini.llm import llm


possible_actions = ["SAVE", "QA"]


def classify_email(email_text: str):
    """
    Uses Gemini llm model to determine actions
    """
    system_instruction = """You are a classification model for an email processing application.
    You will be provided with Email Subject and Email text as input. 
    Your only purpose is to understand the email subject and content and classify the action.
    There are two possible actions "SAVE" and "QA"
    If the email seems like the user is trying to ask a question then classify the action as "QA"
    If the email looks like a forward message or just some notes and the email doesnt seem like the user is posting a question then classify it as "SAVE"
    OUTPUT INSTRUCTION
    The output must be in JSON in the following format
    For QA the JSON response should be {"action":"QA"}
    For SAVE the JSON response should be {"action":"SAVE"}
    """
    response = llm(email_text, system_instruction=system_instruction)
    return response


if __name__ == "__main__":
    # Test the classification
    test_email = "What is the deadline for submitting the project?"
    result = classify_email(test_email)
    print(f"Test email: {test_email}")
    print(f"Classification result: {result}")
