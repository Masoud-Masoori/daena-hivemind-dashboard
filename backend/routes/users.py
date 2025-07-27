from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import uuid
import hashlib
import secrets

router = APIRouter()

# Pydantic models
class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: str  # 'admin', 'manager', 'operator', 'viewer'
    department: str
    permissions: List[str]

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    department: Optional[str] = None
    permissions: Optional[List[str]] = None

class User(UserBase):
    id: str
    last_login: str
    status: str  # 'active', 'inactive', 'suspended'
    created_at: str

class PasswordChange(BaseModel):
    old_password: str
    new_password: str

# Mock data storage
users_db = {
    "user-001": {
        "id": "user-001",
        "username": "admin",
        "email": "admin@daena.com",
        "role": "admin",
        "department": "IT",
        "permissions": ["read", "write", "delete", "admin"],
        "password_hash": hashlib.sha256("admin123".encode()).hexdigest(),
        "last_login": "2025-01-14T16:30:00Z",
        "status": "active",
        "created_at": "2025-01-01T00:00:00Z"
    },
    "user-002": {
        "id": "user-002",
        "username": "manager",
        "email": "manager@daena.com",
        "role": "manager",
        "department": "Operations",
        "permissions": ["read", "write"],
        "password_hash": hashlib.sha256("manager123".encode()).hexdigest(),
        "last_login": "2025-01-14T15:45:00Z",
        "status": "active",
        "created_at": "2025-01-05T10:00:00Z"
    },
    "user-003": {
        "id": "user-003",
        "username": "operator",
        "email": "operator@daena.com",
        "role": "operator",
        "department": "Support",
        "permissions": ["read"],
        "password_hash": hashlib.sha256("operator123".encode()).hexdigest(),
        "last_login": "2025-01-14T14:20:00Z",
        "status": "active",
        "created_at": "2025-01-10T14:00:00Z"
    }
}

@router.get("/", response_model=List[User])
async def get_users():
    """Get all users"""
    users = []
    for user in users_db.values():
        user_copy = user.copy()
        del user_copy["password_hash"]  # Don't expose password hashes
        users.append(user_copy)
    return users

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: str):
    """Get a specific user"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    user = users_db[user_id].copy()
    del user["password_hash"]  # Don't expose password hash
    return user

@router.post("/", response_model=User)
async def create_user(user_data: UserCreate):
    """Create a new user"""
    # Check if username or email already exists
    for user in users_db.values():
        if user["username"] == user_data.username:
            raise HTTPException(status_code=400, detail="Username already exists")
        if user["email"] == user_data.email:
            raise HTTPException(status_code=400, detail="Email already exists")
    
    user_id = f"user-{str(uuid.uuid4())[:8]}"
    now = datetime.utcnow().isoformat() + "Z"
    
    # Hash password
    password_hash = hashlib.sha256(user_data.password.encode()).hexdigest()
    
    new_user = {
        "id": user_id,
        "username": user_data.username,
        "email": user_data.email,
        "role": user_data.role,
        "department": user_data.department,
        "permissions": user_data.permissions,
        "password_hash": password_hash,
        "last_login": now,
        "status": "active",
        "created_at": now
    }
    
    users_db[user_id] = new_user
    
    # Return user without password hash
    user_response = new_user.copy()
    del user_response["password_hash"]
    return user_response

@router.put("/{user_id}", response_model=User)
async def update_user(user_id: str, user_data: UserUpdate):
    """Update a user"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    user = users_db[user_id]
    update_data = user_data.dict(exclude_unset=True)
    
    # Check for username/email conflicts
    for other_user in users_db.values():
        if other_user["id"] != user_id:
            if "username" in update_data and other_user["username"] == update_data["username"]:
                raise HTTPException(status_code=400, detail="Username already exists")
            if "email" in update_data and other_user["email"] == update_data["email"]:
                raise HTTPException(status_code=400, detail="Email already exists")
    
    for field, value in update_data.items():
        user[field] = value
    
    # Return user without password hash
    user_response = user.copy()
    del user_response["password_hash"]
    return user_response

