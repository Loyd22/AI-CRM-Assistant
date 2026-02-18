import json  # Used to convert a Python dictionary into a JSON string for saving
from sqlalchemy.orm import Session  # A database connection/session object
from app.models.ai_analysis import AIAnalysis  # The database table model for AI analysis records


# "Repository" = a helper class that does database actions for AIAnalysis.
# Think of it like a staff member who knows how to:
# - save AI results
# - find the latest AI result for a ticket
# - update the final edited text
# - approve the analysis
class AIAnalysisRepo:
    @staticmethod
    def create_for_ticket(db: Session, ticket_id: int, ai_result: dict) -> AIAnalysis:
        # Create a new row (record) in the ai_analyses table for this ticket.
        # We copy values from ai_result (the AI output) into the DB columns.
        row = AIAnalysis(
            ticket_id=ticket_id,                # link this analysis to the ticket
            raw_json=json.dumps(ai_result),     # save the full AI output as a JSON string (for debugging)
            summary=ai_result.get("summary"),   # save summary (if present)
            category=ai_result.get("category"), # save category (if present)
            urgency=ai_result.get("urgency"),   # save urgency (if present)
            suggested_action=ai_result.get("suggested_action"), # save suggested action
            draft_reply=ai_result.get("draft_reply"),           # save draft reply
        )

        db.add(row)      # prepare to insert into database
        db.commit()      # actually save it into the database
        db.refresh(row)  # reload from DB so it includes generated fields (like id)
        return row       # return the saved row

    @staticmethod
    def get_latest_by_ticket(db: Session, ticket_id: int) -> AIAnalysis | None:
        # Get the newest AI analysis for a specific ticket.
        # "order_by(id desc)" means: newest first.
        return (
            db.query(AIAnalysis)
            .filter(AIAnalysis.ticket_id == ticket_id)  # only rows for this ticket
            .order_by(AIAnalysis.id.desc())             # newest row first
            .first()                                    # take the first one (latest)
        )

    @staticmethod
    def update_final(db: Session, analysis_id: int, data: dict) -> AIAnalysis | None:
        # Find the AI analysis row by its ID.
        row = db.query(AIAnalysis).filter(AIAnalysis.id == analysis_id).first()
        if not row:
            return None  # if not found, return nothing

        # Update fields on that row based on the incoming data.
        # Example: data might contain final_summary, final_reply, etc.
        for k, v in data.items():
            setattr(row, k, v)  # set row.k = v

        db.commit()      # save changes to the database
        db.refresh(row)  # reload updated row from the database
        return row

    @staticmethod
    def approve(db: Session, analysis_id: int) -> AIAnalysis | None:
        # Find the AI analysis row by its ID.
        row = db.query(AIAnalysis).filter(AIAnalysis.id == analysis_id).first()
        if not row:
            return None  # if not found, return nothing

        # Mark it as approved (1 = approved).
        row.is_approved = 1

        db.commit()      # save changes
        db.refresh(row)  # reload updated row
        return row