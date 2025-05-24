from google import genai
from google.genai import types
import os


GEMINI_EMBEDDING_MODEL = "text-embedding-004"
GEMINI_EMBEDDING_DIMENSIONS = 768


def is_embedding_valid(embedding) -> bool:
    """
    Validate that embedding is an array with EXPECTED_DIMENSIONS dimensions.
    """
    if not isinstance(embedding, (list, tuple)):
        print(f"Embedding is not a list/array. Type: {type(embedding)}")
        return False

    EXPECTED_DIMENSIONS = GEMINI_EMBEDDING_DIMENSIONS
    if len(embedding) != EXPECTED_DIMENSIONS:
        print(
            f"Embedding has wrong length. Expected: {EXPECTED_DIMENSIONS}, Got: {len(embedding)}"
        )
        return False

    return True


async def get_embeddings(text: str, title: str | None = None) -> list[float]:
    try:
        API_KEY = os.getenv("GEMINI_API_KEY", "")
        client = genai.Client(api_key=API_KEY)
        config = types.EmbedContentConfig(
            task_type="RETRIEVAL_DOCUMENT",
        )
        if title:
            config.title = title
        result = await client.aio.models.embed_content(
            model=GEMINI_EMBEDDING_MODEL,
            contents=text,
            config=config,
        )

        if result.embeddings[0].values is None:
            raise Exception("Something went wrong while getting embeddings")

        embedding = result.embeddings[0].values

        if not is_embedding_valid(embedding):
            raise Exception(
                f"Embedding validation failed - not a proper {GEMINI_EMBEDDING_DIMENSIONS}-dimensional array"
            )
        return embedding
    except Exception as e:
        print(f"Error getting embedding: {e}")
        raise e
