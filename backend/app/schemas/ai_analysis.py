"""
ai_analysis.py (schema)
Purpose: Pydantic schemas for validating AIAnalysis API input/output.
Inputs: request payloads (update/approve)
Outputs: response models for API.
"""

from typing import Optional
from pydantic import BaseModel, ConfigDict


class AIAnalysisRead(BaseModel):
    """Response schema for returning a saved AI analysis row."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    ticket_id: int

    summary: Optional[str] = None
    category: Optional[str] = None
    urgency: Optional[str] = None
    suggested_action: Optional[str] = None
    draft_reply: Optional[str] = None

    final_summary: Optional[str] = None
    final_category: Optional[str] = None
    final_urgency: Optional[str] = None
    final_suggested_action: Optional[str] = None
    final_draft_reply: Optional[str] = None

    is_approved: int


class AIAnalysisUpdate(BaseModel):
    """Request schema for editing the final (approved) fields."""
    final_summary: Optional[str] = None
    final_category: Optional[str] = None
    final_urgency: Optional[str] = None
    final_suggested_action: Optional[str] = None
    final_draft_reply: Optional[str] = None