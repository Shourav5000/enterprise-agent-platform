from typing import List, Optional
from pydantic import BaseModel, Field

class IncidentState(BaseModel):
    incident_id: str
    raw_ticket_text: str
    category: Optional[str] = None
    urgency_score: Optional[int] = Field(default=1, ge=1, le=5)
    retrieved_logs: List[str] = Field(default_factory=list)
    generated_patch: Optional[str] = None
    qa_status: Optional[str] = Field(default="PENDING")
    execution_logs: List[str] = Field(default_factory=list)
    requires_human_approval: bool = True