from typing import Optional  # Lets us say a field is allowed to be empty (None)
from pydantic import BaseModel, ConfigDict  # Pydantic = checks/controls the JSON format of API data


# This is the "shape" of the AI analysis data that the backend sends to the frontend.
# Think of it like a template of what the frontend should receive when reading an AI analysis.
class AIAnalysisRead(BaseModel):
    # This allows Pydantic to read data directly from SQLAlchemy database objects
    # (so we can return a DB row and Pydantic will convert it into JSON correctly)
    model_config = ConfigDict(from_attributes=True)

    id: int         # unique ID of this AI analysis record
    ticket_id: int  # which ticket this analysis belongs to

    # These are the AI SUGGESTIONS (can be empty if not saved)
    summary: Optional[str] = None
    category: Optional[str] = None
    urgency: Optional[str] = None
    suggested_action: Optional[str] = None
    draft_reply: Optional[str] = None

    # These are the FINAL / EDITED versions (what a human changes and approves)
    final_summary: Optional[str] = None
    final_category: Optional[str] = None
    final_urgency: Optional[str] = None
    final_suggested_action: Optional[str] = None
    final_draft_reply: Optional[str] = None

    is_approved: int  # 0 = not approved yet, 1 = approved


# This is what the frontend sends when it wants to SAVE edits.
# Notice: it only allows updating the "final_" fields.
class AIAnalysisUpdate(BaseModel):
    final_summary: Optional[str] = None
    final_category: Optional[str] = None
    final_urgency: Optional[str] = None
    final_suggested_action: Optional[str] = None
    final_draft_reply: Optional[str] = None


# This is what the frontend sends when it wants to APPROVE the analysis.
# By default, it sets is_approved = 1 (meaning approved).
class AIAnalysisApprove(BaseModel):
    is_approved: int = 1