from app.gemini.get_embeddings import get_embeddings
from app.lance_db import vector_search, VectorSearchResult
from typing import List


async def get_kb(question: str, user_id: str) -> str:
    """
    Get context from vector db for the given question
    Args:
        question: The question to search for context
        user_id: The user's ID which is used as the table name in LanceDB
    Returns:
        A string containing the relevant context from the knowledge base
    """
    try:
        # Get embeddings for the question
        question_embedding: list[float] = await get_embeddings(question)
        
        # Search the vector database
        search_results: list[VectorSearchResult] = await vector_search(
            table_name=user_id,
            query_vector=question_embedding,
            limit=6  # Get top 6 most relevant chunks
        )
        
        # If no results found, return empty string
        if not search_results:
            return ""
            
        # Sort results by chunk sequence to maintain original order
        sorted_results: list[VectorSearchResult] = sorted(search_results, key=lambda x: int(x.chunk_sequence))
        
        # Combine the text from all results
        context: str = "\n".join(result.text for result in sorted_results)
        
        return context
    except Exception as e:
        print(f"Error in get_kb: {e}")
        return ""
