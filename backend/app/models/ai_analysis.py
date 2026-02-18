from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey  # Tools to describe table columns
from sqlalchemy.sql import func  # Gives us "current time" automatically (for created_at/updated_at)
from app.db.base import Base  # The base class that all database tables in this app inherit from


# This class represents a new table in the database called "ai_analyses".
# Think of it like a record sheet that saves the AI's suggestions for a ticket,
# and also saves the final edited/approved version.
class AIAnalysis(Base):
    __tablename__ = "ai_analyses"  # The table name inside the database

    # Unique ID number for each AI analysis row (auto-increases)
    id = Column(Integer, primary_key=True, index=True)

    # This links the AI analysis to a specific ticket.
    # ForeignKey("tickets.id") means: ticket_id must match an existing ticket's id.
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=False, index=True)

    # This stores the full raw AI JSON output as text (useful for debugging later).
    raw_json = Column(Text, nullable=True)

    # ---------- AI SUGGESTED FIELDS ----------
    # These are the initial suggestions coming from the AI.
    summary = Column(Text, nullable=True)            # short summary of the ticket
    category = Column(String(100), nullable=True)    # category guess (ex: Billing, Bug)
    urgency = Column(String(50), nullable=True)      # urgency guess (ex: High, Medium, Low)
    suggested_action = Column(Text, nullable=True)   # what the AI thinks you should do next
    draft_reply = Column(Text, nullable=True)        # a draft message you can send to the customer

    # ---------- FINAL (EDITED) FIELDS ----------
    # These fields are for the human-edited / approved version.
    # Example: you edit the AI draft, then save the final version here.
    final_summary = Column(Text, nullable=True)
    final_category = Column(String(100), nullable=True)
    final_urgency = Column(String(50), nullable=True)
    final_suggested_action = Column(Text, nullable=True)
    final_draft_reply = Column(Text, nullable=True)

    # Shows whether the AI analysis has been approved.
    # 0 = not approved yet, 1 = approved (simple for SQLite).
    is_approved = Column(Integer, default=0)

    # Automatically saved timestamps:
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)  # when row was created
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)  # when row was last updated