from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum 

class UrgencyLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    EMERGENCY = "emergency"

class SymptomInput(BaseModel):
    patient_name: str = Field(..., description="Full name of the patient")
    age: int = Field(...,ge=1, le=120, description="Age of the patient in years")
    symptoms: str = Field(..., min_length=10, description="Describe your symptoms in detail")
    duration_hours: Optional[int] = Field(None, description="How long have you had these symptoms?")
    existing_conditions: Optional[str] = Field(None, description="Any existing medical conditions?")

class TriageResult(BaseModel):
    patient_name: str
    urgency_level: UrgencyLevel
    assessment: str
    recommended_action: str
    follow_up_questions: list[str]
    disclaimer: str = "This is AI-generated guidance only. Always consult a real doctor."