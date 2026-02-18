"""
ai_prompts.py
Purpose: Build the analysis prompt for the model.
Fits in: backend/app/services
Inputs: ticket details
Output: a single prompt string
"""

def build_ticket_analysis_prompt(title: str, message: str, status: str) -> str:
    """
    Create a clear instruction prompt for analyzing a ticket.

    Params:
      title: ticket title
      message: ticket message/body
      status: current backend status value (open/in_progress/resolved)

    Returns:
      A string prompt to send to the LLM
    """
    return f"""
You are an AI support assistant for a CRM ticketing system.

Analyze this support ticket and respond ONLY with JSON matching the required schema.

Ticket:
- title: {title}
- message: {message}
- status: {status}

Guidelines:
- summary: 1 to 2 sentences.
- category: short label like "billing", "technical", "account", "shipping", "general".
- urgency: "low", "medium", or "high".
- suggested_action: what the support agent should do next (1 to 3 bullets in plain text).
- draft_reply: a polite reply to the customer.

Do not include extra keys. Do not include markdown. Output JSON only.
""".strip()