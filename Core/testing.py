import asyncio
import logging
import unittest
from typing import Dict, List, Any, Optional
from datetime import datetime
import json
import os
from dataclasses import dataclass
import pytest
import aiohttp
import redis
from Core.messaging.message_bus import MessageBus

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='logs/testing.log'
)
logger = logging.getLogger(__name__)

@dataclass
class TestResult:
    name: str
    status: str
    duration: float
    error: Optional[str] = None
    details: Dict[str, Any] = None

class TestRunner:
    def __init__(self):
        self.results: List[TestResult] = []
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None

    async def run_test(self, test_func, *args, **kwargs) -> TestResult:
        """Run a single test."""
        start_time = datetime.now()
        try:
            await test_func(*args, **kwargs)
            status = "PASSED"
            error = None
        except Exception as e:
            status = "FAILED"
            error = str(e)
            logger.error(f"Test {test_func.__name__} failed: {e}")
        
        duration = (datetime.now() - start_time).total_seconds()
        result = TestResult(
            name=test_func.__name__,
            status=status,
            duration=duration,
            error=error
        )
        self.results.append(result)
        return result

    async def run_suite(self, test_suite: List[callable]):
        """Run a suite of tests."""
        self.start_time = datetime.now()
        for test in test_suite:
            await self.run_test(test)
        self.end_time = datetime.now()

    def get_summary(self) -> Dict[str, Any]:
        """Get test run summary."""
        if not self.results:
            return {"status": "No tests run"}
        
        total = len(self.results)
        passed = sum(1 for r in self.results if r.status == "PASSED")
        failed = total - passed
        duration = (self.end_time - self.start_time).total_seconds() if self.end_time else 0
        
        return {
            "total": total,
            "passed": passed,
            "failed": failed,
            "duration": duration,
            "success_rate": (passed / total) * 100 if total > 0 else 0
        }

    def export_results(self, filename: str):
        """Export test results to file."""
        with open(filename, "w") as f:
            json.dump({
                "summary": self.get_summary(),
                "results": [
                    {
                        "name": r.name,
                        "status": r.status,
                        "duration": r.duration,
                        "error": r.error,
                        "details": r.details
                    }
                    for r in self.results
                ]
            }, f, indent=2)

class SystemTest:
    def __init__(self):
        self.runner = TestRunner()
        self.cache = redis.Redis(host='localhost', port=6379, db=0)
        self.session = None

    async def setup(self):
        """Setup test environment."""
        self.session = aiohttp.ClientSession()

    async def teardown(self):
        """Cleanup test environment."""
        if self.session:
            await self.session.close()
        self.cache.flushdb()

    async def test_message_bus(self):
        """Test message bus functionality."""
        bus = MessageBus()
        received_messages = []
        
        async def message_handler(message):
            received_messages.append(message)
        
        await bus.subscribe("test.topic", message_handler)
        await bus.publish("test.topic", {"data": "test"}, "test_sender")
        
        await asyncio.sleep(0.1)  # Allow time for message processing
        
        assert len(received_messages) == 1
        assert received_messages[0].content["data"] == "test"

    async def test_tracing(self):
        """Test distributed tracing."""
        from Core.tracing import Tracer
        
        tracer = Tracer()
        async with tracer.start_span("test_span") as span:
            await tracer.set_attribute(span.id, "test_attr", "test_value")
            await tracer.add_event(span.id, "test_event")
        
        trace = await tracer.get_trace(span.trace_id)
        assert len(trace) == 1
        assert trace[0].name == "test_span"
        assert trace[0].attributes["test_attr"] == "test_value"

    async def test_cache(self):
        """Test Redis cache functionality."""
        from Core.cache import RedisCache
        
        cache = RedisCache()
        test_data = {"key": "value"}
        
        await cache.set("test_key", test_data)
        retrieved = await cache.get("test_key")
        
        assert retrieved == test_data
        assert await cache.exists("test_key")
        
        await cache.delete("test_key")
        assert not await cache.exists("test_key")

    async def test_monitoring(self):
        """Test system monitoring."""
        from Core.monitoring import SystemMonitor
        
        monitor = SystemMonitor()
        metrics = await monitor.get_metrics()
        
        assert "cpu" in metrics
        assert "memory" in metrics
        assert "disk" in metrics
        assert "network" in metrics
        assert "gpu" in metrics

    async def run_all_tests(self):
        """Run all system tests."""
        await self.setup()
        
        test_suite = [
            self.test_message_bus,
            self.test_tracing,
            self.test_cache,
            self.test_monitoring
        ]
        
        await self.runner.run_suite(test_suite)
        self.runner.export_results("test_results.json")
        
        await self.teardown()
        return self.runner.get_summary()

# Example usage:
async def main():
    system_test = SystemTest()
    summary = await system_test.run_all_tests()
    print(f"Test Summary: {summary}")

if __name__ == "__main__":
    asyncio.run(main()) 