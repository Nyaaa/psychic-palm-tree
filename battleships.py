from tabulate import tabulate
from termcolor import colored
from random import randint
import logging

logging.basicConfig(format='|%(levelname)s| %(message)s', level=logging.DEBUG)


def print_tables_side_by_side(*tables, spacing=10):
    string_tables_split = [tabulate(t, tablefmt="pretty", showindex=range(1, board_size + 1),
                                    headers=range(1, board_size + 1)).splitlines() for t in tables]
    num_lines = max(map(len, string_tables_split))

    for i in range(num_lines):
        line_each_table = []
        for table_lines in string_tables_split:
            line_table_string = table_lines[i]
            line_each_table.append(line_table_string + (" " * spacing))

        final_line_string = "".join(line_each_table)
        print(final_line_string)


class BoardException(Exception):
    pass


class OutOfBoundsException(BoardException):
    def __str__(self):
        return "Target not on board"


class IllegalMoveException(BoardException):
    def __str__(self):
        return "Target not allowed"


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
        while True:
            try:
                repeat = self.enemy_board.shot(self.ask())
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):
    def ask(self):
        print("Computer's turn")
        return Dot(randint(0, board_size - 1), randint(0, board_size - 1))


class User(Player):
    def ask(self):
        print("Your turn")
        while True:
            text = input("Enter target coordinates [X Y] or [0] to exit:").split()
            try:
                numbers = [int(i) for i in text]
                if numbers[0] == 0:
                    exit(0)
                if len(numbers) != 2:
                    print("Enter 2 numbers")
                    continue
                return Dot(numbers[0] - 1, numbers[1] - 1)
            except ValueError:
                print("Enter a number")
                continue


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
        self.char_water = colored("■", "blue")
        self.char_ship = colored("■", "yellow")
        self.char_hit = colored("╳", "red")
        self.char_sunk = colored("■", "red")
        self.sea = [[self.char_water] * board_size for _ in range(board_size)]

    def add_ship(self, ship):
        for dot in ship.dots:
            if self.out(dot) or dot in self.no_placement:
                raise OutOfBoundsException()
        for dot in ship.dots:
            self.sea[dot.x][dot.y] = self.char_ship
        self.ship_list.append(ship)
        self.contour(ship)

    def contour(self, ship, show=False):
        surround = [(-1, -1), (-1, 0), (-1, 1), (0, 0), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dot in ship.dots:
            self.no_placement.append(dot)
            for x, y in surround:
                test = Dot(dot.x + x, dot.y + y)
                if not self.out(test) and test not in self.no_placement:
                    if show:
                        self.sea[test.x][test.y] = "•"
                    self.no_placement.append(test)

    def out(self, dot):
        if not((0 <= dot.x < board_size) and (0 <= dot.y < board_size)):
            return True

    def shot(self, target):
        print(f"Shooting at {target.x + 1, target.y + 1}:")

        if self.out(target):
            raise OutOfBoundsException()
        elif target in self.no_placement:
            raise IllegalMoveException()

        self.no_placement.append(target)
        for ship in self.ship_list:
            if target in ship.dots:
                ship.hp -= 1
                if ship.hp == 0:
                    print("Ship destroyed!")
                    for dot in ship.dots:
                        self.sea[dot.x][dot.y] = self.char_sunk
                        self.contour(ship, show=True)
                else:
                    print("Ship hit!")
                    self.sea[target.x][target.y] = self.char_hit
                return True
        print("Missed!")
        self.sea[target.x][target.y] = "•"
        return False

    def draw(self):
        if self.hide:
            self.sea = [[x.replace(self.char_ship, self.char_water) for x in l] for l in self.sea]
        return self.sea


class Game:
    def __init__(self):
        logging.debug("user board")
        board1 = self.random_board()
        logging.debug("AI board")
        board2 = self.random_board()
        board2.hide = True
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
        board.no_placement.clear()
        return board

    def greet(self):
        pass

    def loop(self):
        step = 0
        tables = [self.human_player.board.draw(), self.ai_player.board.draw()]
        logging.debug(f"ships: {self.human_player.board.ship_list}")
        logging.debug(f"ships: {self.ai_player.board.ship_list}")
        while True:
            if step % 2 == 0:
                print_tables_side_by_side(*tables)
                repeat = self.human_player.move()
            else:
                repeat = self.ai_player.move()
            if repeat:
                print("Shoot again")
                continue
            else:
                step += 1

    def start(self):
        self.greet()
        self.loop()


board_size = 6
g = Game()
g.start()
