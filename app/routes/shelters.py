from fastapi import APIRouter
from app.models import Shelter, ShelterBase
from app.database import Session


def shelters_router():
    router = APIRouter()

    @router.get("/shelters")
    async def get_shelters():
        try:
            session = Session()
            shelters = session.query(Shelter).all()
        except Exception as e:
            return ("Failed to get shelters:", str(e))
        return shelters

    @router.get("/shelters/{id}")
    async def get_shelter(id: int):
        try:
            session = Session()
            shelter = session.query(Shelter).filter(Shelter.id == id).first()
        except Exception as e:
            return ("Failed to get shelter:", str(e))
        return shelter

    @router.post("/shelters")
    async def create_shelter(shelter: ShelterBase):
        db_shelter = Shelter(
            name=shelter.name, description=shelter.description, address=shelter.address
        )
        try:
            session = Session()
            session.add(db_shelter)
            session.commit()
        except Exception as e:
            return ("Failed to register shelter:", str(e))

        return shelter

    @router.put("/shelters/{id}")
    async def update_shelter(id: int, shelter: ShelterBase):
        try:
            session = Session()
            shelter_db = session.query(Shelter).filter(Shelter.id == id).first()
            shelter_db.name = shelter.name
            shelter_db.description = shelter.description
            shelter_db.address = shelter.address
            session.commit()
        except Exception as e:
            return ("Failed to update shelter:", str(e))

        return shelter

    @router.delete("/shelters/{id}")
    async def delete_shelter(id: int):
        try:
            session = Session()
            shelter = session.query(Shelter).filter(Shelter.id == id).first()
            session.delete(shelter)
            session.commit()
        except Exception as e:
            return ("Failed to delete shelter:", str(e))

        return {"message": "Shelter deleted successfully"}

    return router
