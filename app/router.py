from fastapi import APIRouter, Depends
from app.routes.auth import get_current_user

from app.routes import (
    auth_router,
    token_router,
    healthcheck_router,
    tutors_router,
    shelters_router,
)

router = APIRouter()
router.include_router(healthcheck_router(), prefix="/v1", tags=["Healthcheck"])
router.include_router(token_router(), prefix="", tags=["Token"])
router.include_router(auth_router(), prefix="/v1", tags=["Auth"])
router.include_router(
    tutors_router(),
    prefix="/v1",
    tags=["Tutors"],
    dependencies=[Depends(get_current_user)],
)
router.include_router(
    shelters_router(),
    prefix="/v1",
    tags=["Shelters"],
    dependencies=[Depends(get_current_user)],
)
