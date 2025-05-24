from typing import Optional, List, Any, AsyncGenerator
import asyncpg
import os
from contextlib import asynccontextmanager

DATABASE_URL: str = os.getenv("DATABASE_URL", "")


class Database:
    _pool: Optional[asyncpg.Pool] = None

    @classmethod
    async def connect(cls) -> None:
        try:
            print("Creating database pool... for db string: ", DATABASE_URL)
            cls._pool = await asyncpg.create_pool(
                DATABASE_URL,
                min_size=5,
                max_size=10,
            )
        except Exception as e:
            raise RuntimeError(f"Failed to connect to database: {e}")

    @classmethod
    async def disconnect(cls) -> None:
        if cls._pool:
            try:
                await cls._pool.close()
            except Exception as e:
                raise RuntimeError(f"Failed to disconnect from database: {e}")

    @classmethod
    async def fetch(cls, query: str, *args: Any) -> List[asyncpg.Record]:
        """Fetch multiple rows"""
        if not cls._pool:
            raise RuntimeError("Database connection not established")
        async with cls._pool.acquire() as connection:
            return await connection.fetch(query, *args)

    @classmethod
    async def fetchrow(cls, query: str, *args: Any) -> Optional[asyncpg.Record]:
        """Fetch a single row"""
        if not cls._pool:
            raise RuntimeError("Database connection not established")
        async with cls._pool.acquire() as connection:
            return await connection.fetchrow(query, *args)

    @classmethod
    async def fetchval(cls, query: str, *args: Any) -> Any:
        """Fetch a single value"""
        if not cls._pool:
            raise RuntimeError("Database connection not established")
        async with cls._pool.acquire() as connection:
            return await connection.fetchval(query, *args)

    @classmethod
    async def execute(cls, query: str, *args: Any) -> str:
        """Execute query without returning results"""
        if not cls._pool:
            raise RuntimeError("Database connection not established")
        async with cls._pool.acquire() as connection:
            return await connection.execute(query, *args)

    @classmethod
    async def executemany(cls, query: str, args: List[tuple]) -> None:
        """Execute query with multiple sets of arguments"""
        if not cls._pool:
            raise RuntimeError("Database connection not established")
        async with cls._pool.acquire() as connection:
            await connection.executemany(query, args)

    @classmethod
    async def execute_and_return(
        cls, query: str, *args: Any
    ) -> Optional[asyncpg.Record]:
        """Execute query and return the affected row(s)"""
        if not cls._pool:
            raise RuntimeError("Database connection not established")
        async with cls._pool.acquire() as connection:
            return await connection.fetchrow(query, *args)

    @classmethod
    @asynccontextmanager
    async def transaction(cls) -> AsyncGenerator[asyncpg.Connection, None]:
        """Context manager for database transactions"""
        if not cls._pool:
            raise RuntimeError("Database connection not established")

        async with cls._pool.acquire() as connection:
            async with connection.transaction():
                yield connection
