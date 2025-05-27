import redis.asyncio as redis
import os
import random
import string
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
                health_check_interval=30,
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

    @classmethod
    async def generate_and_store_otp(cls, email: str) -> str:
        """
        Generate a 6-digit OTP and store it in Redis with 5-minute expiration.

        Args:
            email: User's email address

        Returns:
            Tuple[str, bool]: (OTP, is_new_otp)
            - OTP: The 6-digit OTP string
            - is_new_otp: True if new OTP was generated, False if existing OTP was returned
        """
        redis_instance = await cls.connect()
        otp_key = f"otp:{email}"

        # Check if OTP already exists for this email
        existing_otp = await redis_instance.get(otp_key)

        if existing_otp:
            # OTP already exists, return it
            return existing_otp

        # Generate new 6-digit OTP
        otp = "".join(random.choices(string.digits, k=6))

        # Store OTP in Redis with 5-minute (300 seconds) expiration
        await redis_instance.setex(otp_key, 300, otp)

        return otp

    @classmethod
    async def verify_otp(cls, email: str, provided_otp: str) -> bool:
        """
        Verify the provided OTP against the stored OTP for the email.

        Args:
            email: User's email address
            provided_otp: OTP provided by the user

        Returns:
            bool: True if OTP is valid, False otherwise
        """
        redis_instance = await cls.connect()
        otp_key = f"otp:{email}"

        stored_otp = await redis_instance.get(otp_key)

        if stored_otp and stored_otp == provided_otp:
            # OTP is valid, optionally delete it after successful verification
            await redis_instance.delete(otp_key)
            return True

        return False


# Convenience alias
Redis = RedisConnection
