from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.endpoints import commonplayerinfo
from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog


def get_team_games(team_id):
    games = leaguegamefinder.LeagueGameFinder(
        team_id_nullable=team_id
    )

    games_df = games.get_data_frames()[0]

    return games_df


def search_player(player_name):
    all_players = players.get_players()

    results = [
        player for player in all_players
        if player_name.lower() in player["full_name"].lower()
    ]

    return results


def get_player_info(player_id):
    info = commonplayerinfo.CommonPlayerInfo(
        player_id=player_id
    )

    return info.get_data_frames()[0]


def get_player_games(player_id):

    games = playergamelog.PlayerGameLog(
        player_id=player_id
    )

    return games.get_data_frames()[0]

if __name__ == "__main__":

    warriors = get_team_games("1610612744")

    print(warriors.head())