from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.repositories.tickets_repo import TicketsRepo
from app.repositories.ai_analysis_repo import AIAnalysisRepo
from app.services.automation_rules import AutomationRules
from app.services.ai_prompt import build_ticket_analysis_prompt
from app.services.ai_client import call_openai_structured
from app.services.ai_validator import validate_analysis

router = APIRouter()


@router.post("/tickets/{ticket_id}/analyze")
def analyze_ticket_endpoint(ticket_id: int, db: Session = Depends(get_db)):
    # 1) Fetch ticket
    ticket = TicketsRepo.get_by_id(db, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    # 2) Build prompt
    prompt = build_ticket_analysis_prompt(ticket.title, ticket.message, ticket.status)

    # 3) Call OpenAI once + 4) validate
    try:
        raw = call_openai_structured(prompt)
        result = validate_analysis(raw)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"AI analysis failed: {str(e)}",
        )

    # 5) Save analysis
    AIAnalysisRepo.create_for_ticket(db=db, ticket_id=ticket_id, ai_result=result)

    # 6) Apply automation rules
    AutomationRules.apply(
        ticket=ticket,
        category=result.get("category"),
        urgency=result.get("urgency"),
    )

    # 7) Commit
    db.commit()
    db.refresh(ticket)

    # 8) Return
    return result