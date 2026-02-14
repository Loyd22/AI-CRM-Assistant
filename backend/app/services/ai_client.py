import re  # Tool for cleaning text (example: remove extra spaces)
from app.services.ai_validator import validate_ai_result  # Checks that the AI output has the correct fields


# This function is a simple "local AI".
# It does NOT call real AI like OpenAI.
# It just uses keyword rules so the feature works for now.
# Later you can replace this with real AI calls.
def analyze_ticket_locally(title: str, message: str) -> dict:
    # Combine title + message and make everything lowercase
    # so word matching is easier (Login == login)
    text = (title + " " + message).lower()

    # ---------- CATEGORY RULES ----------
    # We guess the category based on keywords found in the ticket text.
    if any(k in text for k in ["login", "password", "otp", "signin", "sign in"]):
        category = "Authentication"
    elif any(k in text for k in ["payment", "invoice", "billing", "refund"]):
        category = "Billing"
    elif any(k in text for k in ["bug", "error", "crash", "broken", "issue"]):
        category = "Bug"
    else:
        category = "General"

    # ---------- URGENCY RULES ----------
    # We guess urgency by looking for "emergency" type words.
    if any(k in text for k in ["urgent", "asap", "immediately", "can't access", "down", "blocked"]):
        urgency = "High"
    elif any(k in text for k in ["soon", "today", "important"]):
        urgency = "Medium"
    else:
        urgency = "Low"

    # ---------- SUMMARY ----------
    # Create a short summary from the message.
    summary = message.strip()  # remove spaces at the start/end
    summary = re.sub(r"\s+", " ", summary)  # replace many spaces/newlines with a single space
    summary = summary[:140] + ("..." if len(summary) > 140 else "")  # cut to 140 chars max

    # ---------- SUGGESTED ACTION ----------
    # Suggest what the support team should do next.
    suggested_action = (
        "Ask for reproduction steps and screenshots, then assign to support/engineering."
        if category == "Bug"
        else "Ask for more details and provide next steps."
    )

    # ---------- DRAFT REPLY ----------
    # A ready-to-send reply template to the user.
    draft_reply = (
        "Thanks for reaching out. We received your ticket and are looking into it. "
        "Could you share more details (steps you took, screenshots, and the exact error message) "
        "so we can help faster?"
    )

    # Return the AI result in a dictionary (JSON-like format)
    return {
        "summary": summary or "User reported an issue.",  # if summary is empty, use a default
        "category": category,
        "urgency": urgency,
        "suggested_action": suggested_action,
        "draft_reply": draft_reply,
    }


# This is the main function your API should call.
# It generates the AI output and then validates it to make sure it is correct.
def analyze_ticket(title: str, message: str) -> dict:
    # Step 1: generate AI-like result using local rules
    raw = analyze_ticket_locally(title, message)

    # Step 2: validate result to guarantee it has all required fields
    validated = validate_ai_result(raw)

    # Step 3: convert the validated object back into normal JSON/dict
    return validated.model_dump()