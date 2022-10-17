from tabulate import tabulate
from termcolor import colored
from random import randint


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, compare):
        return self.x == compare.x and self.y == compare.y

    def __repr__(self):
        return f"({self.x}, {self.y})"


class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        pass

    def move(self):
        pass


class Ship:
    def __init__(self, location, hp, direction):
        self.location = location
        self.length = hp
        self.hp = hp
        if direction == 0:
            self.direction = "x"
        else:
            self.direction = "y"

    @property
    def dots(self):
        _coordinates = []
        for i in range(self.length):
            _x = self.location.x
            _y = self.location.y
            if self.direction == "x":
                _x += i
            elif self.direction == "y":
                _y += i
            _coordinates.append(Dot(_x, _y))
        return _coordinates


class Board:
    def __init__(self, size, hide=False):
        self.size = size
        self.hide = hide
        water = colored("■", "blue")
        self.sea = [[water] * size for columns in range(size)]
        self.header = list(range(size))

    def place_ships(self):
        pass

    def draw(self):
        print(tabulate(self.sea, headers=self.header, showindex="always", tablefmt="pretty"))


class Game:
    def __init__(self):
        self.size = 6
        player_board = self.random_board()

    def random_board(self):
        ship_list = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        board_with_ships = False
        attempt = 0
        for s in ship_list:
            while attempt < 10:
                ship = Ship(location=Dot(randint(0, self.size), randint(0, self.size)), hp=s, direction=randint(0, 1))
                print(ship.direction, ship.dots)
                attempt += 1

        return board_with_ships

    def greet(self):
        print("hello")

    def loop(self):
        b = Board(size=self.size)
        b.draw()

    def start(self):
        self.greet()
        self.loop()


g = Game()
g.start()
