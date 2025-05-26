from app.gemini.llm import llm
from google.genai import types
from pydantic import BaseModel
from enum import Enum
import json
from typing import Literal, Any


class OutputFormat(BaseModel):
    action: Literal["QA", "SAVE"]


async def classify_email(email_text: str) -> OutputFormat:
    """
    Uses Gemini llm model to determine actions
    Returns:
        OutputFormat
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
    config: types.GenerateContentConfig = types.GenerateContentConfig(
        system_instruction=system_instruction,
        response_mime_type="application/json",
        response_schema=OutputFormat,
    )

    response: types.GenerateContentResponse = await llm(email_text, config)
    # Reference: https://ai.google.dev/gemini-api/docs/structured-output
    if response.parsed:
        parsed_res: BaseModel | Enum | dict[Any, Any] = response.parsed
        if isinstance(parsed_res, OutputFormat):
            action: str = parsed_res.action
            if action == "QA" or action == "SAVE":
                return parsed_res

    raise Exception("Error in classify_email llm response")


import asyncio


async def main() -> None:
    try:
        test_email = "Make sure to participate in dev , to hackathon"
        result: OutputFormat = await classify_email(test_email)
        print(f"Test email: {test_email}")
        print(f"Classification result: {result.action}")
    except Exception as e:
        print("Oops !")
        print(e)


if __name__ == "__main__":
    # Test the classification
    asyncio.run(main())
