import time

class Tree:
    grid = []
    child = []
    def __init__(self, grid):
        self.grid = grid
    def appendChild(self, child):
        self.child.append(child)

def tryMove(grid, dir):
    bisa = False
    if dir == 0: # up
        for y in range(1, 4):
            for x in range(4):
                if not grid[y][x]: continue
                ny = y - 1
                while ny >= 0 and not grid[ny][x]: ny -= 1
                if y != ny + 1 or ny >= 0 and grid[y][x] == grid[ny][x]:
                    bisa = True
                    break
            if bisa: break
    elif dir == 1: # down
        for y in range(2, -1, -1):
            for x in range(4):
                if not grid[y][x]: continue
                ny = y + 1
                while ny < 4 and not grid[ny][x]: ny += 1
                if y != ny - 1 or ny < 4 and grid[y][x] == grid[ny][x]:
                    bisa = True
                    break
            if bisa: break
    elif dir == 2: # left
        for x in range(1, 4):
            for y in range(4):
                if not grid[y][x]: continue
                nx = x - 1
                while nx >= 0 and not grid[y][nx]: nx -= 1
                if x != nx + 1 or nx >= 0 and grid[y][x] == grid[y][nx]:
                    bisa = True
                    break
            if bisa: break
    elif dir == 3: # right
        for x in range(2, -1, -1):
            for y in range(4):
                if not grid[y][x]: continue
                nx = x + 1
                while nx < 4 and not grid[y][nx]: nx += 1
                if x != nx - 1 or nx < 4 and grid[y][x] == grid[y][nx]:
                    bisa = True
                    break
            if bisa: break
    return bisa

def move(grid, dir):
    # TODO
    return grid

def buildMinimaxTree(grid, depth, maxDepth):
    if depth == maxDepth: return Tree(grid)
    root = Tree(grid)
    if depth % 2 == 0: # player turn
        for i in range(4):
            if tryMove(grid, i):
                root.appendChild(buildMinimaxTree(move(grid, i), depth + 1, maxDepth))
    # else: # computer turn
    #     for y in range(4):
    #         for x in range(4):
    #             TODO
    return root

def convertToNumGrid(grid):
    res = []
    for y in range(4):
        row = []
        for x in range(4):
            row.append(grid[y][x].value)
        res.append(row)
    return res

def calculateNextMove(grid):
    numgrid = convertToNumGrid(grid)
    tree = []
    tree = buildMinimaxTree(numgrid, 0, 2)