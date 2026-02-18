"""
ai_client.py
Purpose: Call OpenAI and return a strict JSON object for ticket analysis.
Fits in: backend/app/services
Inputs: ticket fields (title, message, current status)
Output: dict with keys: summary, category, urgency, suggested_action, draft_reply
Side effects: external API call to OpenAI
"""

import json
import os
from typing import Any, Dict, Optional

from openai import OpenAI

_client: Optional[OpenAI] = None


def get_client() -> OpenAI:
    """Create OpenAI client lazily so env vars exist inside Docker."""
    global _client
    if _client is not None:
        return _client

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set in the backend container.")
    _client = OpenAI(api_key=api_key)
    return _client


def get_model_name() -> str:
    """Return model name from env, with a safe default."""
    return os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


def call_openai_structured(prompt: str) -> Dict[str, Any]:
    """
    Call OpenAI Structured Outputs (Responses API) and return strict JSON.

    Params:
      prompt: full instruction text to the model

    Returns:
      dict: summary/category/urgency/suggested_action/draft_reply
    """
    # IMPORTANT: For Responses API, schema goes under text.format.schema
    # and text.format.name is REQUIRED.
    format_spec = {
        "type": "json_schema",
        "name": "ticket_analysis",
        "strict": True,
        "schema": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "summary": {"type": "string"},
                "category": {"type": "string"},
                "urgency": {"type": "string"},
                "suggested_action": {"type": "string"},
                "draft_reply": {"type": "string"},
            },
            "required": ["summary", "category", "urgency", "suggested_action", "draft_reply"],
        },
    }

    client = get_client()
    resp = client.responses.create(
        model=get_model_name(),
        input=prompt,
        text={"format": format_spec},
        temperature=0.2,
    )

    output_text = resp.output_text
    if not output_text:
        raise RuntimeError("Empty output_text from OpenAI.")
    return json.loads(output_text)