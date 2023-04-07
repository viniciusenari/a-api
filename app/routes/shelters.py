from fastapi import APIRouter


def shelters_router():
    router = APIRouter()

    @router.get("/shelters")
    async def get_shelters():
        return {"message": "Hello World"}

    return router
