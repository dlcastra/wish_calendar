import os
import random
import re
import sqlite3
import sys
from datetime import datetime

import kivy
from kivy import Config
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.resources import resource_add_path
from kivy.uix.floatlayout import FloatLayout

from wishes import wish_list

# Database setup
conn = sqlite3.connect("calendar.db")
c = conn.cursor()
c.execute(
    """CREATE TABLE IF NOT EXISTS events
             (date TEXT PRIMARY KEY, wish TEXT, image TEXT)"""
)
conn.commit()

# App setup
kivy.require("2.3.0")
Config.set("graphics", "width", "400")
Config.set("graphics", "height", "600")


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class CalendarApp(FloatLayout):
    def __init__(self, **kwargs):
        super(CalendarApp, self).__init__(**kwargs)
        now = datetime.now()
        self.today = f"{now.day} {now.strftime('%B')}"
        self.load_or_create_event(0)

    def load_or_create_event(self, _dt):
        c.execute("SELECT * FROM events WHERE date=?", (self.today,))
        result = c.fetchone()
        if result:
            self.ids.date_label.text = result[0]
            self.ids.wish_label.text = result[1]
            image_path = resource_path(result[2])
            self.ids.background_image.source = image_path

        else:
            self.create_event_and_display()

    def get_background_image(self):
        month = datetime.now().month
        _path = None
        if month in [12, 1, 2]:
            _path = resource_path("images/winter/")
        elif month in [3, 4, 5]:
            _path = resource_path("images/spring/")
        elif month in [6, 7, 8]:
            _path = resource_path("images/summer/")
        else:
            _path = resource_path("images/autumn/")

        return self.get_random_image(_path)

    @staticmethod
    def get_random_image(path):
        if os.path.exists(path) and os.listdir(path):
            get_images = [file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))]
            choice_image = random.choice(get_images)
            image_path = os.path.join(path, choice_image)
            return image_path
        else:
            print(f"Directory does not exist or is empty: {path}")
            return None

    def create_event_and_display(self):
        get_wish = [wish for wish in wish_list]
        wish = random.choice(get_wish)

        image_path = self.get_background_image()
        abs_image_path = os.path.abspath(image_path)
        pattern = re.compile(r"\bimages.*")
        short_path = pattern.search(abs_image_path)
        math_path = short_path.group()

        c.execute(
            """
            INSERT INTO events (date, wish, image) 
            VALUES (?, ?, ?)
        """,
            (self.today, wish, math_path),
        )
        conn.commit()
        self.ids.date_label.text = self.today
        self.ids.wish_label.text = wish
        self.ids.background_image.source = math_path


class WishCalendar(App):
    def build(self):
        kv_file_path = resource_path("calendar.kv")
        Builder.load_file(kv_file_path)
        content = CalendarApp()
        Clock.schedule_interval(content.load_or_create_event, 30)
        return content


if __name__ == "__main__":
    if hasattr(sys, "_MEIPASS"):
        resource_add_path(os.path.join(sys._MEIPASS))
    WishCalendar().run()
