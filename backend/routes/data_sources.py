from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import uuid
import random

router = APIRouter()

# Pydantic models
class DataSourceBase(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    
    name: str
    type: str  # 'database', 'api', 'file', 'stream', 'webhook'
    connection_string: str
    sync_frequency: str

class DataSourceCreate(DataSourceBase):
    pass

class DataSourceUpdate(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    
    name: Optional[str] = None
    type: Optional[str] = None
    connection_string: Optional[str] = None
    sync_frequency: Optional[str] = None

class DataSource(DataSourceBase):
    id: str
    status: str  # 'connected', 'disconnected', 'error'
    last_sync: str
    schema_data: Dict[str, Any]  # Renamed from 'schema' to avoid conflict

class ConnectionTest(BaseModel):
    connected: bool
    error: Optional[str] = None

# Mock data storage
data_sources_db = {
    "ds-001": {
        "id": "ds-001",
        "name": "Customer Database",
        "type": "database",
        "connection_string": "postgresql://user:pass@localhost:5432/customers",
        "status": "connected",
        "last_sync": "2025-01-14T16:00:00Z",
        "sync_frequency": "1h",
        "schema_data": {
            "tables": ["customers", "orders", "products"],
            "columns": {
                "customers": ["id", "name", "email", "created_at"],
                "orders": ["id", "customer_id", "total", "status"],
                "products": ["id", "name", "price", "category"]
            }
        }
    },
    "ds-002": {
        "id": "ds-002",
        "name": "Sales API",
        "type": "api",
        "connection_string": "https://api.sales.com/v1",
        "status": "connected",
        "last_sync": "2025-01-14T15:30:00Z",
        "sync_frequency": "30m",
        "schema_data": {
            "endpoints": ["/sales", "/customers", "/products"],
            "rate_limit": "1000 requests/hour",
            "authentication": "Bearer token"
        }
    },
    "ds-003": {
        "id": "ds-003",
        "name": "Log Files",
        "type": "file",
        "connection_string": "/var/log/application/*.log",
        "status": "error",
        "last_sync": "2025-01-14T12:00:00Z",
        "sync_frequency": "5m",
        "schema_data": {
            "format": "json",
            "fields": ["timestamp", "level", "message", "user_id"],
            "file_pattern": "*.log"
        }
    },
    "ds-004": {
        "id": "ds-004",
        "name": "Real-time Events",
        "type": "stream",
        "connection_string": "kafka://localhost:9092/events",
        "status": "connected",
        "last_sync": "2025-01-14T16:45:00Z",
        "sync_frequency": "realtime",
        "schema_data": {
            "topics": ["user_events", "system_events", "business_events"],
            "message_format": "avro",
            "partitions": 3
        }
    }
}

@router.get("/", response_model=List[DataSource])
async def get_data_sources():
    """Get all data sources"""
    return list(data_sources_db.values())

@router.get("/{source_id}", response_model=DataSource)
async def get_data_source(source_id: str):
    """Get a specific data source"""
    if source_id not in data_sources_db:
        raise HTTPException(status_code=404, detail="Data source not found")
    return data_sources_db[source_id]

@router.post("/", response_model=DataSource)
async def create_data_source(source_data: DataSourceCreate):
    """Create a new data source"""
    source_id = f"ds-{str(uuid.uuid4())[:8]}"
    now = datetime.utcnow().isoformat() + "Z"
    
    new_source = {
        "id": source_id,
        "name": source_data.name,
        "type": source_data.type,
        "connection_string": source_data.connection_string,
        "status": "disconnected",
        "last_sync": now,
        "sync_frequency": source_data.sync_frequency,
        "schema_data": {}
    }
    
    data_sources_db[source_id] = new_source
    return new_source

@router.put("/{source_id}", response_model=DataSource)
async def update_data_source(source_id: str, source_data: DataSourceUpdate):
    """Update a data source"""
    if source_id not in data_sources_db:
        raise HTTPException(status_code=404, detail="Data source not found")
    
    source = data_sources_db[source_id]
    update_data = source_data.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        source[field] = value
    
    return source

@router.delete("/{source_id}")
async def delete_data_source(source_id: str):
    """Delete a data source"""
    if source_id not in data_sources_db:
        raise HTTPException(status_code=404, detail="Data source not found")
    
    del data_sources_db[source_id]
    return {"message": "Data source deleted successfully"}

@router.post("/{source_id}/test")
async def test_data_source_connection(source_id: str):
    """Test connection to a data source"""
    if source_id not in data_sources_db:
        raise HTTPException(status_code=404, detail="Data source not found")
    
    source = data_sources_db[source_id]
    
    # Simulate connection test
    if random.random() > 0.1:  # 90% success rate
        source["status"] = "connected"
        return {"connected": True, "error": None}
    else:
        source["status"] = "error"
        return {
            "connected": False, 
            "error": "Connection timeout or authentication failed"
        }

@router.post("/{source_id}/sync")
async def sync_data_source(source_id: str, background_tasks: BackgroundTasks):
    """Sync data from a data source"""
    if source_id not in data_sources_db:
        raise HTTPException(status_code=404, detail="Data source not found")
    
    source = data_sources_db[source_id]
    
    if source["status"] != "connected":
        raise HTTPException(status_code=400, detail="Data source is not connected")
    
    sync_id = f"sync-{str(uuid.uuid4())[:8]}"
    
    # Simulate sync process
    def simulate_sync():
        import time
        time.sleep(random.uniform(2, 8))  # Simulate sync time
        
        # Update last sync time
        source["last_sync"] = datetime.utcnow().isoformat() + "Z"
        
        # Randomly update schema (simulate schema changes)
        if random.random() > 0.8:
            if source["type"] == "database":
                source["schema_data"]["tables"].append(f"new_table_{random.randint(1, 100)}")
            elif source["type"] == "api":
                source["schema_data"]["endpoints"].append(f"/new_endpoint_{random.randint(1, 100)}")
    
    background_tasks.add_task(simulate_sync)
    
    return {
        "sync_id": sync_id,
        "status": "started",
        "message": "Data sync initiated"
    }

@router.get("/{source_id}/quality")
async def get_data_quality_report(source_id: str):
    """Get data quality report for a data source"""
    if source_id not in data_sources_db:
        raise HTTPException(status_code=404, detail="Data source not found")
    
    # Simulate data quality analysis
    quality_score = random.uniform(0.7, 1.0)
    
    issues = []
    if quality_score < 0.9:
        issues.append({
            "type": "missing_data",
            "severity": "medium",
            "description": "Some records have missing required fields",
            "affected_records": random.randint(10, 100)
        })
    
    if quality_score < 0.95:
        issues.append({
            "type": "duplicate_records",
            "severity": "low",
            "description": "Duplicate records detected",
            "affected_records": random.randint(5, 50)
        })
    
    return {
        "quality_score": quality_score,
        "issues": issues,
        "last_analyzed": datetime.utcnow().isoformat() + "Z"
    }

@router.get("/stats/overview")
async def get_data_source_stats():
    """Get data source statistics"""
    total_sources = len(data_sources_db)
    connected_sources = sum(1 for source in data_sources_db.values() if source["status"] == "connected")
    error_sources = sum(1 for source in data_sources_db.values() if source["status"] == "error")
    
    # Count by type
    type_counts = {}
    for source in data_sources_db.values():
        source_type = source["type"]
        type_counts[source_type] = type_counts.get(source_type, 0) + 1
    
    # Recent syncs (last 24 hours)
    recent_syncs = [
        source for source in data_sources_db.values()
        if datetime.fromisoformat(source["last_sync"].replace("Z", "+00:00")) > 
        datetime.now().replace(tzinfo=None) - timedelta(hours=24)
    ]
    
    return {
        "total_sources": total_sources,
        "connected_sources": connected_sources,
        "error_sources": error_sources,
        "type_distribution": type_counts,
        "recent_syncs": len(recent_syncs),
        "sync_success_rate": connected_sources / total_sources if total_sources > 0 else 0
    }

@router.get("/types/available")
async def get_available_data_source_types():
    """Get available data source types and their configurations"""
    return {
        "database": {
            "description": "Relational and NoSQL databases",
            "supported_protocols": ["postgresql", "mysql", "mongodb", "redis"],
            "connection_format": "protocol://user:pass@host:port/database",
            "sync_options": ["realtime", "1m", "5m", "15m", "30m", "1h", "6h", "12h", "24h"]
        },
        "api": {
            "description": "REST and GraphQL APIs",
            "supported_protocols": ["http", "https"],
            "connection_format": "https://api.example.com/v1",
            "sync_options": ["realtime", "1m", "5m", "15m", "30m", "1h"]
        },
        "file": {
            "description": "Local and remote files",
            "supported_protocols": ["file", "s3", "ftp", "sftp"],
            "connection_format": "protocol://path/to/files",
            "sync_options": ["1m", "5m", "15m", "30m", "1h", "6h", "12h", "24h"]
        },
        "stream": {
            "description": "Real-time data streams",
            "supported_protocols": ["kafka", "rabbitmq", "redis"],
            "connection_format": "protocol://host:port/topic",
            "sync_options": ["realtime"]
        },
        "webhook": {
            "description": "Webhook endpoints",
            "supported_protocols": ["http", "https"],
            "connection_format": "https://webhook.example.com/endpoint",
            "sync_options": ["realtime"]
        }
    }

@router.post("/{source_id}/schema/discover")
async def discover_data_source_schema(source_id: str):
    """Discover schema for a data source"""
    if source_id not in data_sources_db:
        raise HTTPException(status_code=404, detail="Data source not found")
    
    source = data_sources_db[source_id]
    
    # Simulate schema discovery
    if source["type"] == "database":
        discovered_schema = {
            "tables": ["users", "orders", "products", "categories"],
            "columns": {
                "users": ["id", "name", "email", "created_at", "updated_at"],
                "orders": ["id", "user_id", "total", "status", "created_at"],
                "products": ["id", "name", "price", "category_id", "stock"],
                "categories": ["id", "name", "description"]
            }
        }
    elif source["type"] == "api":
        discovered_schema = {
            "endpoints": ["/users", "/orders", "/products", "/analytics"],
            "rate_limit": "1000 requests/hour",
            "authentication": "Bearer token",
            "response_format": "json"
        }
    else:
        discovered_schema = {
            "format": "json",
            "fields": ["timestamp", "event_type", "data"],
            "sample_data": {"timestamp": "2025-01-14T16:00:00Z", "event_type": "user_login", "data": {}}
        }
    
    source["schema_data"] = discovered_schema
    return {"message": "Schema discovered successfully", "schema": discovered_schema} 