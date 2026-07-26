from nba_api.stats.endpoints import commonplayerinfo
from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog
import pandas as pd


def get_team_games(team_id):

    files = {
        "1610612744": "warriors_games.csv",
        "1610612747": "lakers_games.csv",
        "1610612738": "celtics_games.csv",
        "1610612748": "heat_games.csv",
        "1610612742": "mavericks_games.csv"
    }

    return pd.read_csv(files[team_id])


def search_player(player_name):

    all_players = players.get_players()

    results = [
        player for player in all_players
        if player_name.lower() in player["full_name"].lower()
    ]

    return results


def get_player_info(player_id):

    player_info = {
        2544: {
            "NAME": "LeBron James",
            "TEAM": "Los Angeles Lakers",
            "POSITION": "Forward",
            "HEIGHT": "6-9",
            "WEIGHT": "250"
        }
    }

    if player_id in player_info:
        return pd.DataFrame([player_info[player_id]])

    return pd.DataFrame(
        {
            "Message": [
                "Player information not available"
            ]
        }
    )


def get_player_games(player_id):

    if player_id == 2544:

        return pd.DataFrame(
            {
                "GAME_DATE": [
                    "2026-01-01",
                    "2026-01-05",
                    "2026-01-10"
                ],
                "PTS": [
                    25,
                    30,
                    22
                ],
                "REB": [
                    8,
                    7,
                    10
                ],
                "AST": [
                    9,
                    6,
                    8
                ],
                "MIN": [
                    35,
                    34,
                    36
                ]
            }
        )

    return pd.DataFrame()


if __name__ == "__main__":

    warriors = get_team_games("1610612744")

    print(warriors.head())