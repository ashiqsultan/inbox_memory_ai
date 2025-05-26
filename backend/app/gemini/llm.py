from google import genai
from google.genai import types
from typing import Optional
import os


async def llm(
    prompt: str,
    system_instruction: Optional[str] = None,
    model: str = "gemini-2.0-flash",
) -> str:
    """
    Generate content using the Gemini model.
    Args:

        prompt: The input prompt to generate content from
        system_instruction: Optional system instruction to set the context/persona
        model: The Gemini model to use
    Returns:
        The generated text response
    """
    API_KEY = os.getenv("GEMINI_API_KEY", "")
    client = genai.Client(api_key=API_KEY)
    config = (
        types.GenerateContentConfig(system_instruction=system_instruction)
        if system_instruction
        else None
    )

    response = await client.aio.models.generate_content(
        model=model, config=config, contents=prompt
    )

    return response.text
