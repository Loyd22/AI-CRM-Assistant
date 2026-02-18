"""
automation_rules.py
Purpose: Apply simple routing rules after AI analysis to auto-assign tickets.
Inputs: SQLAlchemy Ticket model instance + AI fields (category, urgency)
Output: Mutates ticket.assigned_to in-place (and returns it for convenience).
"""

from __future__ import annotations # Allows us to use "Ticket" in type hints before it's defined

from typing import Optional # For type hinting that a variable can be None

class AutomationRules:
    """Applies business routing rules based on AI classification."""

    @staticmethod # This method can be called without creating an instance of AutomationRules
    def apply(ticket, category: Optional[str], urgency: Optional[str]):
        """
        Apply assignment rules to a ticket.

        Args:
            ticket: SQLAlchemy Ticket model instance (must have assigned_to attribute).
            category: AI category string (e.g., "Billing").
            urgency: AI urgency string (e.g., "High").

        Returns:
            The same ticket instance (mutated).
        """
        cat = (category or "").strip().lower()  # Normalize category to lowercase for easier matching
        urg = (urgency or "").strip().lower()   # Normalize urgency to lowercase for easier matching

        # # Priority: category-based routing first (more specific)
        if cat == "billing":
            ticket.assigned_to = "Billing Team"
            return ticket 
        
        if urg == "high":
            ticket.assigned_to = "Urgent Queue"
            return ticket
        
        return ticket # If no rules matched, return the ticket unchanged (assigned_to stays as is)
        
