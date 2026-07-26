from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.endpoints import commonplayerinfo
from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog
import pandas as pd
import time


def get_team_games(team_id):

    try:
        time.sleep(1)

        games = leaguegamefinder.LeagueGameFinder(
            team_id_nullable=team_id,
            timeout=60
        )

        games_df = games.get_data_frames()[0]

        return games_df

    except Exception as e:
        print("Team data error:", e)
        return pd.DataFrame()



def search_player(player_name):

    all_players = players.get_players()

    results = [
        player for player in all_players
        if player_name.lower() in player["full_name"].lower()
    ]

    return results



def get_player_info(player_id):

    try:

        info = commonplayerinfo.CommonPlayerInfo(
            player_id=player_id,
            timeout=60
        )

        return info.get_data_frames()[0]

    except Exception as e:
        print("Player info error:", e)
        return pd.DataFrame()



def get_player_games(player_id):

    try:

        games = playergamelog.PlayerGameLog(
            player_id=player_id,
            timeout=60
        )

        return games.get_data_frames()[0]

    except Exception as e:
        print("Player games error:", e)
        return pd.DataFrame()



if __name__ == "__main__":

    warriors = get_team_games("1610612744")

    print(warriors.head())
