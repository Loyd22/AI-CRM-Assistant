from app.db.session import SessionLocal  # Import the function/class that creates a new database session (connection)

def get_db():  # Dependency function FastAPI will use to provide a DB session to your routes
    db = SessionLocal()  # Create/open a new DB session for this request
    try:
        yield db  # Give the DB session to the route (route uses it to query/insert/update)
    finally:
        db.close()  # Always close the session after the request (prevents connection leaks)