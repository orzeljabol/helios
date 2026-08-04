from pydantic import BaseModel, Field


class InferenceRequest(BaseModel):
    prompt: str = Field(min_length=1)
    deadline_ms: int = Field(gt=0)
    priority: int = Field(ge=0)
