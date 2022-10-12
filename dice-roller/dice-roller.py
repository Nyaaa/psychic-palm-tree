import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import NumericProperty


class MainScreen(ScreenManager):
    def __init__(self):
        super(MainScreen, self).__init__()


class FirstScreen(Screen):
    #some methods
    pass


class SecondScreen(Screen):
    #some methods
    pass


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
