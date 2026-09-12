import streamlit as st

from services.database_service import get_table_data
from utils.db_connection import get_connection


st.title("🏏 Top Cricket Statistics")
st.write("Explore player and team statistics from the database.")


# ============================================================
# Load database tables
# ============================================================

players = get_table_data("players")
batting = get_table_data("batting")
bowling = get_table_data("bowling")
teams = get_table_data("teams")


# ============================================================
# KPI SECTION
# ============================================================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Players",
    len(players[1]),
)

col2.metric(
    "Total Teams",
    len(teams[1]),
)

col3.metric(
    "Batting Records",
    len(batting[1]),
)

col4.metric(
    "Bowling Records",
    len(bowling[1]),
)


st.divider()


# ============================================================
# TOP BATSMEN
# ============================================================

st.subheader("🏏 Top Run Scorers")

top_batsmen_query = """
SELECT
    p.player_name,
    SUM(b.runs) AS total_runs
FROM batting b
JOIN players p
    ON b.player_id = p.player_id
GROUP BY
    p.player_id,
    p.player_name
ORDER BY total_runs DESC
LIMIT 10;
"""

connection = get_connection()

top_batsmen = connection.execute(
    top_batsmen_query
).fetchall()

connection.close()


if top_batsmen:
    st.dataframe(
        top_batsmen,
        use_container_width=True,
    )
else:
    st.info("No batting data available.")


st.divider()


# ============================================================
# TOP BOWLERS
# ============================================================

st.subheader("🎯 Top Wicket Takers")

top_bowlers_query = """
SELECT
    p.player_name,
    SUM(b.wickets) AS total_wickets
FROM bowling b
JOIN players p
    ON b.player_id = p.player_id
GROUP BY
    p.player_id,
    p.player_name
ORDER BY total_wickets DESC
LIMIT 10;
"""

connection = get_connection()

top_bowlers = connection.execute(
    top_bowlers_query
).fetchall()

connection.close()


if top_bowlers:
    st.dataframe(
        top_bowlers,
        use_container_width=True,
    )
else:
    st.info("No bowling data available.")


st.divider()


# ============================================================
# HIGHEST INDIVIDUAL SCORES
# ============================================================

st.subheader("🔥 Highest Individual Scores")

highest_scores_query = """
SELECT
    p.player_name,
    MAX(b.runs) AS highest_score
FROM batting b
JOIN players p
    ON b.player_id = p.player_id
GROUP BY
    p.player_id,
    p.player_name
ORDER BY highest_score DESC
LIMIT 10;
"""

connection = get_connection()

highest_scores = connection.execute(
    highest_scores_query
).fetchall()

connection.close()


if highest_scores:
    st.dataframe(
        highest_scores,
        use_container_width=True,
    )
else:
    st.info("No score data available.")