# ml_basic.py
import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# 1. Ładowanie danych
conn = sqlite3.connect("livescore.db")

df = pd.read_sql_query("""
SELECT 
    m.id,
    m.match_date,
    t1.name AS home_team,
    t2.name AS away_team,
    m.home_team_id,
    m.away_team_id,
    m.home_score,
    m.away_score
FROM matches m
JOIN teams t1 ON m.home_team_id = t1.id
JOIN teams t2 ON m.away_team_id = t2.id
ORDER BY m.match_date
""", conn)

# 2. Obliczenie wyniku meczu (z punktu widzenia gospodarza)
def get_result(row):
    if int(row["home_score"]) > int(row["away_score"]):
        return 1
    elif int(row["home_score"]) < int(row["away_score"]):
        return -1
    else:
        return 0

df["result"] = df.apply(get_result, axis=1)

# 3. Funkcja licząca formę drużyny na podstawie ostatnich n meczów
def calc_team_form(df, team_col, result_col, n_last=5):
    team_history = {}
    form_list = []

    for idx, row in df.iterrows():
        team_id = row[team_col]
        history = team_history.get(team_id, [])

        # średnia z ostatnich n_last meczów
        if len(history) == 0:
            form_list.append(0.0)
        else:
            form_list.append(sum(history[-n_last:]) / min(len(history), n_last))

        # aktualizacja historii
        # jeśli drużyna grała u siebie
        if team_col == "home_team_id":
            res = row[result_col]
            val = 1 if res == 1 else 0.5 if res == 0 else 0
        else:  # drużyna grała na wyjeździe
            res = row[result_col]
            val = 1 if res == -1 else 0.5 if res == 0 else 0

        history.append(val)
        team_history[team_id] = history

    return form_list

df["home_form_5"] = calc_team_form(df, "home_team_id", "result", n_last=5)
df["away_form_5"] = calc_team_form(df, "away_team_id", "result", n_last=5)
df["form_diff"] = df["home_form_5"] - df["away_form_5"]

# 4. Przygotowanie danych do modelu
X = df[["form_diff"]]
y = df["result"]

# 5. Cross-validation
model = RandomForestClassifier(n_estimators=300, random_state=42)

scores = cross_val_score(model, X, y, cv=5, scoring="accuracy")

print("Rozkład klas:")
print(df["result"].value_counts(normalize=True))

print("\nAccuracy dla każdego folda:")
print(scores)

print("\nŚrednia accuracy:")
print(scores.mean())

# 6. Opcjonalnie - train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model.fit(X_train, y_train)
predictions = model.predict(X_test)
print("\nAccuracy (train-test split):", accuracy_score(y_test, predictions))