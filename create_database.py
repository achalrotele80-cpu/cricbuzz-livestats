import sqlite3


DB_NAME = "cricbuzz_livestats.db"


def check_database():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        ORDER BY name
    """)

    tables = cursor.fetchall()

    print("Tables in database:")

    for table in tables:
        print(table[0])

    connection.close()


if __name__ == "__main__":
    check_database()