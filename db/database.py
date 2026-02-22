from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATBASE_URL = "sqlite:///livescore.db"

engine = create_engine(DATBASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()
