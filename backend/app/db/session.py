from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import DATABASE_URL

# SQLite needs this option because FastAPI can use multiple threads.
# Postgres does not need this.
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

# Engine = the main "connection" object to the database
engine = create_engine(DATABASE_URL, connect_args=connect_args)

# SessionLocal = factory that creates DB sessions
# A session is what you use later to run queries (read/write data)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)