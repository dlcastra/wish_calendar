import os
import random
import sys
import sqlite3

from app.wishes import wish_list


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def get_wishes_from_db():
    conn = sqlite3.connect("calendar.db")
    with conn as cust_conn:
        cursor = cust_conn.cursor()
        cursor.execute(
            """
            SELECT wish FROM events
            """
        )
        result = cursor.fetchall()

    return result


def generate_wish():
    get_wish = [wish for wish in wish_list]
    result = random.choice(get_wish)
    return result


def save_or_get_other(new_wish, wishes_from_db):
    while new_wish in wishes_from_db:
        new_wish = generate_wish()

    return new_wish


def add_notes(note):
    conn = sqlite3.connect("calendar.db")
    with conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO notes (note) 
            VALUES (?)
            """,
            (note,),
        )


def get_all_notes():
    conn = sqlite3.connect("calendar.db")
    with conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM notes")
        rows = cursor.fetchall()

    return rows


if __name__ == "__main__":
    print(get_all_notes())
