from random import randint
import numpy as np
from colorama import Back, Style


def get_level():
    levels = [1,2,3]
    while True:
        try:
            level = int(input("Chose level: ").strip())
            if level in levels:
                return level
            else:
                raise ValueError
        except ValueError:
            print("Wrong input, chose integer between 1-3")


def get_bomb_map(l):
    bm = []
    if l == 1:
        n = 4
    elif l == 2:
        n = 7
    else:
        n = 10
    for _ in range(n):
        while True:
            b = [randint(1,10), randint(1,10)]
            if b not in bm:
                bm.append(b)
                break
    #In matrix indexes go from 0
    mx = np.zeros((10,10))
    for i in range(10):
        for j in range(10):
            if [i+1,j+1] not in bm:
                mx[i][j] = 0
            else:
                mx[i][j] = 9
    return mx


def get_whole_map(bombs):
    whole = np.zeros((10,10))
    for i in range(10):
        for j in range(10):
            i_l, i_r, j_l, j_r = [1,2,1,2]
            if bombs[i][j] == 9:
                if i == 0:
                    i_l = 0
                elif i == 9:
                    i_r = 1
                if j == 0:
                    j_l = 0
                elif j == 9:
                    j_r = 1
                whole[i-i_l:i+i_r, j-j_l:j+j_r] += 1

    for i in range(10):
        for j in range(10):
            if bombs[i][j] == 9:
                whole[i][j] = 9
    return whole


def get_displayed_map(mp):
    letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    corners = [[0,0],[11,11],[0,11],[11,0]]
    disp = []
    for i in range(12):
        row = []
        for j in range(12):
            if 0 < i < 11 and 0 < j < 11:
                row.append("⬜")
            elif [i,j] in corners:
                row.append("#")
            elif i == 0  or i == 11:
                row.append(j)
            elif j == 0  or j == 11:
                row.append(letters[i-1])
        disp.append(row)
    return disp


def validate_guess(g: str):
    valid_letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    if "-s" in g or "-f" in g:
        if g.endswith("10") and (g[-3].upper() in valid_letters):
            return True
        elif g[-1].isdecimal() and g[-1] != "0" and (g[-2].upper() in valid_letters):
            return True
        else:
            return False
    else:
        return False


def convert(guess: str):
    letters_co = {"A": 1}
    letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    for i in range(9):
        letters_co[letters[i+1]] = i + 2
    r1 = guess[1]
    co = guess[2:].strip().upper()
    x = letters_co[co[0]]
    y = int(co[1:])
    return [r1, [x,y]]


def shoot(dispm, wholem, x, y):
    n = get_coloured_numbers()
    symbols = ["🌊", n[1], n[2], n[3], n[4], n[5], n[6], n[7], n[8]]
    #blank square hit
    if wholem[x-1][y-1] == 0:
        end = 0
        #displayed_map has indexes grater by 1 in comparison to whole_map
        x = x - 1
        y = y - 1
        reveal1 = [[x,y]]
        #finds all connected blank squers
        for coordinates in reveal1:
            x = coordinates[0]
            y = coordinates[1]
            [x,y,ri,rj] = shoot_h(x,y)
            for i in range(ri):
                for j in range(rj):
                    if wholem[x+i][y+j] == 0 and ([x+i,y+j] not in reveal1):
                        reveal1.append([x+i,y+j])
        #finds squares with numbers connected to blank squeres
        reveal_2 = []
        numbers = [0,1,2,3,4,5,6,7,8]
        for coordinates in reveal1:
            x = coordinates[0]
            y = coordinates[1]
            [x,y,ri,rj] = shoot_h(x,y)
            for i in range(ri):
                for j in range(rj):
                    if (wholem[x+i][y+j] in numbers) and ([x+i,y+j] not in reveal_2):
                        reveal_2.append([x+i,y+j])
        #sets emojis for displayed map
        for pole in reveal_2:
            dispm[pole[0]+1][pole[1]+1] = symbols[int(wholem[pole[0]][pole[1]])]

    #bomb square hit
    elif wholem[x-1][y-1] == 9:
        for i in range(10):
            for j in range(10):
                if wholem[i][j] == 9:
                    dispm[i+1][j+1] = "💣"
        end = 1
        dispm[x][y] = Back.RED + "💣" + Style.RESET_ALL
    #square with number hit
    else:
        end = 0
        dispm[x][y] = symbols[int(wholem[x-1][y-1])]
    return dispm, end


def shoot_h(x,y):
    if x == 0 or x == 9:
        ri = 2
    else:
        ri = 3
    if y == 0 or y == 9:
        rj = 2
    else:
        rj = 3

    if x != 0:
        x = x - 1
    if y != 0:
        y = y - 1
    return [x,y,ri,rj]


def get_coloured_numbers():
    numbers=[0,1,2,3,4,5,6,7,8]
    numbers[1] = Back.BLUE + " 1 " + Style.RESET_ALL
    numbers[2] = Back.GREEN + " 2 " + Style.RESET_ALL
    numbers[3] = Back.RED + " 3 " + Style.RESET_ALL
    numbers[4] = Back.MAGENTA + " 4 " + Style.RESET_ALL
    numbers[5] = Back.MAGENTA + " 5 " + Style.RESET_ALL
    numbers[6] = Back.MAGENTA + " 6 " + Style.RESET_ALL
    numbers[7] = Back.MAGENTA + " 7 " + Style.RESET_ALL
    numbers[8] = Back.MAGENTA + " 8 " + Style.RESET_ALL
    return numbers


def check_end(dispm, wholem, level):
    cnt = 0
    if level == 1:
        bombs = 4
    elif level == 2:
        bombs = 7
    else:
        bombs = 10
    for i in range(10):
        for j in range(10):
            if wholem[i][j] == 9 and dispm[i+1][j+1] == "🚩":
                cnt = cnt + 1
                if cnt == bombs:
                    return True
            elif wholem[i][j] != 9 and dispm[i+1][j+1] == "🚩":
                cnt = cnt - 1
    for i in range(10):
        for j in range(10):
            if wholem[i][j] != 9 and (dispm[i+1][j+1] == "⬜" or dispm[i+1][j+1] == "🚩"):
                return False
    return True
