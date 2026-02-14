# backend/app/repositories/tickets_repo.py

# Session is the DB connection used to run queries (add, commit, query, etc.)
from sqlalchemy.orm import Session
# Import the SQLAlchemy database model (table)
from app.models.ticket import Ticket
# Import the request schema used for creating tickets
from app.schemas.ticket import TicketCreate
from typing import Optional
from app.models.ticket import TicketStatus


class TicketsRepo:
    """
    Repository = the class that talks to the database.

    Why use this?
    - Keeps your routes clean (routes just call repo methods)
    - Easier to test
    - Cleaner structure for real internships/projects
    """

    @staticmethod
    def create(db: Session, payload: TicketCreate) -> Ticket:
        """
        Create a new ticket row in the database.
        """

        # Build a Ticket ORM object from the incoming validated payload
        ticket = Ticket(
            title=payload.title,
            message=payload.message,

            # payload.status is an Enum (TicketStatus)
            # .value converts it to a string like "Open"
            status=payload.status.value,

            category=payload.category,
            urgency=payload.urgency,
            assigned_to=payload.assigned_to,
        )

        # Add the object to the session (still not saved yet)
        db.add(ticket)

        # Commit saves it into the database
        db.commit()

        # Refresh reloads the row from DB so we get:
        # id, created_at, updated_at values filled in
        db.refresh(ticket)

        return ticket

    @staticmethod
    def get_by_id(db: Session, ticket_id: int) -> Optional[Ticket]:
        """
        Get 1 ticket by its id.
        Returns None if not found.
        """

        return db.query(Ticket).filter(Ticket.id == ticket_id).first()

    @staticmethod
    def list(db: Session, limit: int = 50, offset: int = 0) -> list[Ticket]:
        """
        List tickets (latest first).
        limit = how many to return
        offset = for pagination (skip first N rows)
        """

        return (
            db.query(Ticket)
            .order_by(Ticket.created_at.desc())  # newest tickets first
            .offset(offset)                      # skip some rows
            .limit(limit)                        # take only "limit" rows
            .all()                               # execute query and return list
        )
    
    @staticmethod
    def update_status(db: Session, ticket_id: int, new_status: TicketStatus) -> Optional[Ticket]:
        """
        Update the status of a ticket.
        Returns the updated ticket, or None if not found.
        """

        ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
        if not ticket:
            return None

        ticket.status = new_status  # Convert Enum to string
        db.commit()
        db.refresh(ticket)
        return ticket


    @staticmethod
    def delete(db: Session, ticket_id: int) -> bool:
        """
        Delete a ticket by its id.
        Returns True if deleted, False if not found.
        """

        ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
        if not ticket:
            return False

        db.delete(ticket)
        db.commit()
        return True