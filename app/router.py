from fastapi import APIRouter

from app.routes import auth_router, token_router

router = APIRouter()
router.include_router(token_router(), prefix="", tags=["token"])
router.include_router(auth_router(), prefix="/v1", tags=["auth"])
