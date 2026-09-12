import streamlit as st
from services.match_service import (
    fetch_live_matches,
    save_live_matches,
)

from services.scorecard_service import (
    fetch_scorecard,
    save_scorecard,
)

st.title("🏏 Live Cricket Matches")
st.caption("Real-time match information from Cricbuzz")

# Refresh button
if st.button("🔄 Refresh Live Matches"):
    st.rerun()

data = fetch_live_matches()

if data is None:
    st.error("Unable to fetch live match data.")
    st.stop()

if st.button("💾 Save Matches to Database"):

    saved_count = save_live_matches(data)

    st.success(
        f"{saved_count} matches saved to database."
    )

if data is None:
    st.error("Unable to fetch live match data.")
    st.stop()

# Check the API response
if "typeMatches" not in data:
    st.warning("Live match data format is different from expected.")
    st.json(data)
    st.stop()

matches_found = 0

for match_type in data.get("typeMatches", []):

    series_matches = match_type.get("seriesMatches", [])

    for series in series_matches:

        series_data = series.get("seriesAdWrapper")

        if not series_data:
            continue

        series_name = series_data.get(
            "seriesName",
            "Unknown Series"
        )

        st.subheader(f"🏆 {series_name}")

        for match in series_data.get("matches", []):

            matches_found += 1

            match_info = match.get("matchInfo", {})
            match_id = match_info.get("matchId")
            match_score = match.get("matchScore", {})

            team1 = match_info.get(
                "team1",
                {}
            ).get("teamName", "Team 1")

            team2 = match_info.get(
                "team2",
                {}
            ).get("teamName", "Team 2")

            status = match_info.get(
                "status",
                "Status unavailable"
            )

            venue = match_info.get(
                "venueInfo",
                {}
            ).get("ground", "Venue unavailable")

            city = match_info.get(
                "venueInfo",
                {}
            ).get("city", "")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f"### 🏏 {team1}")

                team1_score = match_score.get(
                    "team1Score",
                    {}
                )

                if team1_score:
                    score = team1_score.get(
                        "inngs1",
                        {}
                    )

                    runs = score.get("runs", "-")
                    wickets = score.get("wickets", "-")
                    overs = score.get("overs", "-")

                    st.metric(
                        "Score",
                        f"{runs}/{wickets}"
                    )

                    st.write(f"Overs: {overs}")

            with col2:
                st.markdown(f"### 🏏 {team2}")

                team2_score = match_score.get(
                    "team2Score",
                    {}
                )

                if team2_score:
                    score = team2_score.get(
                        "inngs1",
                        {}
                    )

                    runs = score.get("runs", "-")
                    wickets = score.get("wickets", "-")
                    overs = score.get("overs", "-")

                    st.metric(
                        "Score",
                        f"{runs}/{wickets}"
                    )

                    st.write(f"Overs: {overs}")

            st.info(f"📢 {status}")

            if city:
                st.write(f"📍 {venue}, {city}")
            else:
                st.write(f"📍 {venue}")

            if st.button(
                "📊 Save Scorecard",
                key=f"scorecard_{match_id}",
            ):
                try:
                    scorecard_data = fetch_scorecard(match_id)

                    saved = save_scorecard(
                        match_id,
                        scorecard_data,
                    )

                    st.success(
                        f"Scorecard saved. {saved} batting records added."
                    )

                except Exception as error:
                    st.error(
                        f"Unable to save scorecard: {error}"
                    )

            st.divider()


if matches_found == 0:
    st.info("No live matches are currently available.")
