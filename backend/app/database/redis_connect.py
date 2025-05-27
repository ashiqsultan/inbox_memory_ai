import redis.asyncio as redis
import os
from typing import Optional


class RedisConnection:
    _instance: Optional[redis.Redis] = None

    @classmethod
    async def connect(cls) -> redis.Redis:
        """Connect to Redis and return the connection instance."""
        if cls._instance is None:
            redis_url = os.getenv("REDIS_URL", "redis://redis:6379")
            cls._instance = redis.from_url(
                redis_url,
                encoding="utf-8",
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5,
                retry_on_timeout=True,
                health_check_interval=30
            )
            
            # Test the connection
            try:
                await cls._instance.ping()
                print("✅ Connected to Redis successfully")
            except Exception as e:
                print(f"❌ Failed to connect to Redis: {e}")
                raise
        
        return cls._instance

    @classmethod
    async def disconnect(cls):
        """Disconnect from Redis."""
        if cls._instance:
            await cls._instance.close()
            cls._instance = None
            print("Disconnected from Redis")

    @classmethod
    def get_instance(cls) -> Optional[redis.Redis]:
        """Get the current Redis instance."""
        return cls._instance


# Convenience alias
Redis = RedisConnection 