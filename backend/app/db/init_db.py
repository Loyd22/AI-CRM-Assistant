from app.db.session import engine 
from app.db.base import Base  # Import the Base class for models


def init_db():
    
     # This creates all tables that exist in your models.
    # If tables already exist, it will NOT delete them.
    Base.metadata.create_all(bind=engine) # Create all tables in the database