from pydantic import BaseModel, Field  # Tools that help us check if JSON data is complete and correct


# This class is like a "required form" for the AI output.
# It says: the AI must return these 5 fields, and each one must be non-empty text.
class AIAnalyzeResult(BaseModel):
    summary: str = Field(..., min_length=1)           # must exist, must be text, must not be empty
    category: str = Field(..., min_length=1)          # must exist, must be text, must not be empty
    urgency: str = Field(..., min_length=1)           # must exist, must be text, must not be empty
    suggested_action: str = Field(..., min_length=1)  # must exist, must be text, must not be empty
    draft_reply: str = Field(..., min_length=1)       # must exist, must be text, must not be empty


def validate_ai_result(data: dict) -> AIAnalyzeResult:
    # This function takes raw data (a normal dictionary, like JSON from AI)
    # and checks if it matches the required format above.
    # If it matches, it returns a cleaned/validated AIAnalyzeResult object.
    # If it does NOT match (missing field or empty text), it will throw an error.
    return AIAnalyzeResult.model_validate(data)