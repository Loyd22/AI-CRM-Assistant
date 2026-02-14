


# datetime is used in response models (created_at/updated_at)
from datetime import datetime

# Enum ensures only allowed status values are accepted by the API
from enum import Enum

# Optional means this value can be None (nullable)
from typing import Optional

# Pydantic validates request/response data
from pydantic import BaseModel


class TicketStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"


class TicketCreate(BaseModel):
    """
    This schema is for: "Create Ticket" request body.

    Client sends ONLY fields they can control.
    They do NOT send id, created_at, updated_at because DB generates those.
    """

     # Required fields
    title: str
    message: str

    # Default status if not provided
    status: TicketStatus = TicketStatus.OPEN

    # Optional fields (can be missing or None)
    category: Optional[str] = None
    urgency: Optional[str] = None
    assigned_to: Optional[str] = None

class TicketRead(BaseModel):
        """
        This schema is for: "Ticket response" (what API returns).

        Includes DB-generated fields like id and timestamps.
        """
        id: int
        title: str
        message: str
        status: TicketStatus
        category: Optional[str] = None
        urgency: Optional[str] = None
        assigned_to: Optional[str] = None
        created_at: datetime
        updated_at: datetime



        # This tells Pydantic: "You may read data from ORM objects (SQLAlchemy models)"
        # So you can return a Ticket model directly and it will convert to this schema.

        class Config:
            orm_mode = True


class TicketUpdate(BaseModel):
    # for now, only allow status change (simple)
    status: TicketStatus
        