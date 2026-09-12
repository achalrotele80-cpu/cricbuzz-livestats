from utils.api import get_scorecard


def fetch_scorecard(match_id):
    """Fetch scorecard data for a specific match."""
    return get_scorecard(match_id)


def parse_scorecard(data):
    """Extract batting and bowling records from scorecard data."""

    batting_records = []
    bowling_records = []

    for innings in data.get("scorecard", []):

        innings_id = innings.get("inningsid")
        batting_team = innings.get("batteamname")

        for position, batsman in enumerate(
            innings.get("batsman", []),
            start=1
        ):

            batting_records.append({
                "innings": innings_id,
                "team_name": batting_team,
                "player_id": batsman.get("id"),
                "player_name": batsman.get("name"),
                "batting_position": position,
                "runs": batsman.get("runs"),
                "balls": batsman.get("balls"),
                "fours": batsman.get("fours"),
                "sixes": batsman.get("sixes"),
                "strike_rate": batsman.get("strkrate"),
            })

        for bowler in innings.get("bowler", []):

            bowling_records.append({
                "innings": innings_id,
                "team_name": batting_team,
                "player_id": bowler.get("id"),
                "player_name": bowler.get("name"),
                "overs": bowler.get("overs"),
                "runs_conceded": bowler.get("runs"),
                "wickets": bowler.get("wickets"),
                "economy": bowler.get("economy"),
            })

    return batting_records, bowling_records


from services.database_service import (
    save_player,
    get_team_id,
    save_batting,
)

def save_scorecard(match_id, data):
    """Save batting and bowling data from a scorecard."""

    batting_records, bowling_records = parse_scorecard(data)

    saved_count = 0

    for record in batting_records:
        save_player(
            record["player_id"],
            record["player_name"],
        )

        team_id = get_team_id(record["team_name"])

        if team_id:
            save_batting(
                match_id,
                record["player_id"],
                team_id,
                record["innings"],
                record["batting_position"],
                record["runs"],
                record["balls"],
                record["fours"],
                record["sixes"],
                record["strike_rate"],
            )

            saved_count += 1

    for record in bowling_records:
        save_player(
            record["player_id"],
            record["player_name"],
        )

        team_id = get_team_id(record["team_name"])

        if team_id:
            save_bowling(
                match_id,
                record["player_id"],
                team_id,
                record["innings"],
                record["overs"],
                record["runs_conceded"],
                record["wickets"],
                record["economy"],
            )

    return saved_count