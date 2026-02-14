from datetime import datetime 
# We use Enum to define allowed status values (Open, In Progress, Resolved)
from enum import Enum 

from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func 

# Base is the parent class for all SQLAlchemy models
# It tells SQLAlchemy: "this class is a table"
from app.db.base import Base 



# This Enum is for your OWN code clarity.
# In the DB, we will store the status as a plain string.
class TicketStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"


class Ticket(Base):
    """
    This is the DATABASE model (SQLAlchemy ORM model).

    SQLAlchemy uses this class to create a table in the database.
    Think: "this is how a ticket is stored in the DB"
    """

    __tablename__ = "tickets"

     # Basic fields
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)

    # Store status as a string (Open / In Progress / Resolved)
    status = Column(String, nullable=False, default=TicketStatus.OPEN.value)

    # Nullable fields (allowed to be empty for now)
    category = Column(String, nullable=True)
    urgency = Column(String, nullable=True)
    assigned_to = Column(String, nullable=True)

    # Auto timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )