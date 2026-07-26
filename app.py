import streamlit as st
import pandas as pd
from nba_data import (
    get_team_games,
    search_player,
    get_player_info,
    get_player_games
)

st.set_page_config(
    page_title="NBA Analytics Dashboard",
    page_icon="🏀",
    layout="wide"
)

st.title("🏀 NBA Analytics Dashboard")

st.write(
    """
    Welcome to the NBA Analytics Dashboard.
    
    This application uses the NBA API to display team statistics,
    player information, and performance analysis.
    """
)

st.sidebar.header("Navigation")

page = st.sidebar.selectbox(
    "Choose a page",
    [
        "Home",
        "Team Analysis",
        "Player Search",
        "Player Comparison",
        "Statistics",
        "About"
    ]
)


if page == "Home":

    st.subheader("🏀 NBA Analytics Dashboard")

    st.write(
        """
        Explore NBA team and player performance using live NBA API data.

        Features:
        - Team game analysis
        - Player search
        - Player comparisons
        - Statistical charts
        """
    )

    st.info(
        "Use the sidebar to navigate through the dashboard."
    )


elif page == "Team Analysis":

    st.subheader("🏀 Team Analysis")

    teams = {
        "Golden State Warriors": "1610612744",
        "Los Angeles Lakers": "1610612747",
        "Boston Celtics": "1610612738",
        "Miami Heat": "1610612748",
        "Dallas Mavericks": "1610612742"
    }

    selected_team = st.selectbox(
        "Select a Team",
        list(teams.keys())
    )

    team_id = teams[selected_team]

    if st.button("Load Team Data"):

        data = get_team_games(team_id)

        if data.empty:
          st.error("Unable to load NBA data. Please try again later.")

        else:
          st.subheader(selected_team)

          st.dataframe(
              data[
                  [
                      "GAME_DATE",
                      "MATCHUP",
                      "WL",
                      "PTS",
                      "PLUS_MINUS"
            ]
        ]
    )



elif page == "Player Search":

    st.subheader("🏀 Player Search")

    player_name = st.text_input(
        "Enter player name"
    )

    if player_name:

        results = search_player(player_name)

        if results:

            st.write("Search Results:")

            for player in results:

                st.write(
                    f"**{player['full_name']}** "
                    f"- ID: {player['id']}"
                )

                if st.button(
                    f"View {player['full_name']} Info",
                    key=str(player["id"]) + "_info"
                ):

                    info = get_player_info(
                        player["id"]
                    )

                    st.dataframe(info)


                if st.button(
                    f"View {player['full_name']} Game Stats",
                    key=str(player["id"]) + "_games"
                ):

                    games = get_player_games(
                        player["id"]
                    )

                    st.subheader("Recent Game Statistics")

                    st.dataframe(
                        games[
                            [
                                "GAME_DATE",
                                "MATCHUP",
                                "MIN",
                                "PTS",
                                "REB",
                                "AST"
                            ]
                        ]
                    )

                    st.subheader("Points Per Game")

                    chart_data = games[
                        [
                            "GAME_DATE",
                            "PTS"
                        ]
                    ]

                    chart_data = chart_data.set_index("GAME_DATE")

                    st.line_chart(chart_data)

        else:

            st.warning("No players found.")

elif page == "Player Comparison":

    st.subheader("🏀 Player Comparison")

    player1 = st.text_input(
        "Enter first player"
    )

    player2 = st.text_input(
        "Enter second player"
    )


    if st.button("Compare Players"):

        player1_results = search_player(player1)
        player2_results = search_player(player2)


        if player1_results and player2_results:

            player1_id = player1_results[0]["id"]
            player2_id = player2_results[0]["id"]


            player1_games = get_player_games(
                player1_id
            )

            player2_games = get_player_games(
                player2_id
            )


            comparison = pd.DataFrame(
                {
                    "Player": [
                        player1_results[0]["full_name"],
                        player2_results[0]["full_name"]
                    ],

                    "Average Points": [
                        round(player1_games["PTS"].mean(), 2),
                        round(player2_games["PTS"].mean(), 2)
                    ],

                    "Average Rebounds": [
                        round(player1_games["REB"].mean(), 2),
                        round(player2_games["REB"].mean(), 2)
                    ],

                    "Average Assists": [
                        round(player1_games["AST"].mean(), 2),
                        round(player2_games["AST"].mean(), 2)
                    ]
                }
            )


            st.dataframe(comparison)


            st.subheader("Points Comparison")

            chart = comparison.set_index(
                "Player"
            )["Average Points"]

            st.bar_chart(chart)


        else:

            st.warning(
                "Could not find one or both players."
            )

elif page == "Statistics":

    st.subheader("📊 Team Statistics")

    st.info("Select an NBA team and generate statistics to view performance data.")

    teams = {
        "Golden State Warriors": "1610612744",
        "Los Angeles Lakers": "1610612747",
        "Boston Celtics": "1610612738",
        "Miami Heat": "1610612748",
        "Dallas Mavericks": "1610612742"
    }

    selected_team = st.selectbox(
        "Select a team for statistics",
        list(teams.keys())
    )

    if st.button("Generate Statistics"):

        team_data = get_team_games(
            teams[selected_team]
        )

        if team_data.empty:
           st.error("Unable to load NBA statistics.")
           st.stop()

        st.success("Statistics generated successfully!")

        st.subheader(selected_team)

        # Metrics
        total_games = len(team_data)

        average_points = round(
            team_data["PTS"].mean(),
            2
        )

        average_plus_minus = round(
            team_data["PLUS_MINUS"].mean(),
            2
        )

        wins = len(
            team_data[
                team_data["WL"] == "W"
            ]
        )

        win_percentage = round(
            (wins / total_games) * 100,
            2
        )


        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Games Played",
            total_games
        )

        col2.metric(
            "Average Points",
            average_points
        )

        col3.metric(
            "Avg +/-",
            average_plus_minus
        )

        col4.metric(
            "Win %",
            f"{win_percentage}%"
        )


        # Checkbox requirement
        show_data = st.checkbox(
            "Show game-by-game statistics"
        )

        if show_data:
            st.dataframe(team_data)


        st.subheader("Points Over Games")

        chart = team_data[
            [
                "GAME_DATE",
                "PTS"
            ]
        ]

        chart = chart.set_index(
            "GAME_DATE"
        )

        st.line_chart(chart)


elif page == "About":

    st.subheader("ℹ️ About This Project")

    st.write(
        """
        NBA Analytics Dashboard

        Built with:
        - Python
        - Streamlit
        - NBA API

        This application retrieves NBA data and
        displays team and player performance
        through tables, metrics, and charts.
        """
    )
