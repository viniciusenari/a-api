import hashlib

from fastapi import APIRouter, Depends, HTTPException
from app.database import Session
from app.models import User, UserBase, UserBaseInDB, UserInDB
from app.routes.auth import get_current_user


def tutors_router():
    router = APIRouter()

    @router.get("/tutors")
    async def get_tutors(current_user: UserInDB = Depends(get_current_user)):
        try:
            session = Session()
            tutors = session.query(User).all()
        except Exception as e:
            return ("Failed to get tutors:", str(e))
        return tutors

    @router.get("/tutors/{id}")
    async def get_tutor(id: int, current_user: UserInDB = Depends(get_current_user)):
        try:
            session = Session()
            tutor = session.query(User).filter(User.id == id).first()
        except Exception as e:
            return ("Failed to get tutor:", str(e))
        return tutor

    @router.post("/tutors")
    async def create_tutor(
        user: UserBaseInDB, current_user: UserInDB = Depends(get_current_user)
    ):
        username = user.username
        email = user.email
        password = user.hashed_password
        hashed_password = hashlib.sha256(password.encode("utf-8")).hexdigest()

        session = Session()
        user = session.query(UserInDB).filter(UserInDB.username == username).first()
        if user:
            raise HTTPException(status_code=400, detail="Username already registered")
        
        user = UserInDB(username=username, email=email, hashed_password=hashed_password)

        try:
            session = Session()
            session.add(user)
            session.commit()
        except Exception as e:
            return ("Failed to register user:", str(e))

        return UserBase(username=username, email=email)

    @router.put("/tutors/{id}")
    async def update_tutor(
        id: int, user: UserBaseInDB, current_user: UserInDB = Depends(get_current_user)
    ):
        try:
            session = Session()
            tutor = session.query(User).filter(User.id == id).first()
            tutor.username = user.username
            tutor.email = user.email
            tutor.hashed_password = user.hashed_password
            session.commit()
        except Exception as e:
            return ("Failed to update tutor", str(e))
        return "Updated tutor"

    @router.delete("/tutors/{id}")
    async def delete_tutor(id: int, current_user: UserInDB = Depends(get_current_user)):
        try:
            session = Session()
            tutor = session.query(User).filter(User.id == id).first()
            session.delete(tutor)
            session.commit()
        except Exception as e:
            return ("Failed to delete tutor", str(e))
        return "Deleted tutor"

    return router
