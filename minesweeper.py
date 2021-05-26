from Grid import Grid
import os
from string import ascii_lowercase


def user_input():
    print("To reveal a location, enter the column num, then row. Example \"5 4\"")
    print("To flag a mine, enter an f after the column num then row. Example \"3 2 f\"")
    inp = input("Enter a column, then row: ").split()
    return inp


def invalid_input():
    os.system("cls")
    print("Invalid Input")
    print(grid.visible_grid())


def select_difficulty():
    difficulties = {1: "Beginner", 2: "Intermediate", 3: "Expert"}
    print("Select a difficulty:\n")
    for key in difficulties:
        print(f"[{key}] {difficulties[key]}")
    selected = input()
    if not selected.isdigit():
        print("Invalid difficulty")
        select_difficulty()
        func = select_difficulty()
        return func
    elif int(selected) not in difficulties:
        print("Invalid difficulty")
        func = select_difficulty()
        return func
    else:
        return difficulties[int(selected)]


flag = False
difficulty = select_difficulty()
difficulties = {"Beginner": (8, 8, 8), "Intermediate": (16, 16, 40), "Expert": (30, 16, 99)}
grid = Grid(*difficulties[difficulty])
print(grid.visible_grid())
columns = {ascii_lowercase[i]: i for i in range(0, difficulties[difficulty][0] + 1)}
while grid.alive:
    inp = user_input()
    if len(inp) > 2:
        if str(inp[2]).lower() == "f":
            flag = True
    elif len(inp) < 2:
        invalid_input()
        continue
    else:
        flag = False
    if not inp[1].isdigit():
        invalid_input()
        continue
    if not len(inp[0]) == 1:
        invalid_input()
        continue
    if (int(inp[1])) > len(grid.grid) or not inp[0].lower() in columns:
        invalid_input()
        continue
    loc = (columns[inp[0].lower()], int(inp[1]) - 1)
    grid.reveal(loc, flag)
print(grid.finish_time())
