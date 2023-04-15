from fastapi import APIRouter
from app.database import Session
from app.models import Pet, PetBase


def pets_router():
    router = APIRouter()

    @router.get("/pets")
    async def get_pets():
        try:
            session = Session()
            pets = session.query(Pet).all()
        except Exception as e:
            return ("Failed to get pets:", str(e))
        return pets
    
    @router.get("/pets/{id}")
    async def get_pet(id: int):
        try:
            session = Session()
            pet = session.query(Pet).filter(Pet.id == id).first()
        except Exception as e:
            return ("Failed to get pet:", str(e))
        return pet

    @router.post("/pets")
    async def create_pet(pet: PetBase):
        pet_db = Pet(
            shelter_id=pet.shelter_id,
            description=pet.description,
            adopted=pet.adopted,
            age=pet.age,
            address=pet.address,
            image=pet.image,
        )
        try:
            session = Session()
            session.add(pet_db)
            session.commit()
        except Exception as e:
            return ("Failed to register pet:", str(e))

        return pet
    
    @router.put("/pets/{id}")
    async def update_pet(id: int, pet: PetBase):
        try:
            session = Session()
            pet_db = session.query(Pet).filter(Pet.id == id).first()
            pet_db.shelter_id = pet.shelter_id
            pet_db.description = pet.description
            pet_db.adopted = pet.adopted
            pet_db.age = pet.age
            pet_db.address = pet.address
            pet_db.image = pet.image
            session.commit()
        except Exception as e:
            return ("Failed to update pet:", str(e))

        return pet
    
    @router.delete("/pets/{id}")
    async def delete_pet(id: int):
        try:
            session = Session()
            pet = session.query(Pet).filter(Pet.id == id).first()
            session.delete(pet)
            session.commit()
        except Exception as e:
            return ("Failed to delete pet:", str(e))

        return "Pet deleted"
    
    return router

def adoption_router():
    router = APIRouter()

    @router.post("/adoption/{pet_id}")
    async def adoption_pet(pet_id: int):
        try:
            session = Session()
            pet = session.query(Pet).filter(Pet.id == pet_id).first()
            if pet.adopted:
                return "Pet already adopted"
            pet.adopted = True
            session.commit()
        except Exception as e:
            return ("Failed to adoption pet:", str(e))

        return {
            "adoption": "success",
            "pet": PetBase.from_orm(pet).dict()
        }
    
    @router.delete("/adoption/{pet_id}")
    async def return_pet(pet_id: int):
        try:
            session = Session()
            pet = session.query(Pet).filter(Pet.id == pet_id).first()
            if not pet.adopted:
                return "Pet not adopted"
            pet.adopted = False
            session.commit()
        except Exception as e:
            return ("Failed to return pet:", str(e))

        return {
            "return": "success",
            "pet": PetBase.from_orm(pet).dict()
        }

    return router