"""
routes_ai_analysis.py
Purpose: Endpoints for reading, editing, and approving saved AI analysis results.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.repositories.ai_analysis_repo import AIAnalysisRepo
from app.schemas.ai_analysis import AIAnalysisRead, AIAnalysisUpdate

router = APIRouter()


@router.get("/tickets/{ticket_id}/analysis", response_model=AIAnalysisRead)
def get_latest_analysis(ticket_id: int, db: Session = Depends(get_db)):
    """Fetch latest saved AI analysis for a ticket."""
    row = AIAnalysisRepo.get_latest_by_ticket(db, ticket_id)
    if not row:
        raise HTTPException(status_code=404, detail="No analysis found for this ticket")
    return row


@router.patch("/tickets/{ticket_id}/analysis", response_model=AIAnalysisRead)
def update_latest_analysis(ticket_id: int, payload: AIAnalysisUpdate, db: Session = Depends(get_db)):
    """Edit final fields of latest analysis (draft edits before approval)."""
    row = AIAnalysisRepo.update_final_by_ticket(db, ticket_id, payload.model_dump(exclude_unset=True))
    if not row:
        raise HTTPException(status_code=404, detail="No analysis found for this ticket")
    return row


@router.post("/tickets/{ticket_id}/analysis/approve", response_model=AIAnalysisRead)
def approve_latest_analysis(ticket_id: int, db: Session = Depends(get_db)):
    """Approve the latest analysis for a ticket (locks it logically)."""
    row = AIAnalysisRepo.approve_latest_by_ticket(db, ticket_id)
    if not row:
        raise HTTPException(status_code=404, detail="No analysis found for this ticket")
    return row