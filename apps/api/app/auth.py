from fastapi import HTTPException, Header
from app.models.config import get_settings

settings = get_settings()


def verify_password(password: str) -> str:
    """Verify password and return auth level: 'demo' or 'admin'"""
    if password == settings.admin_password:
        return "admin"
    elif password == settings.demo_password:
        return "demo"
    else:
        raise HTTPException(status_code=401, detail="Invalid password")


def require_admin(authorization: str = Header(...)):
    """Dependency to require admin password"""
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    password = authorization.replace("Bearer ", "")
    auth_level = verify_password(password)
    
    if auth_level != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    return auth_level
