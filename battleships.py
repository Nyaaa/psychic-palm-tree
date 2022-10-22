from tabulate import tabulate
from termcolor import colored
from random import randint, choice
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
        self.target_choice = []

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                repeat = self.enemy_board.shot(self.ask())
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):
    def ask(self):
        self.target_choice.clear()
        x = []
        y = []

        for i in self.enemy_board.hit:
            x.append(i.x)
            y.append(i.y)
        x.sort()
        y.sort()

        if len(set(x)) == 1 and len(set(y)) == 1:  # One hit
            near = [(-1, 0), (0, -1), (0, 1), (1, 0)]
            for x1, y1 in near:
                self.target_choice.append(Dot(x[0] + x1, y[0] + y1))
        elif len(set(x)) == 1:  # common X axis
            self.target_choice.append(Dot(x[0], y[0] - 1))  # left
            self.target_choice.append(Dot(x[0], y[-1] + 1))  # right
        elif len(set(y)) == 1:  # common Y axis
            self.target_choice.append(Dot(x[0] - 1, y[0]))  # up
            self.target_choice.append(Dot(x[-1] + 1, y[0]))  # down

        print(self.target_choice)
        return self.target_choice

    def move(self):
        print("Computer's turn")
        while True:
            try:
                if self.enemy_board.hit:
                    target = choice(self.ask())
                else:
                    target = Dot(randint(0, board_size - 1), randint(0, board_size - 1))

                repeat = self.enemy_board.shot(target)
                return repeat
            except BoardException as e:
                logging.debug(e)


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
            except IndexError:
                continue


class Ship:
    def __init__(self, location, hp, direction):
        self.location = location
        self.length = hp
        self.hp = hp
        self.direction = direction

    @property
    def dots(self):
        coordinates = []
        for i in range(self.length):
            x = self.location.x
            y = self.location.y
            if self.direction == 0:
                x += i
            elif self.direction == 1:
                y += i
            coordinates.append(Dot(x, y))
        return coordinates

    def __repr__(self):
        return f"{self.dots}"


class Board:
    def __init__(self, hide=False):
        self.hide = hide
        self.ship_list = []
        self.no_placement = []
        self.hit = []
        self.char_water = colored("■", "blue")
        self.char_ship = colored("■", "yellow")
        self.char_hit = colored("╳", "red")
        self.char_sunk = colored("■", "red")
        self.sea = [[self.char_water] * board_size for _ in range(board_size)]

    def add_ship(self, ship):
        for dot in ship.dots:
            if self.boundary_check(dot) or dot in self.no_placement:
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
                if not self.boundary_check(test) and test not in self.no_placement:
                    if show:
                        self.sea[test.x][test.y] = "•"
                    self.no_placement.append(test)

    def shot(self, target):
        if self.boundary_check(target):
            raise OutOfBoundsException()
        elif target in self.no_placement:
            raise IllegalMoveException()

        print(f"🎯 Shooting at {target.x + 1, target.y + 1}:")
        self.no_placement.append(target)
        for ship in self.ship_list:
            if target in ship.dots:
                ship.hp -= 1
                if ship.hp == 0:
                    print("☠ Ship destroyed!")
                    for dot in ship.dots:
                        self.sea[dot.x][dot.y] = self.char_sunk
                        self.contour(ship, show=True)
                    self.hit.clear()
                    self.ship_list.remove(ship)
                else:
                    print("💥 Ship hit!")
                    self.hit.append(target)
                    self.sea[target.x][target.y] = self.char_hit
                return True
        print("🌫️ Missed!")
        self.sea[target.x][target.y] = "•"
        return False

    @staticmethod
    def boundary_check(dot):
        """Returns True if dot is not on the board"""
        if not ((0 <= dot.x < board_size) and (0 <= dot.y < board_size)):
            return True

    def draw(self):
        if self.hide:
            self.sea = [[x.replace(self.char_ship, self.char_water) for x in lst] for lst in self.sea]
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

    @staticmethod
    def random_board_create():
        ship_types = [3, 2, 2, 1, 1, 1, 1]
        #ship_types = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
        #ship_types = [3, 3, 3, 3, 3, 3, 3]
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

    @staticmethod
    def greet():
        print(r"""⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀       ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣸⣇⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀       ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣸⣇⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀       ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⢹⡏⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀       ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⢾⡟⠛⠛⠛⠛⢻⡷⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀       ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣤⡴⠟⣿⣦⣤⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀       ⠀⠀⠀⠀⠀⠀⠀⠀⢰⡟⠋⢿⡷⠀⣿⡇⠈⣿⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀       ⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⠀⠀⠀⠀⣿⣿⣿⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀       ⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⡀⠀⠀⠀⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀       ⠀⠀⠀⠀⣀⣀⣀⣀⣠⣼⣧⣤⣤⣤⣿⣿⣿⣿⣧⣤⣤⣤⣀⣀⣀⣤⠀⠀⠀
⠀       ⠀⠘⠛⠛⠛⠉⠉⠉⠉⠙⠛⠛⠷⠶⢶⣦⣤⣤⣤⣴⡶⠿⠟⠛⠋⠁⠀⠀⠀
⠀       ⠀⠀⠀⠀⠛⠛⠛⠛⠻⠷⠶⠶⣶⣤⣤⣤⣤⣤⣤⣤⣤⣤⡶⠶⠶⠀⠀⠀⠀
⠀       ⢠⡶⠶⠶⠿⠛⠛⠻⠷⠶⢶⣤⣤⣤⣤⣤⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀ _           _   _   _           _     _           
| |         | | | | | |         | |   (_)          
| |__   __ _| |_| |_| | ___  ___| |__  _ _ __  ___ 
| '_ \ / _` | __| __| |/ _ \/ __| '_ \| | '_ \/ __|
| |_) | (_| | |_| |_| |  __/\__ \ | | | | |_) \__ \
|_.__/ \__,_|\__|\__|_|\___||___/_| |_|_| .__/|___/
                                        | |        
                                        |_|  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀""")

    def loop(self):
        step = 0
        tables = [self.human_player.board.draw(), self.ai_player.board.draw()]
        logging.debug(f"Player ships: {self.human_player.board.ship_list}")
        logging.debug(f"AI ships: {self.ai_player.board.ship_list}")

        while True:
            if len(self.ai_player.board.ship_list) == 0:
                print_tables_side_by_side(*tables)
                print("🏆 You win!")
                exit(0)
            elif len(self.human_player.board.ship_list) == 0:
                print_tables_side_by_side(*tables)
                print("💢 You lose!")
                exit(0)

            if step % 2 == 0:
                print_tables_side_by_side(*tables)
                logging.info(f"AI ships: {len(self.ai_player.board.ship_list)}")
                logging.info(f"Player ships: {len(self.human_player.board.ship_list)}")
                repeat = self.human_player.move()
            else:
                repeat = self.ai_player.move()

            if repeat:
                print("⏩ Shoot again")
                continue
            else:
                step += 1
                print("=" * 10, f"Round {step}", "=" * 10)

    def start(self):
        self.greet()
        self.loop()


if __name__ == '__main__':
    board_size = 6
    g = Game()
    g.start()
