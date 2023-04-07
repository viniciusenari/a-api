from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

Base = declarative_base()


class Pet(Base):
    __tablename__ = "pets"

    id = Column(Integer, primary_key=True)
    shelter_id = Column(Integer, ForeignKey("shelters.id"))
    description = Column(String)
    adopted = Column(Boolean)
    age = Column(String)
    address = Column(String)
    image = Column(String)


class PetBase(BaseModel):
    id: int
    shelter_id: int
    description: str
    adopted: bool
    age: str
    address: str
    image: str

    class Config:
        orm_mode = True