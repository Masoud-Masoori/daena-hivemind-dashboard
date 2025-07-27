from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

# Fallback settings if config module is not available
try:
    from backend.config.settings import get_settings
    settings = get_settings()
    API_KEY = settings.SECRET_KEY
    TEST_API_KEY = settings.TEST_API_KEY
except ImportError:
    try:
        from config.settings import get_settings
        settings = get_settings()
        API_KEY = settings.SECRET_KEY
        TEST_API_KEY = settings.TEST_API_KEY
    except ImportError:
        # Fallback settings
        API_KEY = "daena_secure_key_2025"
        TEST_API_KEY = "test-api-key"

class APIKeyGuard(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.api_key = API_KEY
        self.test_api_key = TEST_API_KEY
        
        # List of paths that don't require authentication
        self.public_paths = [
            "/", 
            "/api/v1/health", 
            "/api/v1/rate-limit", 
            "/dashboard", 
            "/dashboard/",
            "/api/v1/external/test",  # Allow test endpoint
            "/docs",
            "/openapi.json",
            "/api/v1/docs",
            "/api/v1/openapi.json",
            "/api/v1/monitoring/metrics",  # Allow metrics endpoint
            "/api/v1/config",  # Allow config endpoint
            "/api/v1/logs",  # Allow logs endpoint
            "/api/v1/daena/status",  # Allow status endpoint
            "/api/v1/daena/analytics",  # Allow analytics endpoint
            "/api/v1/daena/logs",  # Allow daena logs endpoint
            "/api/v1/system/emergency-stop",  # Allow system endpoints
            "/api/v1/system/reboot",
            "/api/v1/system/security-audit",
            "/api/v1/system/performance-optimize",
            "/api/v1/system/update-ai-models",
            "/api/v1/system/deploy-agent",
            "/api/v1/system/create-backup",
            "/api/v1/system/monitor-network",
            "/api/v1/system/manage-users",
            "/api/v1/system/generate-analytics-report",
            "/api/v1/system/setup-workflow-automation",
            "/api/v1/system/manage-apis"
        ]
        
        # External API paths that use their own authentication
        self.external_api_paths = [
            "/api/v1/external/templates/list",
            "/api/v1/external/integrations/available", 
            "/api/v1/external/llm/models"
        ]

    async def dispatch(self, request: Request, call_next):
        # Exclude documentation paths from API key check
        if request.url.path in self.public_paths or request.url.path.startswith("/dashboard/"):
            return await call_next(request)
            
        # Allow external API paths (they have their own authentication)
        if request.url.path.startswith("/api/v1/external/"):
            return await call_next(request)
            
        # Allow OPTIONS requests (CORS preflight)
        if request.method == "OPTIONS":
            return await call_next(request)
            
        client_key = request.headers.get("x-api-key")
        
        # Accept multiple valid keys including frontend default keys
        valid_keys = [
            self.api_key, 
            self.test_api_key, 
            "test-api-key", 
            "daena_secure_key_2025",
            "frontend-key-2025",
            "development-key"
        ]
        
        # For development - allow all localhost requests
        if hasattr(request.url, 'hostname') and (
            "localhost" in str(request.url.hostname) or 
            "127.0.0.1" in str(request.url.hostname) or
            request.url.hostname in ["localhost", "127.0.0.1"]
        ):
            return await call_next(request)
        
        # If no API key provided and not localhost
        if not client_key:
            raise HTTPException(status_code=403, detail="Forbidden: API Key required")
            
        if client_key not in valid_keys:
            raise HTTPException(status_code=403, detail="Forbidden: Invalid API Key")
            
        return await call_next(request)
