from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from helpers import resource_path

class ScreenManagement(ScreenManager):
    pass


class MainScreen(Screen):
    pass


class NotesScreen(Screen):
    pass


class WishCalendar(App):
    def build(self):
        kv_file_path = resource_path("GUI/testing.kv")
        Builder.load_file(kv_file_path)
        return ScreenManagement()

    def on_spinner_select(self, spinner, text):
        if text == "Замітки":  # Check for the selected option
            self.root.current = "notes"
        else:
            self.root.current = "main"


if __name__ == "__main__":
    WishCalendar().run()
