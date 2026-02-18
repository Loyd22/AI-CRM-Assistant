from fastapi import APIRouter
from app.api.v1.routes_tickets import router as tickets_router

# Import the health router (a group of routes)
from app.api.v1.routes_health import router as health_router
from app.api.v1.routes_ai import router as ai_router 
from app.api.v1.routes_ai_analysis import router as ai_analysis_router
# api_router is the main router for all v1 endpoints
api_router = APIRouter()

# Register health routes into the v1 router
# This adds: GET /health (but it becomes /api/v1/health because of main.py prefix)
api_router.include_router(health_router)
api_router.include_router(tickets_router, prefix="/tickets", tags=["tickets"])


api_router.include_router(ai_router, tags=["ai"])
api_router.include_router(ai_analysis_router, tags=["ai-analysis"])