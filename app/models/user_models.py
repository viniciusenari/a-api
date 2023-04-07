from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)

    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, email={self.email})"


class UserInDB(User):
    hashed_password = Column(String)


class UserBase(BaseModel):
    username: str
    email: str

    class Config:
        orm_mode = True


class UserBaseInDB(UserBase):
    hashed_password: str
