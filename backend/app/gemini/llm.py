from google import genai
from google.genai import types
from typing import Optional
import os


async def llm(
    prompt: str, config: types.GenerateContentConfig
) -> types.GenerateContentResponse:
    """
    Generate content using the Gemini model.
    Args:

        prompt: The input prompt to generate content from
        system_instruction: Optional system instruction to set the context/persona
        model: The Gemini model to use
    Returns:
        The generated text response
    """
    MODEL = "gemini-2.0-flash"
    API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    client: genai.Client = genai.Client(api_key=API_KEY)
    config = config
    response: types.GenerateContentResponse = await client.aio.models.generate_content(
        model=MODEL, config=config, contents=prompt
    )

    return response
