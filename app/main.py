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
from kivy.uix.screenmanager import Screen, ScreenManager

from helpers import resource_path, save_or_get_other, generate_wish, get_wishes_from_db

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


class NotesScreen(Screen):
    pass


class FinanceScreen(Screen):
    pass


class MainScreen(Screen):
    pass


class MyScreenManager(ScreenManager):
    pass


class CalendarContent(FloatLayout):
    def __init__(self, **kwargs):
        super(CalendarContent, self).__init__(**kwargs)
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
        used_wishes = get_wishes_from_db()
        create_new_wish = generate_wish()
        wish = save_or_get_other(create_new_wish, used_wishes)

        image_path = self.get_background_image()
        pattern = re.compile(r"\bimages.*")
        short_path = pattern.search(image_path)
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


class Notes(FloatLayout): ...


class Finances(FloatLayout): ...


class WishCalendar(App):
    def build(self):
        # screen_manager = MyScreenManager()
        # main_screen = MainScreen(name='main')
        # nodes_screen = FinanceScreen(name='notes')

        kv_file_path = resource_path("GUI/calendar.kv")
        Builder.load_file(kv_file_path)
        content = CalendarContent()
        Clock.schedule_interval(content.load_or_create_event, 30)
        return content

    def on_spinner_select(self, _spinner, text):
        if text == "Нотатки":
            self.root.current = "finance"


if __name__ == "__main__":
    if hasattr(sys, "_MEIPASS"):
        resource_add_path(os.path.join(sys._MEIPASS))
    WishCalendar().run()
