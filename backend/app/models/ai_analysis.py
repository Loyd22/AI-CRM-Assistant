from sqlalchemy import Column, Integer, String, Text
from app.db.base import Base

class AIAnalysis(Base):
    __tablename__ = "ai_analyses"

    id = Column(Integer, primary_key=True, index=True)
    entity_type = Column(String, nullable=False)  # ex: "ticket" or "lead"
    entity_id = Column(Integer, nullable=False)
    result = Column(Text, nullable=True)          # stored AI output text