"""
ai_analysis.py
Purpose: Database table for storing AI analysis results per ticket, including editable final fields and approval.
Inputs/Outputs: SQLAlchemy model used by repositories/services to read/write rows in ai_analyses table.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base


class AIAnalysis(Base):
    """Stores AI analysis output and user-approved final edits for a ticket."""

    __tablename__ = "ai_analyses"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=False, index=True)

    # Raw and suggested AI output
    raw_json = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    category = Column(String(100), nullable=True)
    urgency = Column(String(50), nullable=True)
    suggested_action = Column(Text, nullable=True)
    draft_reply = Column(Text, nullable=True)

    # Final edited/approved fields
    final_summary = Column(Text, nullable=True)
    final_category = Column(String(100), nullable=True)
    final_urgency = Column(String(50), nullable=True)
    final_suggested_action = Column(Text, nullable=True)
    final_draft_reply = Column(Text, nullable=True)

    # SQLite-friendly boolean (0/1)
    is_approved = Column(Integer, default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)