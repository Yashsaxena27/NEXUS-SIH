from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from backend.app.core.config import settings

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Very simple server-side authentication for SIH demo.
    Checks against a static API token or dummy user session.
    """
    # For demo purposes, we accept "demo-token-123"
    # In a real app, this would verify a JWT or database session.
    valid_token = getattr(settings, "API_AUTH_TOKEN", "demo-token-123")
    
    if credentials.credentials != valid_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return "demo_user"
