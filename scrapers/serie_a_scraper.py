import requests
from .scrape_utils import create_driver, stats_scraping
from sqlalchemy.orm import Session
from db.save_to_db import save_match
from db.database import SessionLocal
import csv
import time
import random


def slugify(name):
    return name.lower().replace(" ", "-")


URL = "https://prod-cdn-public-api.livescore.com/v1/api/app/competition/77/details/1/?locale=en"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.livescore.com/"
}

response = requests.get(URL, headers=headers)

print("Status:", response.status_code)

data = response.json()

events = data["Stages"][0]["Events"]

session : Session = SessionLocal()

for event in events:
    try:
        eid = event["Eid"]
        home = event["T1"][0]["Nm"]
        away = event["T2"][0]["Nm"]
        status = event.get("Eps", "Unknown") 

        home_score = event.get("Tr1")
        away_score = event.get("Tr2")

        if home_score is None or away_score is None:
            continue

        home_slug = slugify(home)
        away_slug = slugify(away)

        match_url = f"https://www.livescore.com/en/football/italy/serie-a/{home_slug}--vs--{away_slug}/{eid}"
        
        match_stats = stats_scraping(match_url)

        match_stats.update({
            "home_score": home_score,
            "away_score": away_score
        })

        save_match(
            session=session,
            league_name="Serie A",
            home_team_name=home,
            away_team_name=away,
            match_date=match_stats["match_date"],
            stats=match_stats
        )
        time.sleep(random.uniform(1,3))
        print("kolejny")
    except Exception as e:
        print(f"Nie udało się pobrać meczu  {eid}: {e}")
        continue