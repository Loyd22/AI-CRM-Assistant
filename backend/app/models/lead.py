from sqlalchemy import Column, Integer, String
from app.db.base import Base

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    status = Column(String, nullable=True)