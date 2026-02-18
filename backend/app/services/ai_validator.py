"""
ai_validator.py
Purpose: Final safety checks for AI output before saving/returning.
Fits in: backend/app/services
"""

from typing import Any, Dict

REQUIRED_KEYS = ["summary", "category", "urgency", "suggested_action", "draft_reply"]

def validate_analysis(result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Ensure result has expected keys and normalize values.

    Params:
      result: dict from AI

    Returns:
      cleaned dict

    Raises:
      ValueError if invalid
    """
    for k in REQUIRED_KEYS:
        if k not in result:
            raise ValueError(f"Missing key: {k}")

    # Normalize urgency to lowercase for consistency
    urgency = str(result["urgency"]).strip().lower()
    if urgency not in ["low", "medium", "high"]:
        urgency = "medium"
    result["urgency"] = urgency

    # Normalize category
    result["category"] = str(result["category"]).strip().lower() or "general"

    return result