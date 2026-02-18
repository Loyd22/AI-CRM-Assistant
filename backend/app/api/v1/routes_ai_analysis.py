from fastapi import APIRouter, Depends, HTTPException  # Tools to create API endpoints, use dependencies, and return errors
from sqlalchemy.orm import Session  # The "database connection" type

from app.api.deps import get_db  # Function that gives us a database session for each request
from app.repositories.ai_analysis_repo import AIAnalysisRepo  # Helper that reads/writes AI analysis in the database
from app.schemas.ai_analysis import AIAnalysisRead, AIAnalysisUpdate  # Rules for what data we return and accept

router = APIRouter()  # Create a group of endpoints related to AI Analysis


# ----------------------------
# 1) GET latest analysis for a ticket
# URL example: GET /api/v1/tickets/5/analysis
# Purpose: Fetch the newest AI analysis saved for ticket #5
# ----------------------------
@router.get("/tickets/{ticket_id}/analysis", response_model=AIAnalysisRead)
def get_latest_analysis(ticket_id: int, db: Session = Depends(get_db)):
    # Get the newest AI analysis record for this ticket from the database
    row = AIAnalysisRepo.get_latest_by_ticket(db, ticket_id)

    # If no analysis exists for this ticket, return a "not found" error
    if not row:
        raise HTTPException(status_code=404, detail="No analysis found for this ticket")

    # Return the analysis (FastAPI will convert it to JSON using AIAnalysisRead schema)
    return row


# ----------------------------
# 2) PATCH update analysis (save edits)
# URL example: PATCH /api/v1/analysis/12
# Purpose: Save the human-edited "final_" fields for analysis #12
# ----------------------------
@router.patch("/analysis/{analysis_id}", response_model=AIAnalysisRead)
def update_analysis(analysis_id: int, payload: AIAnalysisUpdate, db: Session = Depends(get_db)):
    # Convert the incoming payload into a dictionary of only the fields that were provided
    # (exclude_unset=True means: ignore fields the user did not send)
    data = payload.model_dump(exclude_unset=True)

    # Update the analysis in the database (final_summary, final_reply, etc.)
    row = AIAnalysisRepo.update_final(db, analysis_id, data)

    # If analysis record doesn't exist, return a "not found" error
    if not row:
        raise HTTPException(status_code=404, detail="Analysis not found")

    # Return updated analysis record
    return row


# ----------------------------
# 3) POST approve analysis
# URL example: POST /api/v1/analysis/12/approve
# Purpose: Mark analysis #12 as approved (is_approved = 1)
# ----------------------------
@router.post("/analysis/{analysis_id}/approve", response_model=AIAnalysisRead)
def approve_analysis(analysis_id: int, db: Session = Depends(get_db)):
    # Mark the analysis row as approved in the database
    row = AIAnalysisRepo.approve(db, analysis_id)

    # If analysis record doesn't exist, return a "not found" error
    if not row:
        raise HTTPException(status_code=404, detail="Analysis not found")

    # Return the approved analysis record
    return row