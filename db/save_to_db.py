from sqlalchemy.orm import Session
from datetime import datetime
from .leagues import League
from .matches import Match
from .teams import Team

def save_match(session: Session,external_id:str, league_name:str, home_team_name:str, away_team_name:str, match_date: datetime, stats:dict):
    league = session.query(League).filter_by(name=league_name).first()
    if not league:
        league = League(name=league_name)
        session.add(league)
        session.flush()

    home_team = session.query(Team).filter_by(name=home_team_name).first()
    if not home_team:
        home_team = Team(name=home_team_name)
        session.add(home_team)
        session.flush()
    
    away_team = session.query(Team).filter_by(name=away_team_name).first()
    if not away_team:
        away_team = Team(name=away_team_name)
        session.add(away_team)
        session.flush()

    existing_match = session.query(Match).filter(Match.home_team_id == home_team.id, Match.away_team_id == away_team.id, Match.match_date == match_date).first()

    if existing_match:
        print(f"Mecz {home_team_name} vs {away_team_name} już istnieje w bazie.")
        return existing_match
    
    new_match = Match(
        league_id = league.id,
        home_team_id = home_team.id,
        away_team_id = away_team.id,
        match_date = match_date,
        home_score = stats.get("home_score"),
        away_score = stats.get("away_score"),
        home_shots_on_target=stats.get("home_shots_on_target"),
        away_shots_on_target=stats.get("away_shots_on_target"),
        home_possession=stats.get("home_possession"),
        away_possession=stats.get("away_possession"),
        home_corners=stats.get("home_corners"),
        away_corners=stats.get("away_corners"),
        home_yellow_cards=stats.get("home_yellow_cards"),
        away_yellow_cards=stats.get("away_yellow_cards")
    )

    session.add(new_match)
    session.commit()
    print(f"Dodano mecz {home_team_name} vs {away_team_name} do bazy.")
    return new_match
    
    