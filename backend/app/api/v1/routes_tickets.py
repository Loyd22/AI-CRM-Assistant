from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.repositories.tickets_repo import TicketsRepo
from app.schemas.ticket import TicketCreate, TicketUpdate, TicketRead

router = APIRouter()  # tickets router group


# POST /api/v1/tickets
@router.post("", response_model=TicketRead, status_code=status.HTTP_201_CREATED)
def create_ticket(payload: TicketCreate, db: Session = Depends(get_db)):
    # Create a ticket row in the DB and return it
    return TicketsRepo.create(db, payload)


# GET /api/v1/tickets?status_filter=Open
@router.get("", response_model=list[TicketRead])
def list_tickets(
    status_filter: Optional[str] = Query(default=None, description="Open / In Progress / Resolved"),
    db: Session = Depends(get_db),
):
    # Get all tickets (then optionally filter by status)
    tickets = TicketsRepo.list(db)

    if status_filter:
        tickets = [t for t in tickets if t.status == status_filter]

    return tickets


# GET /api/v1/tickets/{ticket_id}
@router.get("/{ticket_id}", response_model=TicketRead)
def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
    # Get one ticket by id
    ticket = TicketsRepo.get_by_id(db, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


# PATCH /api/v1/tickets/{ticket_id}
@router.patch("/{ticket_id}", response_model=TicketRead)
def update_ticket_status(ticket_id: int, payload: TicketUpdate, db: Session = Depends(get_db)):
    # Update only the status
    ticket = TicketsRepo.update_status(db, ticket_id, payload.status.value)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


# DELETE /api/v1/tickets/{ticket_id}
@router.delete("/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ticket(ticket_id: int, db: Session = Depends(get_db)):
    # Delete one ticket
    ok = TicketsRepo.delete(db, ticket_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return None