import logging
import time
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import json
import asyncio
from contextlib import asynccontextmanager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='logs/tracing.log'
)
logger = logging.getLogger(__name__)

@dataclass
class Span:
    id: str
    trace_id: str
    parent_id: Optional[str]
    name: str
    start_time: float
    end_time: Optional[float] = None
    attributes: Dict[str, Any] = None
    events: List[Dict] = None
    status: str = "OK"
    error: Optional[str] = None

class Tracer:
    def __init__(self):
        self.spans: Dict[str, Span] = {}
        self.traces: Dict[str, List[Span]] = {}
        self._export_queue = asyncio.Queue()
        self._processing = False

    @asynccontextmanager
    async def start_span(self, name: str, trace_id: Optional[str] = None, 
                        parent_id: Optional[str] = None, attributes: Dict = None):
        """Start a new span."""
        span_id = str(uuid.uuid4())
        if not trace_id:
            trace_id = str(uuid.uuid4())
        
        span = Span(
            id=span_id,
            trace_id=trace_id,
            parent_id=parent_id,
            name=name,
            start_time=time.time(),
            attributes=attributes or {},
            events=[]
        )
        
        self.spans[span_id] = span
        if trace_id not in self.traces:
            self.traces[trace_id] = []
        self.traces[trace_id].append(span)
        
        try:
            yield span
        except Exception as e:
            span.status = "ERROR"
            span.error = str(e)
            raise
        finally:
            span.end_time = time.time()
            await self._export_queue.put(span)

    async def add_event(self, span_id: str, name: str, attributes: Dict = None):
        """Add an event to a span."""
        if span_id in self.spans:
            self.spans[span_id].events.append({
                "name": name,
                "timestamp": time.time(),
                "attributes": attributes or {}
            })

    async def set_attribute(self, span_id: str, key: str, value: Any):
        """Set an attribute on a span."""
        if span_id in self.spans:
            self.spans[span_id].attributes[key] = value

    async def get_trace(self, trace_id: str) -> List[Span]:
        """Get all spans for a trace."""
        return self.traces.get(trace_id, [])

    async def process_exports(self):
        """Process spans for export."""
        self._processing = True
        while self._processing:
            try:
                span = await self._export_queue.get()
                await self._export_span(span)
            except Exception as e:
                logger.error(f"Error processing span export: {e}")
                await asyncio.sleep(1)

    async def _export_span(self, span: Span):
        """Export a span to storage."""
        try:
            # Export to file
            with open(f"logs/traces/{span.trace_id}.json", "a") as f:
                json.dump({
                    "id": span.id,
                    "trace_id": span.trace_id,
                    "parent_id": span.parent_id,
                    "name": span.name,
                    "start_time": span.start_time,
                    "end_time": span.end_time,
                    "duration": span.end_time - span.start_time if span.end_time else None,
                    "attributes": span.attributes,
                    "events": span.events,
                    "status": span.status,
                    "error": span.error
                }, f)
                f.write("\n")
            
            # Export to monitoring system
            await self._export_to_monitoring(span)
            
        except Exception as e:
            logger.error(f"Error exporting span: {e}")

    async def _export_to_monitoring(self, span: Span):
        """Export span data to monitoring system."""
        try:
            # Add monitoring metrics
            metrics = {
                "span_duration": span.end_time - span.start_time if span.end_time else None,
                "span_status": span.status,
                "has_error": span.error is not None,
                "event_count": len(span.events),
                "attribute_count": len(span.attributes)
            }
            
            # Export to monitoring system
            # TODO: Implement monitoring system integration
            
        except Exception as e:
            logger.error(f"Error exporting to monitoring: {e}")

    async def stop(self):
        """Stop the tracer."""
        self._processing = False
        logger.info("Tracer stopped")

# Example usage:
async def main():
    tracer = Tracer()
    
    # Start export processing
    asyncio.create_task(tracer.process_exports())
    
    # Example trace
    async with tracer.start_span("main_operation") as span:
        await tracer.set_attribute(span.id, "operation_type", "test")
        
        # Nested span
        async with tracer.start_span("sub_operation", parent_id=span.id) as sub_span:
            await tracer.add_event(sub_span.id, "processing_started")
            await asyncio.sleep(0.1)  # Simulate work
            await tracer.add_event(sub_span.id, "processing_completed")
        
        # Add event to parent span
        await tracer.add_event(span.id, "sub_operation_completed")

if __name__ == "__main__":
    asyncio.run(main()) 