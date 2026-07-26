from nba_data import get_team_games

teams = {
    "warriors": "1610612744",
    "lakers": "1610612747",
    "celtics": "1610612738",
    "heat": "1610612748",
    "mavericks": "1610612742"
}

for name, team_id in teams.items():

    print(f"Downloading {name}...")

    data = get_team_games(team_id)

    data.to_csv(
        f"{name}_games.csv",
        index=False
    )

    print(f"{name} saved!")