from fastapi import APIRouter
from app.database import test_db_connection


def healthcheck_router():
    router = APIRouter()

    @router.get("/healthcheck")
    async def healthcheck():
        test_db_connection()
        return {"message": "Healthy"}

    @router.get("/healthcheck/db")
    async def healthcheck_db():
        return test_db_connection()

    return router
