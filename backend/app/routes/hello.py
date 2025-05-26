from fastapi import APIRouter
from app.lance_db import get_or_create_table
from app.config import settings


router = APIRouter()


@router.get("/hello")
async def hello_world():
    print("Hello World started")
    print("Hello World ended")
    return {"message": "Hello World"}


@router.get("/environment")
async def get_environment():
    """
    Get the current environment the application is running in
    """
    return {
        "environment": settings.environment,
        "is_development": settings.is_development,
        "is_production": settings.is_production,
    }


@router.get("/print-table/{table_id}")
async def print_table_items(table_id: str):
    """
    Temporary route to print all items in a LanceDB table given a table ID
    Example: /print-table/26b54e25-b104-4ddf-8db2-db14ebe8b2ac

    This route only works in development mode.
    """
    # Check if we're in production mode
    if settings.is_production:
        return {"message": "nothing to see"}

    try:
        print(f"Fetching all items from table: {table_id}")
        table = await get_or_create_table(table_id)

        # Get all records from the table
        df = await table.to_pandas()

        print(f"Found {len(df)} records in table {table_id}")
        print("=" * 50)

        # Print each record
        for index, row in df.iterrows():
            print(f"Record {index + 1}:")
            print(f"  ID: {row.get('id', 'N/A')}")
            print(f"  Email Ref ID: {row.get('email_ref_id', 'N/A')}")
            print(f"  Text: {row.get('text', 'N/A')[:100]}...")  # First 100 chars
            print(f"  Chunk Sequence: {row.get('chunk_sequence', 'N/A')}")
            print(f"  Created At: {row.get('created_at', 'N/A')}")
            print("-" * 30)

        return {
            "message": f"Printed {len(df)} records from table {table_id}",
            "total_records": len(df),
            "table_id": table_id,
        }

    except Exception as e:
        error_msg = f"Error fetching records from table {table_id}: {str(e)}"
        print(error_msg)
        return {"error": error_msg, "table_id": table_id}
