from fastapi import APIRouter
from app.main.adapter.logger_adapter import logger
from fastapi import APIRouter, Depends
from app.main.adapter.auth import get_current_user

router = APIRouter()

@router.get("/")
# current_user: dict = Depends(get_current_user)
async def hello():
    logger.info("hello route called")
    return {"message": "hello world"}