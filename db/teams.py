from sqlalchemy import Column, Integer, String
from .database import Base

class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer,primary_key=True)
    name = Column(String, unique=True, nullable=False)