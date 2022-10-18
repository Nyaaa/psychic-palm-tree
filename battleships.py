from tabulate import tabulate
from termcolor import colored
from random import randint
import logging

logging.basicConfig(format='|%(levelname)s| %(message)s', level=logging.DEBUG)


def print_tables_side_by_side(*tables, spacing=10):
    string_tables_split = [tabulate(t, tablefmt="pretty", showindex=range(board_size),
                                    headers=range(board_size)).splitlines() for t in tables]
    num_lines = max(map(len, string_tables_split))

    for i in range(num_lines):
        line_each_table = []
        for table_lines in string_tables_split:
            line_table_string = table_lines[i]
            line_each_table.append(line_table_string + (" " * spacing))

        final_line_string = "".join(line_each_table)
        print(final_line_string)


class OutOfBoundsException(Exception):
    pass


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, compare):
        return self.x == compare.x and self.y == compare.y

    def __repr__(self):
        return f"({self.x}, {self.y})"


class Player:
    def __init__(self, board1, board2):
        self.board = board1
        self.enemy_board = board2

    def ask(self):
        pass

    def move(self):
        pass


class AI(Player):
    pass


class User(Player):
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

    def __repr__(self):
        return f"{self.dots}"


class Board:
    def __init__(self, hide=False):
        self.hide = hide
        self.ship_list = []
        self.no_placement = []
        water = colored("■", "blue")
        self.sea = [[water] * board_size for _ in range(board_size)]

    def add_ship(self, ship):
        for dot in ship.dots:
            if self.out(dot) or dot in self.no_placement:
                raise OutOfBoundsException()
        for dot in ship.dots:
            self.sea[dot.x][dot.y] = colored("■", "yellow")
        self.ship_list.append(ship)
        self.contour(ship)

    def contour(self, ship):
        surround = [(-1, -1), (-1, 0), (-1, 1), (0, 0), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dot in ship.dots:
            for x, y in surround:
                test = Dot(dot.x + x, dot.y + y)
                if not self.out(test) and test not in self.no_placement:
                    #self.sea[test.x][test.y] = "."
                    self.no_placement.append(test)

    def out(self, dot):
        if not((0 <= dot.x < board_size) and (0 <= dot.y < board_size)):
            return True

    def draw(self):
        #return tabulate(self.sea, headers=range(1, board_size+1), showindex=range(1, board_size+1), tablefmt="pretty")
        return self.sea


class Game:
    def __init__(self):
        logging.debug("user board")
        board1 = self.random_board()
        logging.debug("AI board")
        board2 = self.random_board()
        self.human_player = User(board1, board2)
        self.ai_player = AI(board2, board1)

    def random_board(self):
        board = None
        while board is None:
            board = self.random_board_create()
        return board

    def random_board_create(self):
        ship_types = [3, 2, 2, 1, 1, 1, 1]
        board = Board()
        attempt = 0
        for s in ship_types:
            while True:
                attempt += 1
                if attempt > 100:
                    return None
                ship = Ship(location=Dot(randint(0, board_size), randint(0, board_size)),
                            hp=s, direction=randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except OutOfBoundsException:
                    pass
        logging.debug(f"attempt: {attempt}")
        return board

    def greet(self):
        pass

    def loop(self):
        tables = [self.human_player.board.draw(), self.ai_player.board.draw()]
        logging.debug(f"ships: {self.human_player.board.ship_list}")
        logging.debug(f"ships: {self.ai_player.board.ship_list}")
        print_tables_side_by_side(*tables)

    def start(self):
        self.greet()
        self.loop()


board_size = 6
g = Game()
g.start()
