from app.gemini.llm import llm
from google.genai import types
from pydantic import BaseModel
from enum import Enum
import json
from typing import Any
import asyncio


class OutputFormatExtractName(BaseModel):
    username: str


async def extract_username_agent(email_text: str) -> OutputFormatExtractName:
    """
    Uses Gemini llm model to extract username from email text
    Returns:
        OutputFormat with username field containing the extracted name or empty string
    """
    system_instruction = f"""You are a username extraction model for an email processing application.
    You will be provided with Email Subject and Email text as input.
    Your only purpose is to identify and extract the user's name from the email content.
    You Are used in signup time so mostly user will provide the name in the email.
    
    Look for:
    - Names in email signatures
    - Names mentioned in "From:" fields
    - Names in email headers
    - Self-references where the user mentions their own name
    - Any clear indication of the sender's name
    
    If you find a clear username/name, extract it and return it.
    If no clear username is found, return an empty string.
    
    OUTPUT INSTRUCTION
    The output must be in JSON in the following format:
    {{"username":"name"}} or 
    {{"username":""}}
    
    """

    config: types.GenerateContentConfig = types.GenerateContentConfig(
        system_instruction=system_instruction,
        response_mime_type="application/json",
        response_schema=OutputFormatExtractName,
    )

    response: types.GenerateContentResponse = await llm(email_text, config)

    if response.parsed:
        parsed_res: BaseModel | Enum | dict[Any, Any] = response.parsed
        if isinstance(parsed_res, OutputFormatExtractName):
            return parsed_res

    raise Exception("Error in extract_username llm response")


async def main() -> None:
    try:
        # Test with an email that contains a name
        test_email_1 = """
        Subject: Hello
        Hi my name is John and I want to sign up,
        """

        result_1: OutputFormatExtractName = await extract_username_agent(test_email_1)
        print(f"Test email 1: {test_email_1[:50]}...")
        print(f"Extracted username: '{result_1.username}'")
        print()

        # Test with an email that doesn't contain a clear name
        test_email_2 = "Make sure to participate in dev hackathon"
        result_2: OutputFormatExtractName = await extract_username_agent(test_email_2)
        print(f"Test email 2: {test_email_2}")
        print(f"Extracted username: '{result_2.username}'")

    except Exception as e:
        print("Oops !")
        print(e)


if __name__ == "__main__":
    # Test the username extraction
    asyncio.run(main())
