import os
import random
import sqlite3
from datetime import datetime

import kivy
from kivy import Config
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout

from app.wishes import wish_list

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
            image_path = result[2]
            self.ids.background_image.source = image_path
        else:
            self.create_event_and_display()

    def get_background_image(self):
        month = datetime.now().month
        _path = None
        if month in [12, 1, 2]:
            _path = "images/winter/"
        elif month in [3, 4, 5]:
            _path = "images/spring/"
        elif month in [6, 7, 8]:
            _path = "images/summer/"
        else:
            _path = "images/autumn/"

        return self.get_random_image(_path)

    @staticmethod
    def get_random_image(path):
        get_images = [file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))]
        choice_image = random.choice(get_images)
        image = os.path.join(path, choice_image)
        return image

    def create_event_and_display(self):
        get_wish = [wish for wish in wish_list]
        wish = random.choice(get_wish)
        image_path = self.get_background_image()
        c.execute(
            """
            INSERT INTO events (date, wish, image) 
            VALUES (?, ?, ?)
        """,
            (self.today, wish, image_path),
        )
        conn.commit()
        self.ids.date_label.text = self.today
        self.ids.wish_label.text = wish
        self.ids.background_image.source = image_path


class CalendarAppMain(App):
    def build(self):
        Builder.load_file("calendar.kv")
        content = CalendarApp()
        Clock.schedule_interval(content.load_or_create_event, 30)
        return CalendarApp()


if __name__ == "__main__":
    CalendarAppMain().run()
