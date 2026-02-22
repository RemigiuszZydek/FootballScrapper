import requests

URL = "https://prod-cdn-public-api.livescore.com/v1/api/app/competition/77/details/1/?locale=en"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.livescore.com/"
}

response = requests.get(URL, headers=headers)

print("Status:", response.status_code)

data = response.json()

# Wyciągamy eventy
events = data["Stages"][0]["Events"]

print("Liczba meczy:", len(events))

print("-" * 50)

for event in events:
    eid = event["Eid"]
    home = event["T1"][0]["Nm"]
    away = event["T2"][0]["Nm"]
    status = event.get("Eps", "Unknown")  # status meczu

    # bezpieczne pobieranie wyniku
    home_score = event.get("Tr1")
    away_score = event.get("Tr2")

    # jeśli wynik nie istnieje, ustaw "-"
    if home_score is None or away_score is None:
        continue

    print(f"{home} vs {away}")
    print(f"Wynik: {home_score} - {away_score}")
    print(f"Status: {status}")
    print(f"EID: {eid}")
    print("-" * 50)