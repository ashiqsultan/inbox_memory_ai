from fastapi import APIRouter
from pydantic import BaseModel, EmailStr
from typing import Optional
from app.database.redis_connect import RedisConnection

router = APIRouter(prefix="/auth", tags=["auth"])


class SignupRequest(BaseModel):
    email: EmailStr
    name: str


class LoginRequest(BaseModel):
    email: EmailStr


class VerifyOTPRequest(BaseModel):
    email: EmailStr
    otp: str


@router.post("/signup")
async def signup(signup_data: SignupRequest):
    """
    User signup endpoint
    """
    print("Signup request received:")
    print(f"Email: {signup_data.email}")
    print(f"Name: {signup_data.name}")

    # Generate and store OTP
    otp = await RedisConnection.generate_and_store_otp(signup_data.email)

    return {
        "message": "Signup request received. OTP sent.",
        "email": signup_data.email,
        "name": signup_data.name,
    }


@router.post("/login")
async def login(login_data: LoginRequest):
    """
    User login endpoint
    """
    print("Login request received:")
    print(f"Email: {login_data.email}")

    # Generate and store OTP
    otp = await RedisConnection.generate_and_store_otp(login_data.email)

    return {
        "message": "Login request received. OTP sent.",
        "email": login_data.email,
    }


@router.post("/verify-otp")
async def verify_otp(otp_data: VerifyOTPRequest):
    """
    Verify OTP endpoint
    """
    print("Verify OTP request received:")
    print(f"Email: {otp_data.email}")
    print(f"OTP: {otp_data.otp}")

    # Verify OTP using Redis
    is_valid = await RedisConnection.verify_otp(otp_data.email, otp_data.otp)

    if is_valid:
        return {
            "message": "OTP verified successfully",
            "email": otp_data.email,
            "verified": True,
        }
    else:
        return {
            "message": "Invalid or expired OTP",
            "email": otp_data.email,
            "verified": False,
        }
