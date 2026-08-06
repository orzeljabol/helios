import asyncio

from pydantic import BaseModel, Field

from helios.models import InferenceRequest


class MockWorker(BaseModel):
    worker_id: str = Field(min_length=1)
    base_latency_ms: int = Field(gt=0)
    capacity: int = Field(gt=0)
    healthy: bool

    async def execute(self, request: InferenceRequest) -> str:
        await asyncio.sleep(self.base_latency_ms / 1000)
        return f"{self.worker_id} processed: {request.prompt}"
