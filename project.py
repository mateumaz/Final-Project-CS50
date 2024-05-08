from tabulate import tabulate
from pyfiglet import Figlet
import sys
from project_functions import get_level, get_bomb_map, get_whole_map, get_displayed_map, validate_guess, convert, shoot, check_end
# so emojis can be printed in the tables without destroying them it is necesary to install wcwidth library: pip install tabulate[widechars]

#emojis 🌊 💣 🚩 ⬜

def main():

    #Display introduction and rules
    figlet=Figlet()
    figlet.setFont(f = "big")
    print(figlet.renderText("Sapper Game"))
    print("Find all bombs without any mistake \nTo win a game you need to reveal all squeres without a bomb \nTo shoot you need to input '-s' followed by coordinates e.g. '-s B4'")
    print("You can mark a squere where you think a bomb is with a flag by inputing '-f' followed by coordinates e.g. '-f B4'")
    print("You can exit the game by presing 'Ctrl' + 'D'")
    print("Levels: \n  1 - 4 bombs\n  2 - 7 bombs\n  3 - 10 bombs")

    #Ask for level - how many bombs will there be
    try:
        level = get_level()
    except EOFError:
        sys.exit("\nGame Ended")

    #Preapre
    bomb_map = get_bomb_map(level)
    whole_map = get_whole_map(bomb_map)
    displayed_map = get_displayed_map(whole_map)
    show_table = True

    #Loop for a game
    while True:
        if show_table:
            print("")
            print(tabulate(displayed_map, tablefmt="grid"))
        try:
            guess = input("Take a shot: '-s' + coordinates, Put a flag: '-f' + coordinates \nMove: ").strip()
            if validate_guess(guess):
                show_table = True
                move, [x,y] = convert(guess)
                if move == "f":
                    displayed_map[x][y] = "🚩"
                elif move == "s":
                    displayed_map, end = shoot(displayed_map,whole_map,x,y)
                    if end == 1:
                        win = False
                        break
                if check_end(displayed_map,whole_map,level):
                    win = True
                    break
            else:
                print("Invalid Input")
                show_table = False
        except EOFError:
            sys.exit("Game Ended")

    #Display final message
    print("")
    print(tabulate(displayed_map, tablefmt="grid"))
    if win:
        print(figlet.renderText("Winner, winner, chicken dinner !!!"))
    else:
        print(figlet.renderText("Game Over"))

if __name__ == "__main__":
    main()
