from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import uuid

router = APIRouter()

# Pydantic models
class NotificationBase(BaseModel):
    type: str  # 'info', 'warning', 'error', 'success'
    title: str
    message: str
    recipient: str

class NotificationCreate(NotificationBase):
    expires_at: Optional[str] = None

class Notification(NotificationBase):
    id: str
    read: bool
    created_at: str
    expires_at: Optional[str] = None

# Mock data storage
notifications_db = {
    "notif-001": {
        "id": "notif-001",
        "type": "info",
        "title": "System Update",
        "message": "System maintenance scheduled for tonight at 2 AM",
        "recipient": "admin",
        "read": False,
        "created_at": "2025-01-14T16:30:00Z",
        "expires_at": "2025-01-15T02:00:00Z"
    },
    "notif-002": {
        "id": "notif-002",
        "type": "warning",
        "title": "High CPU Usage",
        "message": "CPU usage has exceeded 80% for the last 10 minutes",
        "recipient": "admin",
        "read": True,
        "created_at": "2025-01-14T15:45:00Z",
        "expires_at": None
    },
    "notif-003": {
        "id": "notif-003",
        "type": "success",
        "title": "Task Completed",
        "message": "Customer data analysis task has been completed successfully",
        "recipient": "manager",
        "read": False,
        "created_at": "2025-01-14T14:20:00Z",
        "expires_at": None
    },
    "notif-004": {
        "id": "notif-004",
        "type": "error",
        "title": "API Connection Failed",
        "message": "Failed to connect to external API service",
        "recipient": "operator",
        "read": False,
        "created_at": "2025-01-14T13:15:00Z",
        "expires_at": None
    }
}

@router.get("/", response_model=List[Notification])
async def get_notifications(read: Optional[bool] = None):
    """Get all notifications with optional read filter"""
    notifications = list(notifications_db.values())
    
    if read is not None:
        notifications = [notif for notif in notifications if notif["read"] == read]
    
    # Sort by creation date (newest first)
    notifications.sort(key=lambda x: x["created_at"], reverse=True)
    return notifications

@router.get("/{notification_id}", response_model=Notification)
async def get_notification(notification_id: str):
    """Get a specific notification"""
    if notification_id not in notifications_db:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notifications_db[notification_id]

@router.post("/", response_model=Notification)
async def create_notification(notification_data: NotificationCreate):
    """Create a new notification"""
    notification_id = f"notif-{str(uuid.uuid4())[:8]}"
    now = datetime.utcnow().isoformat() + "Z"
    
    new_notification = {
        "id": notification_id,
        "type": notification_data.type,
        "title": notification_data.title,
        "message": notification_data.message,
        "recipient": notification_data.recipient,
        "read": False,
        "created_at": now,
        "expires_at": notification_data.expires_at
    }
    
    notifications_db[notification_id] = new_notification
    return new_notification

@router.post("/{notification_id}/read")
async def mark_notification_as_read(notification_id: str):
    """Mark a notification as read"""
    if notification_id not in notifications_db:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    notifications_db[notification_id]["read"] = True
    return {"message": "Notification marked as read"}

@router.post("/read-all")
async def mark_all_notifications_as_read():
    """Mark all notifications as read"""
    for notification in notifications_db.values():
        notification["read"] = True
    
    return {"message": "All notifications marked as read"}

@router.delete("/{notification_id}")
async def delete_notification(notification_id: str):
    """Delete a notification"""
    if notification_id not in notifications_db:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    del notifications_db[notification_id]
    return {"message": "Notification deleted successfully"}

@router.get("/recipient/{recipient}")
async def get_recipient_notifications(recipient: str, unread_only: bool = False):
    """Get notifications for a specific recipient"""
    recipient_notifications = [
        notif for notif in notifications_db.values() 
        if notif["recipient"] == recipient
    ]
    
    if unread_only:
        recipient_notifications = [notif for notif in recipient_notifications if not notif["read"]]
    
    # Sort by creation date (newest first)
    recipient_notifications.sort(key=lambda x: x["created_at"], reverse=True)
    return recipient_notifications