@router.delete("/{user_id}")
async def delete_user(user_id: str):
    """Delete a user"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    del users_db[user_id]
    return {"message": "User deleted successfully"}

@router.put("/{user_id}/password")
async def change_user_password(user_id: str, password_data: PasswordChange):
    """Change user password"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    user = users_db[user_id]
    
    # Verify old password
    old_password_hash = hashlib.sha256(password_data.old_password.encode()).hexdigest()
    if user["password_hash"] != old_password_hash:
        raise HTTPException(status_code=400, detail="Invalid old password")
    
    # Update password
    new_password_hash = hashlib.sha256(password_data.new_password.encode()).hexdigest()
    user["password_hash"] = new_password_hash
    
    return {"message": "Password changed successfully"}

@router.post("/{user_id}/reset-password")
async def reset_user_password(user_id: str):
    """Reset user password and generate temporary password"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Generate temporary password
    temp_password = secrets.token_urlsafe(8)
    password_hash = hashlib.sha256(temp_password.encode()).hexdigest()
    
    users_db[user_id]["password_hash"] = password_hash
    
    return {
        "temporary_password": temp_password,
        "message": "Password reset successfully. User should change password on next login."
    }

@router.post("/{user_id}/suspend")
async def suspend_user(user_id: str):
    """Suspend a user account"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    users_db[user_id]["status"] = "suspended"
    return {"message": "User suspended successfully"}

@router.post("/{user_id}/activate")
async def activate_user(user_id: str):
    """Activate a user account"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    users_db[user_id]["status"] = "active"
    return {"message": "User activated successfully"}

@router.get("/{user_id}/permissions")
async def get_user_permissions(user_id: str):
    """Get user permissions"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    user = users_db[user_id]
    return {
        "user_id": user_id,
        "username": user["username"],
        "role": user["role"],
        "permissions": user["permissions"]
    }

@router.post("/{user_id}/login")
async def user_login(user_id: str, password: str):
    """Simulate user login"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    user = users_db[user_id]
    
    # Verify password
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    if user["password_hash"] != password_hash:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if user["status"] != "active":
        raise HTTPException(status_code=403, detail="Account is not active")
    
    # Update last login
    user["last_login"] = datetime.utcnow().isoformat() + "Z"
    
    return {
        "message": "Login successful",
        "user": {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "role": user["role"],
            "permissions": user["permissions"]
        }
    }

@router.get("/roles/available")
async def get_available_roles():
    """Get available user roles and their permissions"""
    return {
        "admin": {
            "description": "Full system access",
            "permissions": ["read", "write", "delete", "admin", "user_management", "system_config"]
        },
        "manager": {
            "description": "Department management access",
            "permissions": ["read", "write", "user_management"]
        },
        "operator": {
            "description": "Operational access",
            "permissions": ["read", "write"]
        },
        "viewer": {
            "description": "Read-only access",
            "permissions": ["read"]
        }
    }

@router.get("/departments/list")
async def get_departments():
    """Get list of available departments"""
    departments = set(user["department"] for user in users_db.values())
    return list(departments)

@router.get("/stats/overview")
async def get_user_stats():
    """Get user statistics"""
    total_users = len(users_db)
    active_users = sum(1 for user in users_db.values() if user["status"] == "active")
    suspended_users = sum(1 for user in users_db.values() if user["status"] == "suspended")
    
    role_counts = {}
    for user in users_db.values():
        role = user["role"]
        role_counts[role] = role_counts.get(role, 0) + 1
    
    return {
        "total_users": total_users,
        "active_users": active_users,
        "suspended_users": suspended_users,
        "role_distribution": role_counts,
        "recent_logins": len([user for user in users_db.values() 
                            if datetime.fromisoformat(user["last_login"].replace("Z", "+00:00")) > 
                            datetime.now().replace(tzinfo=None) - timedelta(hours=24)])
    } 