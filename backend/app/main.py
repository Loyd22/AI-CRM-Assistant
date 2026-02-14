from fastapi import FastAPI  
from fastapi.middleware.cors import CORSMiddleware
from app.db.init_db import init_db


# This is the "router registry" for version v1 of your api. You can add more routers here as you create them.
from app.api.v1.api import api_router

# Create the FastAPI application instance
app = FastAPI(
    title="Backend API",
    version="1.0.0",
)

# CORS = Cross-Origin Resource Sharing
# This allows your frontend (running on another port/domain)
# to call your backend without being blocked by the browser.
# Replace / add origins based on where your frontend runs.
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",

]

# Add CORS middleware to the FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,         # which frontend origins are allowed
    allow_credentials=True,        # allow cookies/auth headers if needed
    allow_methods=["*"],           # allow all HTTP methods (GET/POST/PUT/DELETE)
    allow_headers=["*"],           # allow all request headers
)

# Mount the v1 router into the app with the prefix /api/v1
# This means routes registered in api_router will become:
# /api/v1/<route>
app.include_router(api_router, prefix="/api/v1")



@app.on_event("startup")
def on_startup():
    """Actions to perform on application startup."""
    init_db()  # Initialize the database (create tables, etc.)