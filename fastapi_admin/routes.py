from fastapi import APIRouter

router = APIRouter()

# Placeholder route for admin health check or demo
@router.get("/admin/ping", tags=["admin"])
async def admin_ping():
    return {"message": "Admin is alive"}
