from datetime import datetime
from pydantic import BaseModel
from app.gemini.llm import llm
from google.genai import types
from enum import Enum
from typing import Literal, Any


class AnswerOutputFormat(BaseModel):
    answer: str


async def qa_agent(question: str, knowledge_base: str) -> AnswerOutputFormat:
    """
    Gemini model to do question answer based on knowledge_base
    """
    today_date: str = datetime.now().strftime("%Y-%m-%d")
    today_time: str = datetime.now().strftime("%H:%M:%S")

    system_instruction: str = f"""
    You are a helpful assistant.
    You will be provided with a knowledge_base and user_question.
    Your task is to answer user question from the knowledge base. 
    If user question cannot be answered from the knowledgebase then inform the users that you were not able to answer from the internal knowledgebase and answer the question from what you know. 
    Always Priorotize to answer from the given knowledge base.
    Keep your tone friendly.

    The Output must be a JSON in the following format
    {{"answer": "str"}}

    KNOWLEDGE BASE STARTS
    Knowledge Base = {knowledge_base}
    \n
    General Information
    Your name: Inbox Memory Bot
    Today date is {today_date}
    Time is {today_time}
    KNOWLEDGE BASE ENDS
    """

    config: types.GenerateContentConfig = types.GenerateContentConfig(
        system_instruction=system_instruction,
        response_mime_type="application/json",
        response_schema=AnswerOutputFormat,
    )

    response: types.GenerateContentResponse = await llm(question, config)
    if response.parsed:
        parsed_res: BaseModel | Enum | dict[Any, Any] = response.parsed
        if isinstance(parsed_res, AnswerOutputFormat):
            return parsed_res
    raise Exception("Error in qa agent")

async def main() -> None:
    try:
        knowledgebase = """
        The cat sat on a mat
        """
        question = "what did the fox say"
        response: AnswerOutputFormat = await qa_agent(question, knowledgebase)
        print(response.model_dump())

    except Exception as e:
        print("Exception in qa test")
        print(e)

import asyncio
if __name__ == "__main__":
    # Test the classification
    asyncio.run(main())
