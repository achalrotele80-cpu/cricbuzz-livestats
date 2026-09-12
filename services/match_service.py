from datetime import datetime, timezone
from utils.api import get_live_matches
from services.database_service import (
    save_team,
    save_venue,
    save_series,
    save_match,
)

def epoch_ms_to_date(value):
    """Convert epoch milliseconds to YYYY-MM-DD."""
    if not value:
        return None

    try:
        timestamp = int(value) / 1000
        return datetime.fromtimestamp(
            timestamp,
            tz=timezone.utc
        ).strftime("%Y-%m-%d")
    except (TypeError, ValueError, OSError):
        return None

def fetch_live_matches():
    """Fetch and return live match data."""
    return get_live_matches()


def save_live_matches(data):
    """Process API data and save matches to the database."""

    saved_count = 0

    for match_type_data in data.get("typeMatches", []):

        match_type = match_type_data.get("matchType")

        for series_data in match_type_data.get(
            "seriesMatches",
            []
        ):

            series_wrapper = series_data.get(
                "seriesAdWrapper"
            )

            if not series_wrapper:
                continue

            series_id = series_wrapper.get("seriesId")
            series_name = series_wrapper.get("seriesName")

            for match_data in series_wrapper.get(
                "matches",
                []
            ):

                match_info = match_data.get(
                    "matchInfo",
                    {}
                )

                match_id = match_info.get("matchId")

                if not match_id:
                    continue

                team1 = match_info.get("team1", {})
                team2 = match_info.get("team2", {})

                venue = match_info.get(
                    "venueInfo",
                    {}
                )

                # Save teams
                save_team(
                    team1.get("teamId"),
                    team1.get("teamName")
                )

                save_team(
                    team2.get("teamId"),
                    team2.get("teamName")
                )

                # Save venue
                save_venue(
                    venue.get("id"),
                    venue.get("ground"),
                    venue.get("city")
                )

                # Save series
                save_series(
                    series_id,
                    series_name,
                    match_info.get("matchFormat"),
                    epoch_ms_to_date(
                        match_info.get("seriesStartDt")
                    )
                )

                # Save match
                save_match(
                    match_id,
                    series_id,
                    epoch_ms_to_date(
                        match_info.get("startDate")
                    ),
                    match_info.get("matchFormat"),
                    team1.get("teamId"),
                    team2.get("teamId"),
                    venue.get("id"),
                    match_info.get("status")
                )

                saved_count += 1

    return saved_count

