import os


# DATABASE_URL tells the backend where the database is.
# If DATABASE_URL is not set, we use a local SQLite file: backend/app.db
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

