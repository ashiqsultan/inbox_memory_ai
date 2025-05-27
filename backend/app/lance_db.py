from datetime import datetime
from typing import List
from lancedb.pydantic import Vector, LanceModel
import lancedb
from pydantic import BaseModel


class TextEmbeddingSchema(LanceModel):
    id: str
    email_ref_id: str
    vector: Vector(768)
    text: str
    chunk_sequence: int
    created_at: datetime


class VectorSearchResult(BaseModel):
    email_ref_id: str
    text: str
    chunk_sequence: int
    created_at: datetime


DB_PATH = "lance_storage/default-db"


# Function to create and get table
async def get_or_create_table(table_name: str = "default_table"):
    """
    Table name is the user_id.
    Lance stores the data in a files and folder with the name of the table.
    """
    # Connect to local LanceDB
    db = await lancedb.connect_async(DB_PATH)

    # Create table if it doesn't exist
    try:
        table = await db.open_table(table_name)
    except:
        table = await db.create_table(table_name, schema=TextEmbeddingSchema)
    return table


async def add_record(table_name: str, records: list[TextEmbeddingSchema]):
    try:
        table = await get_or_create_table(table_name)
        await table.add(records)
    except Exception as e:
        print("Error in add_record: ")
        print(e)
        raise e


async def delete_records_by_email_ref_id(table_name: str, email_ref_id: str) -> bool:
    """
    Deletes multiple records from the given table_name which has the given email_ref_id
    """
    try:
        table = await get_or_create_table(table_name)
        await table.delete(where=f"email_ref_id = '{email_ref_id}'")
        print(f"Deleted records with email_ref_id: {email_ref_id}")
        return True
    except Exception as e:
        print(f"Error deleting records by email_ref_id: {e}")
        return False


async def vector_search(
    table_name: str,
    query_vector: List[float],
    limit: int = 25,
) -> List[VectorSearchResult]:
    try:
        table = await get_or_create_table(table_name)
        results = (
            await table.vector_search(query_vector)
            .select(["email_ref_id", "chunk_sequence", "text", "created_at"])
            .limit(limit)
            .to_pandas()
        )
        return [VectorSearchResult(**row) for row in results.to_dict("records")]
    except Exception as e:
        print(f"Error in vector_search: {e}")
        return []
