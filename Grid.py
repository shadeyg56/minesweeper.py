import random
from tabulate import tabulate
import os
import datetime
from string import ascii_uppercase


class Grid:
    def __init__(self, width, height, mine_num):
        self.width = width
        self.height = height
        self.mine_num = mine_num
        self.flagged = []
        self.visible = []
        self.neighbors = [(-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (0, -1), (1, -1)]
        # grid is generated upon init
        self.generate()
        self.alive = True
        self.first_move = True
        # writes the grid to a .txt file, mostly for debugging purposes. Good for testing.
        txt = open("grid.txt", "w", encoding="utf-8")
        txt.write(self.show())
        txt.close()

    def generate(self):
        mines_placed = 0
        # class stores 2 versions of the grid. one with values of each cell and one that the user interacts with
        self.grid = [[0 for i in range(0, self.width)] for i in range(0, self.height)]
        self.render = [[" " for i in range(0, self.width)] for i in range(0, self.height)]
        while mines_placed != self.mine_num:
            # randomly select a location to become a mine
            x = random.randint(0, self.width-1)
            y = random.randint(0, self.height-1)
            if self.grid[y][x] != "X":
                self.grid[y][x] = "X"
                # loop through each neighboring cell and increment it by 1
                self.replace_neighbors((x, y))
                mines_placed += 1

    def reveal(self, loc, flag):
        # the cell must not have been revealed
        if self.first_move:
            self.start_time = datetime.datetime.now()
        if loc not in self.visible:
            # add the cell to flagged cells
            if flag:
                if len(self.flagged) <= self.mine_num:
                    self.flagged.append(loc)
                    self.visible.append(loc)
            # if the value of the cell is 0, reveal all of it's neighbors
            elif self.grid[loc[1]][loc[0]] == 0:
                self.visible.append(loc)
                self.get_neighbors(loc)
            else:
                self.visible.append(loc)
            # if the cell is a mine and has not been flagged by the user, trigger game over
            if self.is_mine(loc):
                # if mine hit on first turn, move it to the closest available space to the top left corner
                if self.first_move:
                    self.visible.remove(loc)
                    self.move_mine(loc)
                elif not flag:
                    print("Game Over! You hit a mine.")
                    print(self.show())
                    self.alive = False
                    self.end_time = datetime.datetime.now()
                    return
        # if the cell has already been flagged, and the user selected to flag it it will be unflagged.
        elif loc in self.flagged:
            if flag:
                self.flagged.remove(loc)
                self.visible.remove(loc)
                self.render[loc[1]][loc[0]] = " "
        if self.game_won():
            print("Congratulations! You won.")
            print(self.show())
            self.alive = False
            self.end_time = datetime.datetime.now()
        else:
            os.system("cls")
            print(f"Flags: {len(self.flagged)}/{self.mine_num}")
            print(self.visible_grid())
            self.first_move = False

    def is_mine(self, loc):
        if self.grid[loc[1]][loc[0]] == "X":
            return True
        else:
            return False

    # func to move mine if hit on first turn. moves it to the closest cell to the top left corner (cannot be occupied by a mine)
    def move_mine(self, loc):
        self.grid[loc[1]][loc[0]] = 0
        self.replace_neighbors(loc, increase=False)
        new_loc = (0, 0)
        while self.grid[new_loc[1]][new_loc[0]] == "X":
            new_loc = (new_loc[0]+1, new_loc[1])
            if new_loc[0] == self.width-1:
                new_loc = (0, new_loc[1]+1)
        self.grid[new_loc[1]][new_loc[0]] = "X"
        self.replace_neighbors(new_loc)
        self.get_neighbors(loc)
        txt = open("grid.txt", "w", encoding="utf-8")
        txt.write(self.show())
        txt.close()


    def game_won(self):
        # if num of visible cells equals the total number of cells, the game is won
        # because it is impossible to reveal every cell without using flags there is no need for any other checks
        if len(self.visible) == self.height*self.width:
            return True
        else:
            return False

    # func that returns the grid that the user sees in a nice table
    # uses tabulate package because i'm lazy and works well for this. no need to reinvent the wheel.
    def visible_grid(self):
        for row in range(0, self.height):
            for cell in range(0, self.width):
                loc = (cell, row)
                if loc in self.visible:
                    if loc in self.flagged:
                        self.render[row][cell] = "F"
                    else:
                        self.render[row][cell] = self.grid[row][cell]
        headers = [ascii_uppercase[i] for i in range(0, self.width+1)]
        headers.insert(0, "")
        table = tabulate(self.render, headers=headers, tablefmt="fancy_grid", showindex=[i for i in range(1, self.height+1)], numalign="center", stralign="center")
        return table

    # shows the actual grid w/ real values in a table
    def show(self):
        headers = [ascii_uppercase[i] for i in range(0, self.width+1)]
        headers.insert(0, "")
        table = tabulate(self.grid, headers=headers, tablefmt="fancy_grid", showindex=[i for i in range(1, self.height+1)], numalign="center", stralign="center")
        return table

    # func to by default increment all neighbors of a cell. will decrement if increase=False
    def replace_neighbors(self, loc, increase=True):
        x = loc[0]
        y = loc[1]
        for n in self.neighbors:
            nexty = n[1]+y
            nextx = n[0]+x
            if nexty < len(self.grid) and nextx < len(self.grid[y]):
                if self.grid[nexty][nextx] != "X" and nexty != -1 and nextx != -1:
                    if increase:
                        self.grid[nexty][nextx] += 1
                    else:
                        self.grid[nexty][nextx] -= 1

    # reveals all neighbors of a zero-value cell. If said cell has a zero cell as a neighbor, it is added to the queue and later has its neighbors revealed
    # probably not the most inexpensive way to handle this, but works fine in this case.
    def get_neighbors(self, loc):
        queue = []
        x = loc[0]
        y = loc[1]
        for n in self.neighbors:
            nextx = n[0]+x
            nexty = n[1]+y
            if nexty < len(self.grid) and nextx < len(self.grid[y]):
                if nexty != -1 and nextx != -1:
                    if self.grid[nexty][nextx] == 0:
                        if (nextx, nexty) not in self.visible:
                            queue.append((nextx, nexty))
                            self.visible.append((nextx, nexty))
                    elif self.grid[nexty][nextx] != "X":
                        if (nextx, nexty) not in self.visible:
                            self.visible.append((nextx, nexty))
        for loc in queue:
            self.get_neighbors(loc)

    def finish_time(self):
        delta = self.end_time - self.start_time
        minutes = int(delta.total_seconds() // 60)
        sec = round(delta.total_seconds() - (minutes * 60))
        return f"Time: {minutes}:{sec}"
