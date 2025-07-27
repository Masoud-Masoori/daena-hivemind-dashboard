"""
Authentication Service for Daena AI VP System
Handles user authentication, authorization, and role-based access control
"""

import jwt
import bcrypt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
from pydantic import BaseModel

# JWT Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Security scheme
security = HTTPBearer()

class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[str] = None
    role: Optional[str] = None

class User(BaseModel):
    user_id: str
    username: str
    email: str
    role: str
    is_active: bool = True

class AuthService:
    def __init__(self):
        self.users = {
            "founder": {
                "user_id": "founder_001",
                "username": "founder",
                "email": "founder@daena.ai",
                "role": "founder",
                "password_hash": bcrypt.hashpw("daena2025!".encode(), bcrypt.gensalt()),
                "is_active": True
            },
            "admin": {
                "user_id": "admin_001", 
                "username": "admin",
                "email": "admin@daena.ai",
                "role": "admin",
                "password_hash": bcrypt.hashpw("admin2025!".encode(), bcrypt.gensalt()),
                "is_active": True
            }
        }
        
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        """Create JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire, "type": "access"})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    def create_refresh_token(self, data: dict):
        """Create JWT refresh token"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire, "type": "refresh"})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    def verify_token(self, token: str) -> TokenData:
        """Verify JWT token and return token data"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            user_id: str = payload.get("user_id")
            role: str = payload.get("role")
            
            if username is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            return TokenData(username=username, user_id=user_id, role=role)
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.PyJWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Authenticate user with username and password"""
        if username not in self.users:
            return None
    
        user_data = self.users[username]
        if not bcrypt.checkpw(password.encode(), user_data["password_hash"]):
            return None
    
        if not user_data["is_active"]:
            return None
        
        return User(**{k: v for k, v in user_data.items() if k != "password_hash"})
    
    def get_current_user(self, credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
        """Get current user from JWT token"""
        token = credentials.credentials
        token_data = self.verify_token(token)
        
        if token_data.username not in self.users:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        user_data = self.users[token_data.username]
        return User(**{k: v for k, v in user_data.items() if k != "password_hash"})
    
    def get_current_active_user(self, credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
        """Get current active user"""
        user = self.get_current_user(credentials)
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user"
            )
        return user
    
    def require_role(self, required_role: str):
        """Decorator to require specific role"""
        def role_checker(user: User = security):
            if user.role != required_role and user.role != "founder":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions"
                )
            return user
        return role_checker

# Global auth service instance
auth_service = AuthService() 