@router.get("/stats/overview")
async def get_notification_stats():
    """Get notification statistics"""
    total_notifications = len(notifications_db)
    unread_notifications = sum(1 for notif in notifications_db.values() if not notif["read"])
    read_notifications = total_notifications - unread_notifications
    
    # Count by type
    type_counts = {}
    for notif in notifications_db.values():
        notif_type = notif["type"]
        type_counts[notif_type] = type_counts.get(notif_type, 0) + 1
    
    # Count by recipient
    recipient_counts = {}
    for notif in notifications_db.values():
        recipient = notif["recipient"]
        recipient_counts[recipient] = recipient_counts.get(recipient, 0) + 1
    
    # Recent notifications (last 24 hours)
    recent_notifications = [
        notif for notif in notifications_db.values()
        if datetime.fromisoformat(notif["created_at"].replace("Z", "+00:00")) > 
        datetime.now().replace(tzinfo=None) - timedelta(hours=24)
    ]
    
    return {
        "total_notifications": total_notifications,
        "unread_notifications": unread_notifications,
        "read_notifications": read_notifications,
        "type_distribution": type_counts,
        "recipient_distribution": recipient_counts,
        "recent_notifications": len(recent_notifications)
    }

@router.post("/send")
async def send_notification(notification_data: Dict[str, Any]):
    """Send a notification to multiple recipients"""
    recipients = notification_data.get("recipients", [])
    notification_type = notification_data.get("type", "info")
    title = notification_data.get("title", "")
    message = notification_data.get("message", "")
    
    created_notifications = []
    
    for recipient in recipients:
        notification_id = f"notif-{str(uuid.uuid4())[:8]}"
        now = datetime.utcnow().isoformat() + "Z"
        
        new_notification = {
            "id": notification_id,
            "type": notification_type,
            "title": title,
            "message": message,
            "recipient": recipient,
            "read": False,
            "created_at": now,
            "expires_at": None
        }
        
        notifications_db[notification_id] = new_notification
        created_notifications.append(new_notification)
    
    return {
        "message": f"Sent {len(created_notifications)} notifications",
        "notifications": created_notifications
    }

@router.post("/broadcast")
async def broadcast_notification(notification_data: Dict[str, Any]):
    """Broadcast a notification to all users"""
    notification_type = notification_data.get("type", "info")
    title = notification_data.get("title", "")
    message = notification_data.get("message", "")
    
    # Get all unique recipients from existing notifications
    all_recipients = set(notif["recipient"] for notif in notifications_db.values())
    
    created_notifications = []
    
    for recipient in all_recipients:
        notification_id = f"notif-{str(uuid.uuid4())[:8]}"
        now = datetime.utcnow().isoformat() + "Z"
        
        new_notification = {
            "id": notification_id,
            "type": notification_type,
            "title": title,
            "message": message,
            "recipient": recipient,
            "read": False,
            "created_at": now,
            "expires_at": None
        }
        
        notifications_db[notification_id] = new_notification
        created_notifications.append(new_notification)
    
    return {
        "message": f"Broadcasted notification to {len(created_notifications)} recipients",
        "notifications": created_notifications
    }

@router.delete("/expired")
async def delete_expired_notifications():
    """Delete expired notifications"""
    now = datetime.utcnow()
    expired_notifications = []
    
    for notif_id, notif in list(notifications_db.items()):
        if notif["expires_at"]:
            expires_at = datetime.fromisoformat(notif["expires_at"].replace("Z", "+00:00"))
            if expires_at < now:
                expired_notifications.append(notif)
                del notifications_db[notif_id]
    
    return {
        "message": f"Deleted {len(expired_notifications)} expired notifications",
        "deleted_notifications": expired_notifications
    } 