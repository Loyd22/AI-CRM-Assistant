from fastapi import APIRouter

# A router is a mini "collection of endpoints" you can plug into the app
router = APIRouter(tags=["health"])

# This endpoint is used to confirm the backend is alive.
# When you call GET /api/v1/health, it should return {"status": "ok"}.
@router.get("/health")
def health():
    return {"status": "ok"}