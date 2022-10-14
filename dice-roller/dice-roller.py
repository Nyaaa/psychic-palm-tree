import random
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.label import Label
Window.size = (400, 400)


class MainScreen(ScreenManager):
    def __init__(self):
        super(MainScreen, self).__init__()


class FirstScreen(Screen):
    sides = 0

    def roll(self, sides):
        roll_times = self.ids.roll_times.text
        if not roll_times:
            roll_times = 1
        else:
            roll_times = int(roll_times)
        modifier = self.ids.modifier.text
        if not modifier:
            modifier = 0
            mod_text = ""
        else:
            modifier = int(modifier)
            if modifier > 0:
                mod_text = f"+{modifier}"
            else:
                mod_text = f"-{modifier}"
        rolls = []
        for i in range(roll_times):
            roll = random.randrange(1, sides + 1)
            rolls.append(roll)
        total = sum(rolls, modifier)
        title = f"{roll_times}d{sides}{mod_text}"
        text = f"Rolls: {rolls}\nTotal: {total}\n"
        popup = Popup(title=title,
                      content=Label(text=text),  # TODO add text wrapping
                      size_hint=(None, None), size=(200, 200))
        popup.open()


class DiceRollerApp(App):
    def build(self):
        return MainScreen()


def main():
    Builder.load_file('screen.kv')
    app = DiceRollerApp()
    app.run()


if __name__ == '__main__':
    main()
