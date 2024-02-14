import os
import sqlite3
from datetime import datetime

import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label

from wishes import wish_list
import random

# Config
kivy.require("2.3.0")
Config.set("graphics", "width", "400")
Config.set("graphics", "height", "600")


class CalendarApp(App):
    def __init__(self):
        super().__init__()
        self.date_label = None
        self.wish_label = None
        self.image = None
        self.today = datetime.today()
        self.wishes = [wish for wish in wish_list]
        self.paths = [
            "images/winter/",
            "images/spring/",
            "images/summer/",
            "images/autumn/",
        ]

    def build(self):  # Main logic
        # conn = sqlite3.connect("app_data.db")
        # c = conn.cursor()

        root = FloatLayout()
        self.image = Image(source=self.get_background_image(), size_hint=(1, 1))

        self.date_label = Label(
            text=f"{self.today.day} {self.today.strftime('%B')}",
            color=(11, 11, 11),
            font_size="30sp",
            halign="center",
            valign="middle",
            pos=(200, 500),
            pos_hint={"center_y": 0.85, "center_x": 0.5},
        )
        self.wish_label = Label(
            text=self.get_wish(),
            color=(11, 11, 11),
            font_size="20sp",
            size=(400, 200),
            text_size=(400, None),
            halign="center",
            valign="middle",
            pos_hint={"center_y": 0.70},
        )

        root.add_widget(self.image)
        root.add_widget(self.date_label)
        root.add_widget(self.wish_label)

        Clock.schedule_interval(self.update_time, 60)
        return root

    def get_wish(self):  # Logic for creating wishes.
        hour = datetime.now().hour
        if hour < 12:
            return self.wishes[0]
        elif hour < 18:
            return self.wishes[1]
        else:
            return self.wishes[2]

    def get_random_image(self, index: int):
        path = self.paths[index]
        get_images = [file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))]
        choice_image = random.choice(get_images)
        image = os.path.join(path, choice_image)

        return image

    def get_background_image(self):  # Logic of background selection depending on the time of year.
        month = datetime.now().month
        if month in [12, 1, 2]:
            return self.get_random_image(0)
        elif month in [3, 4, 5]:
            return self.get_random_image(1)
        elif month in [6, 7, 8]:
            return self.get_random_image(2)
        else:
            return self.get_random_image(3)

    def update_time(self, _dt):  # Updating the date depending on the time of day
        new_today = datetime.today()
        if new_today.day != self.today.day:
            self.today = new_today
            self.date_label.text = f"{self.today.day} {self.today.strftime('%B')}"
            self.wish_label.text = self.get_wish()
            self.image.source = self.get_background_image()


if __name__ == "__main__":
    app = CalendarApp()
    app.run()
