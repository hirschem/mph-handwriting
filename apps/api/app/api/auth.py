from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.auth import verify_password

router = APIRouter()


class LoginRequest(BaseModel):
    password: str


class LoginResponse(BaseModel):
    auth_level: str
    message: str


@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """Authenticate user and return auth level"""
    try:
        auth_level = verify_password(request.password)
        return LoginResponse(
            auth_level=auth_level,
            message=f"Logged in as {auth_level}"
        )
    except HTTPException as e:
        raise e
