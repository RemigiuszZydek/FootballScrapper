from sqlalchemy import Column, Integer, String
from .database import Base

class League(Base):
    __tablename__ = "leagues"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)