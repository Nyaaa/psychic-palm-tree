import termtables
from termcolor import colored
import numpy as np

spaces = [1, 2, 3, 4, 5, 6, 7, 8, 9]


score = {
    "playerX": [],
    "playerO": []
}


def board():
    print(spaces[0], "|", spaces[1], "|", spaces[2])
    print(spaces[3], "|", spaces[4], "|", spaces[5])
    print(spaces[6], "|", spaces[7], "|", spaces[8])


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
        num = np.array(spaces)
        reshaped = num.reshape(3, 3)
        termtables.print(reshaped)

        player_sym = player(step)[0]
        player_name = player(step)[1]
        print(f"Player: ( {player_sym} )")
        play = int(input("Enter 1-9 to play, 0 to exit: "))
        if play == 0:
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
            print("Winner: ", player_name)
            break


if __name__ == '__main__':
    print("Tic-tac-toe")
    start()
