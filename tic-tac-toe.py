import termtables
from termcolor import colored
import numpy as np

spaces = [1, 2, 3, 4, 5, 6, 7, 8, 9]
score = {
    "playerX": [],
    "playerO": []
}
win_conditions = (
    (1, 2, 3),
    (4, 5, 6),
    (7, 8, 9),
    (1, 4, 7),
    (2, 5, 8),
    (3, 6, 9),
    (1, 5, 9),
    (3, 5, 7)
)


def board(message=""):
    num = np.array(spaces)
    reshaped = num.reshape(3, 3)
    termtables.print(reshaped)
    print(message)


def win_check(player_name):
    a = set(score[player_name])
    for i in win_conditions:
        if len(a.intersection(i)) == 3:
            return True


def player(step):
    if step % 2 == 0:
        return colored("X", "red", attrs=["bold"]), "playerX"
    else:
        return colored("O", "blue", attrs=["bold"]), "playerO"


def start():
    step = 0
    while True:
        player_sym = player(step)[0]
        player_name = player(step)[1]
        board(f"Player: ( {player_sym} )")

        if step == 9:
            board("Game over!")
            break

        play = input("Enter 1-9 to play, 0 to exit: ")

        try:
            play = int(play)
        except ValueError:
            print("Enter a number")
            continue

        if play == 0:
            board("Game over!")
            break
        else:
            if play in spaces:
                spaces[play - 1] = player_sym
                if player_name == "playerX":
                    score["playerX"].append(play)
                else:
                    score["playerO"].append(play)
            else:
                print("Illegal move, select a different space")
                continue
        step += 1

        if win_check(player_name):
            board(f"Winner: ( {player_sym} )")
            break


if __name__ == '__main__':
    print("Tic-tac-toe")
    start()
