import os
from datetime import datetime

import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label

from wishes import wish_list
from helpers import to_db, from_db, is_database_empty
import random

# Config
kivy.require("2.3.0")
Config.set("graphics", "width", "400")
Config.set("graphics", "height", "600")


class CalendarApp(App):
    def __init__(self):
        super().__init__()
        now = datetime.now()
        self.date_label = None
        self.wish_label = None
        self.image = None
        self.today = now.date()
        self.wishes = [wish for wish in wish_list]
        self.paths = [
            "images/winter/",
            "images/spring/",
            "images/summer/",
            "images/autumn/",
        ]

    def get_wish(self):  # Logic for creating wishes.
        wish = random.choice(self.wishes)
        return wish

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

    # def create_new_record(self):
    #     today = datetime.today()
    #     wish = self.get_wish()
    #     background_image = self.get_background_image()
    #     to_db(today, wish, background_image)

    def update_time(self, _dt):  # Updating the date depending on the time of day
        db_data = from_db()
        new_today = datetime.today()

        if db_data and self.today.day == new_today.day:
            self.date_label.text = f"{self.today.day} {self.today.strftime('%B')}"
            self.wish_label.text = db_data[2]
            self.image.source = db_data[3]

    def build(self):  # Main logic
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

        to_db(self.today, self.wish_label.text, self.image.source)

        Clock.schedule_interval(self.update_time, 10)
        return root


if __name__ == "__main__":
    app = CalendarApp()
    app.run()
