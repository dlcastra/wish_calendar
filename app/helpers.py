import sqlite3
from datetime import datetime


def to_db(date, wish, image):
    conn = sqlite3.connect("app_data.db")
    with conn as cust_conn:
        cursor = cust_conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS data(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE,
                wish TEXT,
                background TEXT
            )
            """
        )

        cursor.execute(
            """
            INSERT INTO data (date, wish, background)
            VALUES (?, ?, ?)
            """,
            (date, wish, image),
        )


def from_db():
    conn = sqlite3.connect("app_data.db")
    with conn as cust_conn:
        cursor = cust_conn.cursor()
        cursor.execute(
            """
            SELECT * FROM data
            """
        )
        result = cursor.fetchone()

    return result


def is_database_empty():
    conn = sqlite3.connect("app_data.db")
    with conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='data'")
        table_exists = cursor.fetchone()
        if table_exists:
            cursor.execute("SELECT COUNT(*) FROM data")
            row_count = cursor.fetchone()[0]
            return row_count == 0
        else:
            return True


if __name__ == "__main__":
    # db_data = from_db()
    # get_day_db = db_data[1].split("-")
    # get_day_db = int(get_day_db[2])
    # now = datetime.now()
    # today = now.date()
    # # print(type(sd[2]))
    # if not db_data or today.day != get_day_db:
    #     print(1)
    #
    # print(db_data)
    print()
