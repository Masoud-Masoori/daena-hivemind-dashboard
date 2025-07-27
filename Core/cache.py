import redis
import json
import logging
from typing import Any, Optional, Dict, List
from datetime import datetime, timedelta
import asyncio
from functools import wraps

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='logs/cache.log'
)
logger = logging.getLogger(__name__)

class RedisCache:
    def __init__(self, host: str = 'localhost', port: int = 6379, db: int = 0,
                 password: Optional[str] = None, ttl: int = 300):
        """Initialize Redis cache connection."""
        self.redis = redis.Redis(
            host=host,
            port=port,
            db=db,
            password=password,
            decode_responses=True
        )
        self.ttl = ttl
        self._connection_pool = redis.ConnectionPool(
            host=host,
            port=port,
            db=db,
            password=password
        )
        self._stats = {
            "hits": 0,
            "misses": 0,
            "sets": 0,
            "deletes": 0
        }

    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        try:
            value = self.redis.get(key)
            if value:
                self._stats["hits"] += 1
                return json.loads(value)
            self._stats["misses"] += 1
            return None
        except Exception as e:
            logger.error(f"Error getting from cache: {e}")
            return None

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set value in cache."""
        try:
            self.redis.setex(
                key,
                ttl or self.ttl,
                json.dumps(value)
            )
            self._stats["sets"] += 1
            return True
        except Exception as e:
            logger.error(f"Error setting cache: {e}")
            return False

    async def delete(self, key: str) -> bool:
        """Delete value from cache."""
        try:
            self.redis.delete(key)
            self._stats["deletes"] += 1
            return True
        except Exception as e:
            logger.error(f"Error deleting from cache: {e}")
            return False

    async def exists(self, key: str) -> bool:
        """Check if key exists in cache."""
        try:
            return bool(self.redis.exists(key))
        except Exception as e:
            logger.error(f"Error checking cache existence: {e}")
            return False

    async def increment(self, key: str, amount: int = 1) -> Optional[int]:
        """Increment value in cache."""
        try:
            return self.redis.incrby(key, amount)
        except Exception as e:
            logger.error(f"Error incrementing cache: {e}")
            return None

    async def get_stats(self) -> Dict[str, int]:
        """Get cache statistics."""
        return self._stats.copy()

    async def clear_stats(self):
        """Clear cache statistics."""
        self._stats = {
            "hits": 0,
            "misses": 0,
            "sets": 0,
            "deletes": 0
        }

    async def get_all_keys(self, pattern: str = "*") -> List[str]:
        """Get all keys matching pattern."""
        try:
            return self.redis.keys(pattern)
        except Exception as e:
            logger.error(f"Error getting keys: {e}")
            return []

    async def get_many(self, keys: List[str]) -> Dict[str, Any]:
        """Get multiple values from cache."""
        try:
            values = self.redis.mget(keys)
            result = {}
            for key, value in zip(keys, values):
                if value:
                    result[key] = json.loads(value)
                    self._stats["hits"] += 1
                else:
                    self._stats["misses"] += 1
            return result
        except Exception as e:
            logger.error(f"Error getting many from cache: {e}")
            return {}

    async def set_many(self, mapping: Dict[str, Any], ttl: Optional[int] = None) -> bool:
        """Set multiple values in cache."""
        try:
            pipeline = self.redis.pipeline()
            for key, value in mapping.items():
                pipeline.setex(
                    key,
                    ttl or self.ttl,
                    json.dumps(value)
                )
            pipeline.execute()
            self._stats["sets"] += len(mapping)
            return True
        except Exception as e:
            logger.error(f"Error setting many in cache: {e}")
            return False

def cached(ttl: Optional[int] = None, key_prefix: str = ""):
    """Decorator for caching function results."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Create cache key
            key_parts = [key_prefix, func.__name__]
            key_parts.extend(str(arg) for arg in args)
            key_parts.extend(f"{k}:{v}" for k, v in sorted(kwargs.items()))
            key = ":".join(key_parts)

            # Try to get from cache
            cache = RedisCache()
            cached_value = await cache.get(key)
            if cached_value is not None:
                return cached_value

            # If not in cache, call function
            result = await func(*args, **kwargs)
            await cache.set(key, result, ttl)
            return result
        return wrapper
    return decorator

# Example usage:
async def main():
    cache = RedisCache()
    
    # Set and get value
    await cache.set("test_key", {"data": "test_value"})
    value = await cache.get("test_key")
    print(f"Retrieved value: {value}")
    
    # Use decorator
    @cached(ttl=60, key_prefix="test")
    async def expensive_operation(x: int, y: int):
        await asyncio.sleep(1)  # Simulate expensive operation
        return x + y
    
    # First call will be slow
    result1 = await expensive_operation(1, 2)
    print(f"First call result: {result1}")
    
    # Second call will be fast (from cache)
    result2 = await expensive_operation(1, 2)
    print(f"Second call result: {result2}")
    
    # Get cache stats
    stats = await cache.get_stats()
    print(f"Cache stats: {stats}")

if __name__ == "__main__":
    asyncio.run(main()) 