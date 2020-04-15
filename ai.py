class Tree:
    grid = []
    child = []
    def __init__(self, grid):
        self.grid = grid
    def append_child(self, child):
        self.child.append(child)

def try_move(grid, direction):
    bisa = False
    if direction == 0: # up
        for y in range(1, 4):
            for x in range(4):
                if not grid[y][x]:
                    continue
                newy = y - 1
                while newy >= 0 and not grid[newy][x]:
                    newy -= 1
                if y != newy + 1 or newy >= 0 and grid[y][x] == grid[newy][x]:
                    bisa = True
                    break
            if bisa:
                break
    elif direction == 1: # down
        for y in range(2, -1, -1):
            for x in range(4):
                if not grid[y][x]:
                    continue
                newy = y + 1
                while newy < 4 and not grid[newy][x]:
                    newy += 1
                if y != newy - 1 or newy < 4 and grid[y][x] == grid[newy][x]:
                    bisa = True
                    break
            if bisa:
                break
    elif direction == 2: # left
        for x in range(1, 4):
            for y in range(4):
                if not grid[y][x]:
                    continue
                newx = x - 1
                while newx >= 0 and not grid[y][newx]:
                    newx -= 1
                if x != newx + 1 or newx >= 0 and grid[y][x] == grid[y][newx]:
                    bisa = True
                    break
            if bisa:
                break
    elif direction == 3: # right
        for x in range(2, -1, -1):
            for y in range(4):
                if not grid[y][x]:
                    continue
                newx = x + 1
                while newx < 4 and not grid[y][newx]:
                    newx += 1
                if x != newx - 1 or newx < 4 and grid[y][x] == grid[y][newx]:
                    bisa = True
                    break
            if bisa:
                break
    return bisa

def move(grid, direction):
    # TODO
    return grid

def build_minimax_tree(grid, depth, max_depth):
    if depth == max_depth:
        return Tree(grid)
    root = Tree(grid)
    if depth % 2 == 0: # player turn
        for i in range(4):
            if try_move(grid, i):
                root.append_child(build_minimax_tree(move(grid, i), depth + 1, max_depth))
    # else: # computer turn
    #     for y in range(4):
    #         for x in range(4):
    #             TODO
    return root

def convert_to_numgrid(grid):
    res = []
    for y in range(4):
        row = []
        for x in range(4):
            row.append(grid[y][x].value)
        res.append(row)
    return res

def calculate_next_move(grid):
    numgrid = convert_to_numgrid(grid)
    tree = []
    tree = build_minimax_tree(numgrid, 0, 2)
