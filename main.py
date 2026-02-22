from db.database import Base, engine
from db.teams import Team
from db.leagues import League
from db.matches import Match

def create_tables():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_tables()