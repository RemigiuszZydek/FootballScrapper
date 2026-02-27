from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base

class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer,primary_key=True)

    league_id = Column(Integer, ForeignKey("leagues.id"))
    home_team_id = Column(Integer, ForeignKey("teams.id"))
    away_team_id = Column(Integer, ForeignKey("teams.id"))

    match_date = Column(DateTime)

    home_score = Column(Integer)
    away_score = Column(Integer)

    home_shots_on_target = Column(Integer)
    away_shots_on_target = Column(Integer)

    home_possession = Column(Integer)
    away_possession = Column(Integer)

    home_corners = Column(Integer)
    away_corners = Column(Integer)

    home_yellow_cards = Column(Integer)
    away_yellow_cards = Column(Integer)

    league = relationship("League")
    home_team = relationship("Team", foreign_keys=[home_team_id])
    away_team = relationship("Team", foreign_keys=[away_team_id])