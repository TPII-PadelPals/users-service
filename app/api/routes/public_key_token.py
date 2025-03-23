from fastapi import APIRouter

router = APIRouter()


@router.post("/", response_model=str)
async def generate_token():
    return ""
