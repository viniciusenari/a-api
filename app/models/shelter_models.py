from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
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