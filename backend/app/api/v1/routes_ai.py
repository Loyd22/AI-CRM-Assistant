from fastapi import APIRouter, Depends,  HTTPException
from sqlalchemy.orm import Session 


from app.api.deps import get_db
from app.repositories.tickets_repo import TicketsRepo
from app.services.ai_client import analyze_ticket 
from app.services.automation_rules import AutomationRules

router = APIRouter() 


@router.post("/tickets/{ticket_id}/analyze")
def analyze_ticket_endpoint(ticket_id: int, db: Session = Depends(get_db)):


    ticket = TicketsRepo.get_by_id(db, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found") 
    
    result = analyze_ticket(ticket.title, ticket.message)

    


    # Purpose: Fetch the ticket record, ensure it exists, then apply automation rules
    # (auto-assignment) based on AI outputs (category/urgency), and persist changes.

    # Fetch the ticket from the database using its ID
    ticket = TicketsRepo.get_by_id(db, ticket_id)

    # If no ticket exists with this ID, stop and return a 404 response
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    # Apply automation rules using AI results:
    # - If urgency is "high" → assigned_to = "Priority Queue"
    # - If category is "billing" → assigned_to = "Billing Team"
    # Note: `result` is the strict AI JSON dict returned by your AI analyzer
    AutomationRules.apply(
        ticket=ticket,
        category=result.get("category"),
        urgency=result.get("urgency"),
    )

    # Save the updated ticket back to the database
    db.commit()

    # Refresh the `ticket` object so it reflects the latest DB state (after commit)
    db.refresh(ticket)
        



    return result


