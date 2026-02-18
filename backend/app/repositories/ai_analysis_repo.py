"""
ai_analysis_repo.py
Purpose: Database operations for AIAnalysis (create, fetch latest, update final fields, approve).
Inputs: SQLAlchemy Session + ids/payload dicts.
Outputs: AIAnalysis model instances or None.
"""

import json
from sqlalchemy.orm import Session
from app.models.ai_analysis import AIAnalysis


class AIAnalysisRepo:
    """Repository for AIAnalysis table CRUD operations."""

    @staticmethod
    def create_for_ticket(db: Session, ticket_id: int, ai_result: dict) -> AIAnalysis:
        """Create a new AI analysis row for a ticket from AI result dict."""
        row = AIAnalysis(
            ticket_id=ticket_id,
            raw_json=json.dumps(ai_result),
            summary=ai_result.get("summary"),
            category=ai_result.get("category"),
            urgency=ai_result.get("urgency"),
            suggested_action=ai_result.get("suggested_action"),
            draft_reply=ai_result.get("draft_reply"),
            # initialize final fields as suggested output (so UI can edit from something)
            final_summary=ai_result.get("summary"),
            final_category=ai_result.get("category"),
            final_urgency=ai_result.get("urgency"),
            final_suggested_action=ai_result.get("suggested_action"),
            final_draft_reply=ai_result.get("draft_reply"),
            is_approved=0,
        )
        db.add(row)
        db.commit()
        db.refresh(row)
        return row

    @staticmethod
    def get_latest_by_ticket(db: Session, ticket_id: int) -> AIAnalysis | None:
        """Get the most recent analysis row for a given ticket."""
        return (
            db.query(AIAnalysis)
            .filter(AIAnalysis.ticket_id == ticket_id)
            .order_by(AIAnalysis.id.desc())
            .first()
        )

    @staticmethod
    def update_final_by_ticket(db: Session, ticket_id: int, data: dict) -> AIAnalysis | None:
        """Update the latest analysis row's final fields for a ticket."""
        row = AIAnalysisRepo.get_latest_by_ticket(db, ticket_id)
        if not row:
            return None
        for k, v in data.items():
            setattr(row, k, v)
        db.commit()
        db.refresh(row)
        return row

    @staticmethod
    def approve_latest_by_ticket(db: Session, ticket_id: int) -> AIAnalysis | None:
        """Mark the latest analysis row for a ticket as approved."""
        row = AIAnalysisRepo.get_latest_by_ticket(db, ticket_id)
        if not row:
            return None
        row.is_approved = 1
        db.commit()
        db.refresh(row)
        return row