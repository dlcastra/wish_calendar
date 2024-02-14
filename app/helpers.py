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


if __name__ == "__main__":
    db_data = from_db()
    get_day_db = db_data[1].split("-")
    get_day_db = int(get_day_db[2])
    now = datetime.now()
    today = now.date()
    # print(type(sd[2]))
    if not db_data or today.day != get_day_db:
        print(1)

    print(db_data)


    # def update_time(self, _dt):  # Updating the date depending on the time of day
    #     db_data = from_db()
    #     get_day_db = db_data[1].split("-")
    #     get_day_db = int(get_day_db[2])
    #     #
    #     if not db_data or self.today.day != get_day_db:
    #         to_db(self.today, self.wish_label.text, self.image.source)
    #
    #     wish = db_data[2]
    #     background_image = db_data[3]
    #
    #     self.date_label.text = f"{self.today.day} {self.today.strftime('%B')}"
    #     self.wish_label.text = wish
    #     self.image.source = background_image