import random
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
Window.size = (400, 400)


class MainScreen(ScreenManager):
    def __init__(self):
        super(MainScreen, self).__init__()


class FirstScreen(Screen):
    pass


class SecondScreen(Screen):
    def roll(self, sides):
        roll_times = self.ids.roll_times.text
        if not roll_times:
            roll_times = 1
        else:
            roll_times = int(roll_times)
        modifier = self.ids.modifier.text
        if not modifier:
            modifier = 0
        else:
            modifier = int(modifier)
        rolls = []
        for i in range(roll_times):
            roll = random.randrange(1, sides+1)
            rolls.append(roll)
        total = sum(rolls, modifier)
        text = f"rolling {roll_times}d{sides}+{modifier}: {rolls} = {total}\n"
        self.ids.output.text += text


class MyKivyApp(App):
    def build(self):
        self.sides = 0
        return MainScreen()


def main():
    Builder.load_file('screen.kv')
    app = MyKivyApp()
    app.run()


if __name__ == '__main__':
    main()
