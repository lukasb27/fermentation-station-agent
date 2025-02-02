from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def get_temp():
    return {"status": "ok"}
