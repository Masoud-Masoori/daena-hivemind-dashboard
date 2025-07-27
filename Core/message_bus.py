# DEPRECATED: Use Core/messaging/message_bus.py instead
raise ImportError("Core/message_bus.py is deprecated. Use Core/messaging/message_bus.py instead.")

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass
import uuid

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='logs/message_bus.log'
)
logger = logging.getLogger(__name__)

@dataclass
class Message:
    id: str
    topic: str
    content: Dict
    sender: str
    timestamp: str
    priority: int = 0
    metadata: Dict = None

class MessageBus:
    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {}
        self.message_queue = asyncio.Queue()
        self.message_history: List[Message] = []
        self.max_history = 1000
        self._processing = False
        self._circuit_breaker = CircuitBreaker()
        self._cache = MessageCache()

    async def publish(self, topic: str, content: Dict, sender: str, priority: int = 0, metadata: Dict = None):
        """Publish a message to a topic."""
        message = Message(
            id=str(uuid.uuid4()),
            topic=topic,
            content=content,
            sender=sender,
            timestamp=datetime.utcnow().isoformat(),
            priority=priority,
            metadata=metadata or {}
        )
        
        await self.message_queue.put(message)
        logger.info(f"Message published to {topic} by {sender}")

    async def subscribe(self, topic: str, callback: Callable):
        """Subscribe to a topic."""
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        self.subscribers[topic].append(callback)
        logger.info(f"New subscription to {topic}")

    async def unsubscribe(self, topic: str, callback: Callable):
        """Unsubscribe from a topic."""
        if topic in self.subscribers:
            self.subscribers[topic].remove(callback)
            logger.info(f"Unsubscribed from {topic}")

    async def process_messages(self):
        """Process messages from the queue."""
        self._processing = True
        while self._processing:
            try:
                message = await self.message_queue.get()
                
                # Check cache
                cached_response = await self._cache.get(message.id)
                if cached_response:
                    await self._notify_subscribers(message, cached_response)
                    continue

                # Process message
                async with self._circuit_breaker:
                    if message.topic in self.subscribers:
                        for callback in self.subscribers[message.topic]:
                            try:
                                response = await callback(message)
                                await self._cache.set(message.id, response)
                                await self._notify_subscribers(message, response)
                            except Exception as e:
                                logger.error(f"Error processing message: {e}")
                                await self._handle_error(message, e)

                # Store in history
                self.message_history.append(message)
                if len(self.message_history) > self.max_history:
                    self.message_history.pop(0)

            except Exception as e:
                logger.error(f"Error in message processing loop: {e}")
                await asyncio.sleep(1)

    async def _notify_subscribers(self, message: Message, response: Any):
        """Notify subscribers of message processing results."""
        for callback in self.subscribers.get(message.topic, []):
            try:
                await callback(message, response)
            except Exception as e:
                logger.error(f"Error notifying subscriber: {e}")

    async def _handle_error(self, message: Message, error: Exception):
        """Handle message processing errors."""
        error_message = Message(
            id=str(uuid.uuid4()),
            topic=f"{message.topic}.error",
            content={"error": str(error), "original_message": message.id},
            sender="system",
            timestamp=datetime.utcnow().isoformat(),
            priority=message.priority + 1
        )
        await self.message_queue.put(error_message)

    async def get_message_history(self, topic: Optional[str] = None, limit: int = 100) -> List[Message]:
        """Get message history, optionally filtered by topic."""
        history = self.message_history
        if topic:
            history = [msg for msg in history if msg.topic == topic]
        return history[-limit:]

    async def stop(self):
        """Stop message processing."""
        self._processing = False
        logger.info("Message bus stopped")

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, reset_timeout: int = 60):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.last_failure_time = None
        self.state = 'CLOSED'

    async def __aenter__(self):
        if self.state == 'OPEN':
            if self.last_failure_time and \
               (datetime.utcnow() - self.last_failure_time).total_seconds() > self.reset_timeout:
                self.state = 'HALF-OPEN'
            else:
                raise CircuitBreakerOpenError()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.failure_count += 1
            self.last_failure_time = datetime.utcnow()
            if self.failure_count >= self.failure_threshold:
                self.state = 'OPEN'
        elif self.state == 'HALF-OPEN':
            self.state = 'CLOSED'
            self.failure_count = 0

class MessageCache:
    def __init__(self, ttl: int = 300):
        self.cache: Dict[str, Dict] = {}
        self.ttl = ttl

    async def get(self, key: str) -> Optional[Dict]:
        """Get a cached message response."""
        if key in self.cache:
            entry = self.cache[key]
            if (datetime.utcnow() - entry['timestamp']).total_seconds() < self.ttl:
                return entry['response']
            del self.cache[key]
        return None

    async def set(self, key: str, response: Any):
        """Cache a message response."""
        self.cache[key] = {
            'response': response,
            'timestamp': datetime.utcnow()
        }

class CircuitBreakerOpenError(Exception):
    pass

# Example usage:
async def main():
    bus = MessageBus()
    
    # Start message processing
    asyncio.create_task(bus.process_messages())
    
    # Example subscriber
    async def handle_message(message: Message, response: Any = None):
        print(f"Received message: {message.content}")
        return {"status": "processed"}
    
    # Subscribe to a topic
    await bus.subscribe("test.topic", handle_message)
    
    # Publish a message
    await bus.publish(
        topic="test.topic",
        content={"data": "test"},
        sender="test_sender"
    )

if __name__ == "__main__":
    asyncio.run(main()) 