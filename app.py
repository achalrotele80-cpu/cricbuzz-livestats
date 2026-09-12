import streamlit as st
import pandas as pd
import plotly.express as px

from utils.db_connection import get_connection

st.set_page_config(
    page_title="Cricbuzz LiveStats",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# DATABASE HELPER
# ============================================================

def get_data(query):
    """Run SQL query and return a DataFrame."""

    connection = get_connection()

    dataframe = pd.read_sql_query(
        query,
        connection,
    )

    connection.close()

    return dataframe


# ============================================================
# HOME DASHBOARD
# ============================================================

def home_page():
    """Display Cricbuzz LiveStats dashboard."""

    st.markdown(
        """
        <style>
        .main-title {
            font-size: 42px;
            font-weight: 700;
            margin-bottom: 0;
        }

        .subtitle {
            font-size: 18px;
            color: #6b7280;
            margin-top: 5px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    st.markdown(
        '<div class="main-title">🏏 Cricbuzz LiveStats</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="subtitle">'
        "Real-Time Cricket Insights & SQL-Based Analytics"
        "</div>",
        unsafe_allow_html=True,
    )

    st.divider()

    # --------------------------------------------------------
    # KPI DATA
    # --------------------------------------------------------

    players_count = get_data(
        "SELECT COUNT(*) AS total FROM players;"
    ).iloc[0]["total"]

    teams_count = get_data(
        "SELECT COUNT(*) AS total FROM teams;"
    ).iloc[0]["total"]

    matches_count = get_data(
        "SELECT COUNT(*) AS total FROM matches;"
    ).iloc[0]["total"]

    total_runs = get_data(
        """
        SELECT COALESCE(SUM(runs), 0) AS total
        FROM batting;
        """
    ).iloc[0]["total"]

    total_wickets = get_data(
        """
        SELECT COALESCE(SUM(wickets), 0) AS total
        FROM bowling;
        """
    ).iloc[0]["total"]

    # --------------------------------------------------------
    # KPI CARDS
    # --------------------------------------------------------

    st.subheader("📊 Cricket Overview")

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "👤 Players",
        f"{int(players_count):,}",
    )

    col2.metric(
        "🏆 Teams",
        f"{int(teams_count):,}",
    )

    col3.metric(
        "🏏 Matches",
        f"{int(matches_count):,}",
    )

    col4.metric(
        "🏃 Total Runs",
        f"{int(total_runs):,}",
    )

    col5.metric(
        "🎯 Total Wickets",
        f"{int(total_wickets):,}",
    )

    st.divider()

    # --------------------------------------------------------
    # TOP RUN SCORERS
    # --------------------------------------------------------

    st.subheader("🏃 Top Run Scorers")

    top_runs = get_data(
        """
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
    )

    if not top_runs.empty:

        col1, col2 = st.columns([2, 1])

        with col1:

            figure = px.bar(
                top_runs.sort_values("total_runs"),
                x="total_runs",
                y="player_name",
                orientation="h",
                title="Top 10 Players by Runs",
                labels={
                    "total_runs": "Runs",
                    "player_name": "Player",
                },
            )

            figure.update_layout(
                height=450,
                showlegend=False,
            )

            st.plotly_chart(
                figure,
                use_container_width=True,
            )

        with col2:

            st.dataframe(
                top_runs,
                use_container_width=True,
                hide_index=True,
            )

    else:

        st.info("No batting data available.")

    st.divider()

    # --------------------------------------------------------
    # TOP WICKET TAKERS
    # --------------------------------------------------------

    st.subheader("🎯 Top Wicket Takers")

    top_wickets = get_data(
        """
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
    )

    if not top_wickets.empty:

        col1, col2 = st.columns([2, 1])

        with col1:

            figure = px.bar(
                top_wickets.sort_values("total_wickets"),
                x="total_wickets",
                y="player_name",
                orientation="h",
                title="Top 10 Players by Wickets",
                labels={
                    "total_wickets": "Wickets",
                    "player_name": "Player",
                },
            )

            figure.update_layout(
                height=450,
                showlegend=False,
            )

            st.plotly_chart(
                figure,
                use_container_width=True,
            )

        with col2:

            st.dataframe(
                top_wickets,
                use_container_width=True,
                hide_index=True,
            )

    else:

        st.info("No bowling data available.")

    st.divider()

    # --------------------------------------------------------
    # MATCH FORMAT
    # --------------------------------------------------------

    st.subheader("🏏 Match Format Analysis")

    format_data = get_data(
        """
        SELECT
            match_type,
            COUNT(*) AS match_count
        FROM matches
        GROUP BY match_type
        ORDER BY match_count DESC;
        """
    )

    if not format_data.empty:

        col1, col2 = st.columns(2)

        with col1:

            figure = px.pie(
                format_data,
                names="match_type",
                values="match_count",
                title="Matches by Format",
                hole=0.45,
            )

            st.plotly_chart(
                figure,
                use_container_width=True,
            )

        with col2:

            st.dataframe(
                format_data,
                use_container_width=True,
                hide_index=True,
            )

    else:

        st.info("No match-format data available.")

    st.divider()

    # --------------------------------------------------------
    # TEAM PERFORMANCE
    # --------------------------------------------------------

    st.subheader("🏆 Team Performance")

    team_runs = get_data(
        """
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
        """
    )

    if not team_runs.empty:

        figure = px.bar(
            team_runs,
            x="team_name",
            y="total_runs",
            title="Total Runs by Team",
            labels={
                "team_name": "Team",
                "total_runs": "Runs",
            },
        )

        figure.update_layout(
            height=450,
            xaxis_tickangle=-35,
        )

        st.plotly_chart(
            figure,
            use_container_width=True,
        )

    else:

        st.info("No team batting data available.")

    st.divider()

    # --------------------------------------------------------
    # RECENT MATCHES
    # --------------------------------------------------------

    st.subheader("📅 Recent Matches")

    recent_matches = get_data(
        """
        SELECT
            m.match_id,
            m.match_date,
            m.match_type,
            t1.team_name AS team_1,
            t2.team_name AS team_2,
            m.status
        FROM matches m
        LEFT JOIN teams t1
            ON m.team1_id = t1.team_id
        LEFT JOIN teams t2
            ON m.team2_id = t2.team_id
        ORDER BY m.match_date DESC
        LIMIT 10;
        """
    )

    if not recent_matches.empty:

        st.dataframe(
            recent_matches,
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.info("No match records available.")

    st.divider()

    st.caption(
        "Cricbuzz LiveStats | "
        "Python • SQL • SQLite • Streamlit • REST API"
    )


# ============================================================
# DEFINE PAGES
# ============================================================

home = st.Page(
    home_page,
    title="Home",
    icon="🏠",
)

live_matches = st.Page(
    "pages/live_matches.py",
    title="Live Matches",
    icon="🏏",
)

top_stats = st.Page(
    "pages/top_stats.py",
    title="Top Statistics",
    icon="📊",
)

sql_queries = st.Page(
    "pages/sql_queries.py",
    title="SQL Analytics",
    icon="🗄️",
)

crud_operations = st.Page(
    "pages/crud_operations.py",
    title="CRUD Operations",
    icon="✏️",
)


# ============================================================
# REGISTER PAGES BUT HIDE AUTOMATIC NAVIGATION
# ============================================================

pg = st.navigation(
    [
        home,
        live_matches,
        top_stats,
        sql_queries,
        crud_operations,
    ],
    position="hidden",
)


# ============================================================
# CUSTOM SIDEBAR
# ============================================================

with st.sidebar:

    # BRANDING AT TOP
    st.markdown(
        """
        <h1 style="margin-bottom: 0;">
            🏏 Cricbuzz
        </h1>

        <p style="
            color: #9ca3af;
            font-size: 15px;
            margin-top: 4px;
        ">
            LiveStats & Cricket Analytics
        </p>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    st.subheader("Dashboard")

    st.page_link(
        home,
        label="Home",
        icon="🏠",
    )

    st.page_link(
        live_matches,
        label="Live Matches",
        icon="🏏",
    )

    st.page_link(
        top_stats,
        label="Top Statistics",
        icon="📊",
    )

    st.page_link(
        sql_queries,
        label="SQL Analytics",
        icon="🗄️",
    )

    st.page_link(
        crud_operations,
        label="CRUD Operations",
        icon="✏️",
    )

    st.divider()

    st.caption(
        "Python • SQL • SQLite • Streamlit"
    )


# ============================================================
# RUN CURRENT PAGE
# ============================================================

pg.run()
