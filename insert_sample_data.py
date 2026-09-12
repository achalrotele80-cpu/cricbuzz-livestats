from utils.db_connection import get_connection


def insert_data():
    connection = get_connection()
    cursor = connection.cursor()

    # -------------------------
    # Teams
    # -------------------------
    teams = [
        (1, "India", "India", "International"),
        (2, "Australia", "Australia", "International"),
        (3, "England", "England", "International"),
        (4, "South Africa", "South Africa", "International"),
        (5, "New Zealand", "New Zealand", "International"),
        (6, "Pakistan", "Pakistan", "International"),
    ]

    cursor.executemany(
        """
        INSERT OR IGNORE INTO teams
        (team_id, team_name, country, team_type)
        VALUES (?, ?, ?, ?)
        """,
        teams,
    )

    # -------------------------
    # Players
    # -------------------------
    players = [
        (1, "Virat Kohli", "India", "Batsman",
         "Right-hand", "Right-arm medium", "1988-11-05"),
        (2, "Rohit Sharma", "India", "Batsman",
         "Right-hand", "Right-arm off break", "1987-04-30"),
        (3, "Jasprit Bumrah", "India", "Bowler",
         "Right-hand", "Right-arm fast", "1993-12-06"),
        (4, "Ravindra Jadeja", "India", "All-rounder",
         "Left-hand", "Slow left-arm orthodox", "1988-12-06"),
        (5, "Steve Smith", "Australia", "Batsman",
         "Right-hand", "Right-arm leg break", "1989-06-02"),
        (6, "Pat Cummins", "Australia", "Bowler",
         "Right-hand", "Right-arm fast", "1993-05-08"),
        (7, "Joe Root", "England", "Batsman",
         "Right-hand", "Right-arm off break", "1990-12-30"),
        (8, "Ben Stokes", "England", "All-rounder",
         "Left-hand", "Right-arm fast", "1991-06-04"),
        (9, "Kagiso Rabada", "South Africa", "Bowler",
         "Right-hand", "Right-arm fast", "1995-05-25"),
        (10, "Kane Williamson", "New Zealand", "Batsman",
         "Right-hand", "Right-arm off break", "1990-08-08"),
        (11, "Babar Azam", "Pakistan", "Batsman",
         "Right-hand", "Right-arm off break", "1994-10-15"),
        (12, "Shaheen Afridi", "Pakistan", "Bowler",
         "Left-hand", "Left-arm fast", "2000-04-06"),
    ]

    cursor.executemany(
        """
        INSERT OR IGNORE INTO players
        (player_id, player_name, country, role,
         batting_style, bowling_style, date_of_birth)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        players,
    )

    # -------------------------
    # Venues
    # -------------------------
    venues = [
        (1, "Wankhede Stadium", "Mumbai", "India", 33000),
        (2, "Melbourne Cricket Ground", "Melbourne", "Australia", 100024),
        (3, "Lord's Cricket Ground", "London", "England", 30000),
        (4, "Newlands Cricket Ground", "Cape Town", "South Africa", 25000),
    ]

    cursor.executemany(
        """
        INSERT OR IGNORE INTO venues
        (venue_id, venue_name, city, country, capacity)
        VALUES (?, ?, ?, ?, ?)
        """,
        venues,
    )

    # -------------------------
    # Series
    # -------------------------
    series = [
        (1, "India vs Australia ODI Series",
         "India", "ODI", "2025-01-01", 3),
        (2, "England Test Series",
         "England", "Test", "2025-02-01", 3),
        (3, "International T20 Series",
         "India", "T20", "2025-03-01", 5),
    ]

    cursor.executemany(
        """
        INSERT OR IGNORE INTO series
        (series_id, series_name, host_country,
         match_type, start_date, total_matches)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        series,
    )

    # -------------------------
    # Matches
    # -------------------------
    matches = [
        (1, 1, "2025-01-05", "ODI", 1, 2, 1,
         1, 5, "Wickets", 1, "Bat", "Completed"),

        (2, 1, "2025-01-08", "ODI", 1, 2, 2,
         2, 12, "Runs", 2, "Field", "Completed"),

        (3, 2, "2025-02-10", "Test", 3, 4, 3,
         3, 7, "Wickets", 3, "Bat", "Completed"),

        (4, 2, "2025-02-20", "Test", 4, 3, 4,
         4, 85, "Runs", 3, "Field", "Completed"),

        (5, 3, "2025-03-05", "T20", 1, 5, 1,
         1, 6, "Wickets", 5, "Field", "Completed"),

        (6, 3, "2025-03-08", "T20", 6, 1, 2,
         6, 8, "Wickets", 6, "Bat", "Completed"),

        (7, 3, "2025-03-12", "T20", 2, 6, 2,
         2, 4, "Wickets", 2, "Field", "Completed"),

        (8, 3, "2025-03-15", "T20", 1, 6, 1,
         1, 25, "Runs", 1, "Bat", "Completed"),
    ]

    cursor.executemany(
        """
        INSERT OR IGNORE INTO matches
        (match_id, series_id, match_date, match_type,
         team1_id, team2_id, venue_id, winner_team_id,
         win_margin, win_type, toss_winner_id,
         toss_decision, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        matches,
    )

    # -------------------------
    # Batting
    # -------------------------
    batting = [
        (1, 1, 1, 1, 1, 1, 85, 92, 8, 2, 92.39),
        (2, 1, 2, 1, 1, 2, 62, 70, 6, 1, 88.57),
        (3, 1, 5, 2, 2, 1, 91, 95, 9, 3, 95.79),
        (4, 1, 6, 2, 2, 8, 15, 20, 1, 0, 75.00),

        (5, 2, 1, 1, 1, 1, 45, 50, 4, 1, 90.00),
        (6, 2, 4, 1, 1, 6, 35, 42, 3, 1, 83.33),
        (7, 2, 5, 2, 2, 1, 76, 88, 7, 2, 86.36),
        (8, 2, 6, 2, 2, 7, 42, 48, 4, 1, 87.50),

        (9, 3, 7, 3, 1, 1, 120, 220, 12, 1, 54.55),
        (10, 3, 8, 3, 1, 2, 88, 160, 8, 0, 55.00),
        (11, 3, 9, 4, 2, 1, 95, 210, 10, 1, 45.24),
        (12, 3, 10, 5, 2, 2, 110, 230, 11, 2, 47.83),

        (13, 4, 7, 3, 1, 1, 75, 130, 8, 0, 57.69),
        (14, 4, 8, 3, 1, 2, 55, 90, 5, 1, 61.11),
        (15, 4, 9, 4, 2, 1, 105, 190, 9, 2, 55.26),
        (16, 4, 10, 5, 2, 2, 65, 120, 6, 1, 54.17),

        (17, 5, 1, 1, 1, 1, 72, 45, 6, 4, 160.00),
        (18, 5, 4, 1, 1, 4, 38, 25, 3, 2, 152.00),
        (19, 5, 10, 5, 2, 1, 54, 40, 5, 2, 135.00),
        (20, 5, 12, 6, 2, 3, 31, 22, 2, 2, 140.91),

        (21, 6, 11, 6, 1, 1, 81, 48, 7, 3, 168.75),
        (22, 6, 12, 6, 1, 2, 25, 18, 2, 1, 138.89),
        (23, 6, 2, 1, 2, 1, 66, 42, 6, 2, 157.14),
        (24, 6, 3, 1, 2, 5, 12, 10, 1, 0, 120.00),

        (25, 7, 5, 2, 1, 1, 88, 52, 8, 3, 169.23),
        (26, 7, 6, 2, 1, 2, 45, 35, 4, 2, 128.57),
        (27, 7, 11, 6, 2, 1, 60, 40, 5, 2, 150.00),
        (28, 7, 12, 6, 2, 2, 18, 15, 1, 1, 120.00),

        (29, 8, 1, 1, 1, 1, 102, 58, 10, 4, 175.86),
        (30, 8, 3, 1, 1, 3, 30, 20, 2, 1, 150.00),
        (31, 8, 11, 6, 2, 1, 70, 48, 7, 2, 145.83),
        (32, 8, 12, 6, 2, 2, 28, 18, 3, 1, 155.56),
    ]

    cursor.executemany(
        """
        INSERT OR IGNORE INTO batting
        (batting_id, match_id, player_id, team_id,
         innings, batting_position, runs, balls,
         fours, sixes, strike_rate)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        batting,
    )

    # -------------------------
    # Bowling
    # -------------------------
    bowling = [
        (1, 1, 3, 1, 2, 10, 42, 3, 4.20),
        (2, 1, 6, 2, 1, 10, 55, 2, 5.50),

        (3, 2, 3, 1, 2, 10, 48, 4, 4.80),
        (4, 2, 6, 2, 1, 10, 50, 3, 5.00),

        (5, 3, 9, 4, 1, 35, 82, 4, 2.34),
        (6, 3, 8, 3, 2, 30, 70, 3, 2.33),

        (7, 4, 9, 4, 1, 32, 75, 5, 2.34),
        (8, 4, 8, 3, 2, 28, 68, 2, 2.43),

        (9, 5, 3, 1, 2, 4, 28, 3, 7.00),
        (10, 5, 12, 6, 1, 4, 35, 2, 8.75),

        (11, 6, 12, 6, 1, 4, 30, 3, 7.50),
        (12, 6, 3, 1, 2, 4, 34, 2, 8.50),

        (13, 7, 6, 2, 1, 4, 26, 3, 6.50),
        (14, 7, 12, 6, 2, 4, 38, 2, 9.50),

        (15, 8, 3, 1, 2, 4, 25, 3, 6.25),
        (16, 8, 12, 6, 1, 4, 41, 1, 10.25),
    ]

    cursor.executemany(
        """
        INSERT OR IGNORE INTO bowling
        (bowling_id, match_id, player_id, team_id,
         innings, overs, runs_conceded, wickets, economy)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        bowling,
    )

    connection.commit()
    connection.close()

    print("Sample cricket data inserted successfully!")


if __name__ == "__main__":
    insert_data()