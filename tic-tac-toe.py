import termtables
from termcolor import colored
import numpy as np
import random


init = [1, 2, 3, 4, 5, 6, 7, 8, 9]
spaces = init.copy()
score = {
    "playerX": [],
    "playerO": []
}
total_score = {
    "playerX": 0,
    "playerO": 0,
    "draw": 0
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


def board():
    num = np.array(spaces)
    reshaped = num.reshape(3, 3)
    termtables.print(reshaped)


def win_check(player_name):
    score_ = set(score[player_name])
    for i in win_conditions:
        i = set(i)
        if len(i.intersection(score_)) == 3:
            return True


def player(step):
    if step % 2 == 0:
        return colored("X", "red", attrs=["bold"]), "playerX"
    else:
        return colored("O", "blue", attrs=["bold"]), "playerO"


def predict_win(player_name):
    score_ = set(score[player_name])
    for i in win_conditions:
        i = set(i)
        if len(i.difference(score_)) == 1:
            res = i.difference(score_).pop()
            if res in spaces:
                return res


def ai_move():
    if predict_win("playerO"):  # can AI win?
        return predict_win("playerO")
    elif predict_win("playerX"):  # can player win?
        return predict_win("playerX")
    else:
        return random.choice([item for item in spaces if isinstance(item, int)])


def move(player_name, player_sym, play):
    if play in spaces:
        spaces[play - 1] = player_sym
        score[player_name].append(play)
        return True
    else:
        return False


def again():
    again_ = check_input("Play again?\n[1]: New game\n[2]: Exit\n")
    if again_ == 1:
        global spaces
        spaces.clear()
        score["playerO"].clear()
        score["playerX"].clear()
        spaces = init.copy()
        start()
    else:
        exit(0)


def check_input(text):
    while True:
        var = input(text)
        try:
            var = int(var)
            return var
        except ValueError:
            print("Enter a number")
            continue


def start():
    step = 0

    while True:
        player_sym = player(step)[0]
        player_name = player(step)[1]
        board()
        print(f"Player: ( {player_sym} )")

        if step == 9:
            board()
            total_score["draw"] += 1
            print("Draw!")
            print(player(2)[0], total_score["playerX"], ":", total_score["playerO"], player(1)[0])
            print("Draw: ", total_score["draw"])
            again()

        if player_name == "playerO" and mode == 1:
            play = ai_move()
        else:
            play = check_input("Enter [1-9] to play, [0] to exit:\n")

        if play == 0:
            board()
            print("Game over!")
            exit(0)
        else:
            if not move(player_name, player_sym, play):
                print("Illegal move, select a different space")
                continue
        step += 1

        if win_check(player_name):
            board()
            print(f"Winner: ( {player_sym} )")
            total_score[player_name] += 1
            print(player(2)[0], total_score["playerX"], ":", total_score["playerO"], player(1)[0])
            print("Draw: ", total_score["draw"])
            again()


if __name__ == '__main__':
    print("Tic-tac-toe")
    mode = check_input("Select game mode\n[1]: Single player\n[2]: Multiplayer\n")
    start()
