from typing import Annotated
from datetime import datetime, timedelta
import hashlib
import jwt

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.database import Session
from app.models import UserInDB, UserBaseInDB


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def authenticate_user(username: str, password: str):
    session = Session()
    user = session.query(UserInDB).filter(UserInDB.username == username).first()
    if not user:
        return False
    if not user.hashed_password == hashlib.sha256(password.encode("utf-8")).hexdigest():
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, "secret", algorithm="HS256")
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, "secret", algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=401, detail="Invalid authentication credentials"
            )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials"
        )
    session = Session()
    user = session.query(UserInDB).filter(UserInDB.username == username).first()
    if user is None:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials"
        )
    return user


def token_router():
    router = APIRouter()

    @router.post("/token")
    async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
        user = authenticate_user(form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=400, detail="Incorrect username or password"
            )
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

    return router


def auth_router():
    router = APIRouter()

    @router.post("/register")
    async def register(user: UserBaseInDB):
        username = user.username
        email = user.email
        password = user.hashed_password

        hashed_password = hashlib.sha256(password.encode("utf-8")).hexdigest()
        user = UserInDB(username=username, email=email, hashed_password=hashed_password)
        try:
            session = Session()
            session.add(user)
            session.commit()
        except Exception as e:
            print("Failed to register user:", str(e))

    @router.get("/current_user")
    async def current_user(current_user: UserInDB = Depends(get_current_user)):
        return current_user

    return router
