from fastapi import APIRouter, Depends,  HTTPException
from sqlalchemy.orm import Session 


from app.api.deps import get_db
from app.repositories.tickets_repo import TicketsRepo
from app.services.ai_client import analyze_ticket 

router = APIRouter() 


@router.post("/tickets/{ticket_id}/analyze")
def analyze_ticket_endpoint(ticket_id: int, db: Session = Depends(get_db)):


    ticket = TicketsRepo.get_by_id(db, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found") 
    
    result = analyze_ticket(ticket.title, ticket.message)
    return result