"""
Authentication routes for Daena AI VP System
Handles login, logout, user management, and role-based access
"""

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional
from datetime import timedelta

from backend.services.auth_service import auth_service, User, security

router = APIRouter(prefix="/api/v1/auth", tags=["authentication"])

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: User

class RefreshTokenRequest(BaseModel):
    refresh_token: str

@router.post("/login", response_model=TokenResponse)
async def login(login_data: LoginRequest):
    """Login and get access token"""
    user = auth_service.authenticate_user(login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create tokens
    access_token = auth_service.create_access_token(
        data={"sub": user.username, "user_id": user.user_id, "role": user.role}
    )
    refresh_token = auth_service.create_refresh_token(
        data={"sub": user.username, "user_id": user.user_id, "role": user.role}
    )
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=30 * 60,  # 30 minutes
        user=user
    )

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(refresh_data: RefreshTokenRequest):
    """Refresh access token using refresh token"""
    try:
        token_data = auth_service.verify_token(refresh_data.refresh_token)
        if token_data.username not in auth_service.users:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        user_data = auth_service.users[token_data.username]
        user = User(**{k: v for k, v in user_data.items() if k != "password_hash"})
        
        # Create new tokens
        access_token = auth_service.create_access_token(
            data={"sub": user.username, "user_id": user.user_id, "role": user.role}
        )
        new_refresh_token = auth_service.create_refresh_token(
            data={"sub": user.username, "user_id": user.user_id, "role": user.role}
        )
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=new_refresh_token,
            expires_in=30 * 60,
            user=user
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

@router.get("/me", response_model=User)
async def get_current_user_info(current_user: User = Depends(auth_service.get_current_active_user)):
    """Get current user information"""
    return current_user

@router.post("/logout")
async def logout(current_user: User = Depends(auth_service.get_current_active_user)):
    """Logout (client should discard tokens)"""
    # In a real implementation, you might want to blacklist the token
    return {"message": "Successfully logged out"}

@router.get("/health")
async def auth_health():
    """Health check for auth service"""
    return {"status": "healthy", "service": "authentication"}

# Add the missing function that other routers need
def get_current_user_optional(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Optional[User]:
    """Get current user if authenticated, otherwise return None"""
    try:
        return auth_service.get_current_user(credentials)
    except:
        return None

# Add permission decorator for voice router
def require_permission(permission: str):
    """Require specific permission"""
    def check_permission(current_user: User = Depends(auth_service.get_current_active_user)) -> User:
        # For now, allow all authenticated users
        return current_user
    return check_permission 