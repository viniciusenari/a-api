from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from pydantic import BaseModel

Base = declarative_base()


class Shelter(Base):
    __tablename__ = "shelters"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    address = Column(String)


class ShelterBase(BaseModel):
    id: int
    name: str
    description: str
    address: str

    class Config:
        orm_mode = True


class Pet(Base):
    __tablename__ = "pets"

    id = Column(Integer, primary_key=True)
    shelter_id = Column(Integer, ForeignKey("shelters.id"))
    description = Column(String)
    adopted = Column(Boolean)
    age = Column(String)
    address = Column(String)
    image = Column(String)

    shelter = relationship("Shelter", backref="pets")


class PetBase(BaseModel):
    shelter_id: int
    description: str
    adopted: bool
    age: str
    address: str
    image: str

    class Config:
        orm_mode = True
