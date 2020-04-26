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

def calculate_empty_tiles(grid):
    E = 0
    for x in range(4):
        for y in range(4):
            if (grid[x][y].value == None)
                E+=1
    return E

def calculate_adjecent_differences(grid):
    D = 0
    for x in range(4):
        for y in range(3):
            D = D + abs(grid[x][y].value - grid[x][y+1].value)
    for y in range(4):
        for x in range(3):
            E = D + abs(grid[x][y].value - grid[x+1][y].value)
    return D

def calculate_middle_value(grid):
    M = grid[1][1].value + grid[1][2].value + grid[2][1].value + grid[2][2].value
    return M

def calculate_heuristic_value(grid):
    A = 1000
    B = 10
    C = 10
    E = calculate_empty_tiles(grid)
    D = calculate_adjecent_differences(grid)
    M = calculate_middle_value(grid)
    H = A * E - B * D - C * M
    return H

def minimax(node, depth, turn): # depth mau berapa banyak search kedalamannya
    if depth == 0 # leaf node
        return calculate_heuristic_value
    if turn == 1 # player turn
        bestValue = -999999
        for # each child of node
            val = minimax(child, depth - 1, 2)
            bestValue = max(bestValue, val)
        return bestValue
    else
        bestValue = +999999
        for # each child of node
            val = minimax(child, depth - 1, 1)
            bestValue = min(bestValue, val)
        return bestValue

def alfabeta_pruning(node, depth, alfa, beta, turn): # depth mau berapa banyak search kedalamannya
    if depth == 0 # leaf node
        return calculate_heuristic_value
    if turn == 1 # player turn
        for # each child of node
            alfa = max(alfa, alphabeta_pruning(child, depth - 1, alfa, beta, 2))
            if alfa > beta
                break
        return alfa
    else
        for # each child of node
            beta = min(beta, alphabeta_pruning(child, depth - 1, alfa, beta, 1))
            if beta < alfa
                break
        return beta

def expectimax(node, depth, turn): # depth mau berapa banyak search kedalamannya
    if depth == 0 # leaf node
        return calculate_heuristic_value
    if turn == 1 # player turn
        bestValue = -999999
        for # each child of node
            val = expectimax(child, depth - 1, 2)
            bestValue = max(bestValue, val)
        return bestValue
    else
        expectedValue = 0
        for # each child of node
            val = expectimax(child, depth - 1, 1)
            expectedValue += Probability[child] * val
        return expectedValue