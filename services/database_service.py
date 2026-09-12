from utils.db_connection import get_connection


def save_team(team_id, team_name):
    """Save a team if it does not already exist."""

    connection = get_connection()

    query = """
        INSERT OR IGNORE INTO teams
        (team_id, team_name)
        VALUES (?, ?)
    """

    connection.execute(
        query,
        (team_id, team_name)
    )

    connection.commit()
    connection.close()


def save_venue(venue_id, venue_name, city):
    """Save a venue if it does not already exist."""

    connection = get_connection()

    query = """
        INSERT OR IGNORE INTO venues
        (venue_id, venue_name, city)
        VALUES (?, ?, ?)
    """

    connection.execute(
        query,
        (venue_id, venue_name, city)
    )

    connection.commit()
    connection.close()


def save_series(series_id, series_name, match_type, start_date):
    """Save a series if it does not already exist."""

    connection = get_connection()

    query = """
        INSERT OR IGNORE INTO series
        (series_id, series_name, match_type, start_date)
        VALUES (?, ?, ?, ?)
    """

    connection.execute(
        query,
        (
            series_id,
            series_name,
            match_type,
            start_date
        )
    )

    connection.commit()
    connection.close()


def save_match(
    match_id,
    series_id,
    match_date,
    match_type,
    team1_id,
    team2_id,
    venue_id,
    status
):
    """Save or update a match."""

    connection = get_connection()

    query = """
        INSERT OR REPLACE INTO matches
        (
            match_id,
            series_id,
            match_date,
            match_type,
            team1_id,
            team2_id,
            venue_id,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)

        ON CONFLICT(match_id)
        DO UPDATE SET
            series_id = excluded.series_id,
            match_date = excluded.match_date,
            match_type = excluded.match_type,
            team1_id = excluded.team1_id,
            team2_id = excluded.team2_id,
            venue_id = excluded.venue_id,
            status = excluded.status
    """
    

    connection.execute(
        query,
        (
            match_id,
            series_id,
            match_date,
            match_type,
            team1_id,
            team2_id,
            venue_id,
            status
        )
    )

    connection.commit()
    connection.close()


def get_table_data(table_name):
    """Retrieve all records from a database table."""

    allowed_tables = {
        "teams",
        "players",
        "venues",
        "series",
        "matches",
        "batting",
        "bowling",
        "fielding",
    }

    if table_name not in allowed_tables:
        raise ValueError("Invalid table name.")

    connection = get_connection()

    query = f"SELECT * FROM {table_name}"

    data = connection.execute(query).fetchall()

    columns = [
        description[0]
        for description in connection.execute(
            query
        ).description
    ]

    connection.close()

    return columns, data

def create_team(team_id, team_name, country):
    """Create a new team in the database."""

    connection = get_connection()

    query = """
        INSERT INTO teams
        (team_id, team_name, country)
        VALUES (?, ?, ?)
    """

    connection.execute(
        query,
        (team_id, team_name, country)
    )

    connection.commit()
    connection.close()

def update_team(team_id, team_name, country):
    """Update an existing team."""

    connection = get_connection()

    query = """
        UPDATE teams
        SET team_name = ?, country = ?
        WHERE team_id = ?
    """

    cursor = connection.execute(
        query,
        (team_name, country, team_id)
    )

    connection.commit()
    connection.close()

    return cursor.rowcount


def delete_team(team_id):
    """Delete a team from the database."""

    connection = get_connection()

    query = """
        DELETE FROM teams
        WHERE team_id = ?
    """

    cursor = connection.execute(
        query,
        (team_id,)
    )

    connection.commit()
    connection.close()

    return cursor.rowcount


def save_player(player_id, player_name):
    """Save a player if the player does not already exist."""

    if not player_id or not player_name:
        return

    connection = get_connection()

    query = """
        INSERT OR IGNORE INTO players
        (
            player_id,
            player_name
        )
        VALUES (?, ?)
    """

    connection.execute(
        query,
        (
            player_id,
            player_name,
        )
    )

    connection.commit()
    connection.close()

def get_team_id(team_name):
    """Return the team ID for a given team name."""

    connection = get_connection()

    query = """
        SELECT team_id
        FROM teams
        WHERE team_name = ?
    """

    result = connection.execute(
        query,
        (team_name,)
    ).fetchone()

    connection.close()

    if result:
        return result[0]

    return None


def save_batting(
    match_id,
    player_id,
    team_id,
    innings,
    batting_position,
    runs,
    balls,
    fours,
    sixes,
    strike_rate,
):
    """Save batting statistics for a player in a match."""

    connection = get_connection()

    query = """
        INSERT INTO batting
        (
            match_id,
            player_id,
            team_id,
            innings,
            batting_position,
            runs,
            balls,
            fours,
            sixes,
            strike_rate
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    connection.execute(
        query,
        (
            match_id,
            player_id,
            team_id,
            innings,
            batting_position,
            runs,
            balls,
            fours,
            sixes,
            float(strike_rate) if strike_rate else None,
        ),
    )

    connection.commit()
    connection.close()


def save_bowling(
    match_id,
    player_id,
    team_id,
    innings,
    overs,
    runs_conceded,
    wickets,
    economy,
):
    """Save bowling statistics for a player in a match."""

    connection = get_connection()

    query = """
        INSERT INTO bowling
        (
            match_id,
            player_id,
            team_id,
            innings,
            overs,
            runs_conceded,
            wickets,
            economy
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """

    connection.execute(
        query,
        (
            match_id,
            player_id,
            team_id,
            innings,
            overs,
            runs_conceded,
            wickets,
            float(economy) if economy else None,
        ),
    )

    connection.commit()
    connection.close()

