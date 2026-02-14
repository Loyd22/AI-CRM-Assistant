# This file is where prompts live (so you don't mix them into routes).
# Even if we start with a "local AI", you'll still keep prompts here
# when you switch to a real LLM later.


def build_ticket_analyze_prompt(title: str, message: str) -> str:
    return f"""
You are a CRM assistant.

Analyze this support ticket and return JSON with EXACT keys:
summary, category, urgency, suggested_action, draft_reply

Ticket title: {title}
Ticket message: {message}
""".strip()