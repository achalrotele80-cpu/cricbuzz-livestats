import streamlit as st

from utils.db_connection import get_connection

# ============================================================
# SQL QUERIES
# ============================================================

queries = {

    "Q1 - Indian Players": """
        SELECT
            player_id,
            player_name,
            country,
            role
        FROM players
        WHERE country = 'India';
    """,

    "Q2 - Matches in Last 30 Days": """
        SELECT
            match_id,
            match_date,
            match_type,
            status
        FROM matches
        WHERE match_date >= DATE('now', '-30 days')
        ORDER BY match_date DESC;
    """,

    "Q3 - Top 10 ODI Run Scorers": """
        SELECT
            p.player_id,
            p.player_name,
            SUM(b.runs) AS total_runs
        FROM batting b
        JOIN players p
            ON b.player_id = p.player_id
        JOIN matches m
            ON b.match_id = m.match_id
        WHERE m.match_type = 'ODI'
        GROUP BY
            p.player_id,
            p.player_name
        ORDER BY total_runs DESC
        LIMIT 10;
    """,

    "Q4 - Venues Above 50,000 Capacity": """
        SELECT
            venue_id,
            venue_name,
            city,
            country,
            capacity
        FROM venues
        WHERE capacity > 50000
        ORDER BY capacity DESC;
    """,

    "Q5 - Matches Won by Each Team": """
        SELECT
            t.team_name,
            COUNT(m.match_id) AS matches_won
        FROM teams t
        JOIN matches m
            ON t.team_id = m.winner_team_id
        GROUP BY
            t.team_id,
            t.team_name
        ORDER BY matches_won DESC;
    """,

    "Q6 - Players by Role": """
        SELECT
            role,
            COUNT(*) AS player_count
        FROM players
        GROUP BY role
        ORDER BY player_count DESC;
    """,

    "Q7 - Highest Score by Format": """
        SELECT
            m.match_type,
            MAX(b.runs) AS highest_score
        FROM batting b
        JOIN matches m
            ON b.match_id = m.match_id
        GROUP BY m.match_type
        ORDER BY highest_score DESC;
    """,

    "Q8 - Series Started in 2024": """
        SELECT
            series_id,
            series_name,
            host_country,
            match_type,
            start_date,
            total_matches
        FROM series
        WHERE start_date >= '2024-01-01'
          AND start_date < '2025-01-01'
        ORDER BY start_date;
    """,

    "Q9 - Player Batting Statistics": """
        SELECT
            p.player_name,
            COUNT(b.batting_id) AS innings,
            SUM(b.runs) AS total_runs,
            AVG(b.runs) AS average_runs
        FROM players p
        JOIN batting b
            ON p.player_id = b.player_id
        GROUP BY
            p.player_id,
            p.player_name
        ORDER BY total_runs DESC;
    """,

    "Q10 - Team Total Runs": """
        SELECT
            t.team_name,
            SUM(b.runs) AS total_runs
        FROM teams t
        JOIN batting b
            ON t.team_id = b.team_id
        GROUP BY
            t.team_id,
            t.team_name
        ORDER BY total_runs DESC;
    """,

    "Q11 - Team Total Wickets": """
        SELECT
            t.team_name,
            SUM(b.wickets) AS total_wickets
        FROM teams t
        JOIN bowling b
            ON t.team_id = b.team_id
        GROUP BY
            t.team_id,
            t.team_name
        ORDER BY total_wickets DESC;
    """,

    "Q12 - Players Above 500 Runs": """
        SELECT
            p.player_name,
            SUM(b.runs) AS total_runs
        FROM players p
        JOIN batting b
            ON p.player_id = b.player_id
        GROUP BY
            p.player_id,
            p.player_name
        HAVING SUM(b.runs) > 500
        ORDER BY total_runs DESC;
    """,

    "Q13 - Players Above 20 Wickets": """
        SELECT
            p.player_name,
            SUM(b.wickets) AS total_wickets
        FROM players p
        JOIN bowling b
            ON p.player_id = b.player_id
        GROUP BY
            p.player_id,
            p.player_name
        HAVING SUM(b.wickets) > 20
        ORDER BY total_wickets DESC;
    """,

    "Q14 - Average Runs by Player": """
        SELECT
            p.player_name,
            AVG(b.runs) AS average_runs
        FROM players p
        JOIN batting b
            ON p.player_id = b.player_id
        GROUP BY
            p.player_id,
            p.player_name
        ORDER BY average_runs DESC;
    """,

    "Q15 - Matches by Venue": """
        SELECT
            v.venue_name,
            COUNT(m.match_id) AS matches_played
        FROM venues v
        JOIN matches m
            ON v.venue_id = m.venue_id
        GROUP BY
            v.venue_id,
            v.venue_name
        ORDER BY matches_played DESC;
    """,

    "Q16 - Matches by Match Type": """
        SELECT
            match_type,
            COUNT(*) AS match_count
        FROM matches
        GROUP BY match_type
        ORDER BY match_count DESC;
    """,

    "Q17 - Players with Batting and Bowling Records": """
        SELECT
            p.player_id,
            p.player_name
        FROM players p
        WHERE p.player_id IN (
            SELECT player_id
            FROM batting
        )
        AND p.player_id IN (
            SELECT player_id
            FROM bowling
        );
    """,

    "Q18 - Highest Score for Each Player": """
        SELECT
            p.player_name,
            MAX(b.runs) AS highest_score
        FROM players p
        JOIN batting b
            ON p.player_id = b.player_id
        GROUP BY
            p.player_id,
            p.player_name
        ORDER BY highest_score DESC;
    """,

    "Q19 - Above Overall Average Runs": """
        SELECT
            p.player_name,
            SUM(b.runs) AS total_runs
        FROM players p
        JOIN batting b
            ON p.player_id = b.player_id
        GROUP BY
            p.player_id,
            p.player_name
        HAVING SUM(b.runs) > (
            SELECT AVG(total_runs)
            FROM (
                SELECT
                    SUM(runs) AS total_runs
                FROM batting
                GROUP BY player_id
            )
        )
        ORDER BY total_runs DESC;
    """,

    "Q20 - Best Bowling Economy": """
        SELECT
            p.player_name,
            AVG(b.economy) AS average_economy,
            SUM(b.wickets) AS total_wickets
        FROM players p
        JOIN bowling b
            ON p.player_id = b.player_id
        GROUP BY
            p.player_id,
            p.player_name
        HAVING SUM(b.wickets) > 0
        ORDER BY average_economy ASC;
    """,
}


# ============================================================
# PAGE HEADER
# ============================================================

st.title("🗄️ SQL Analytics")
st.write(
    "Run SQL-based cricket analytics directly from the database."
)

st.divider()


# ============================================================
# QUERY SELECTION
# ============================================================

selected_question = st.selectbox(
    "Select a SQL Question",
    list(queries.keys()),
)


selected_query = queries[selected_question]


# ============================================================
# DISPLAY SQL
# ============================================================

st.subheader(selected_question)

with st.expander("View SQL Query"):
    st.code(
        selected_query,
        language="sql",
    )


# ============================================================
# RUN QUERY
# ============================================================

if st.button("▶ Run Query"):

    try:
        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(selected_query)

        rows = cursor.fetchall()

        columns = [
            description[0]
            for description in cursor.description
        ]

        connection.close()

        if rows:

            data = [
                dict(zip(columns, row))
                for row in rows
            ]

            st.success(
                f"Query executed successfully — "
                f"{len(data)} record(s) found."
            )

            st.dataframe(
                data,
                use_container_width=True,
            )

        else:

            st.info("No records found.")

    except Exception as error:

        st.error(
            f"Error executing query: {error}"
        )

