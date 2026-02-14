from sqlalchemy.orm import declarative_base

# Base = parent class of all your models (tables)
Base = declarative_base()

# We import models here so SQLAlchemy can "see" them.
# If we don’t import them, create_all might create nothing.
from app.models.user import User  # noqa
from app.models.lead import Lead  # noqa
from app.models.ticket import Ticket  # noqa
from app.models.ai_analysis import AIAnalysis  # noqa