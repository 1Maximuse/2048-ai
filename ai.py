class Tree:
    grid = []
    child = []
    last_move = None
    def __init__(self, grid, last_move):
        self.grid = grid
        self.last_move = last_move
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
    combined = [[False for x in range(4)] for y in range(4)]
    if direction == 0:
        for y in range(1, 4):
            for x in range(4):
                if grid[y][x] is None:
                    continue
                dy = y
                while (dy >= 0):
                    dy -= 1
                    if grid[dy][x] and grid[dy][x] != grid[y][x]:
                        break
                dy += 1
                if dy == y:
                    continue
                if grid[dy][x] == grid[y][x] and not combined[dy][x]:
                    grid[dy][x] *= 2
                    grid[y][x] = None
                    combined[dy][x] = True
                elif grid[dy][x] is None:
                    grid[dy][x] = grid[y][x]
                    grid[y][x] = None
    if direction == 1:
        for y in range(2, -1, -1):
            for x in range(4):
                if grid[y][x] is None:
                    continue
                dy = y
                while (dy < 4):
                    dy += 1
                    if grid[dy][x] and grid[dy][x] != grid[y][x]:
                        break
                dy -= 1
                if dy == y:
                    continue
                if grid[dy][x] == grid[y][x] and not combined[dy][x]:
                    grid[dy][x] *= 2
                    grid[y][x] = None
                    combined[dy][x] = True
                elif grid[dy][x] is None:
                    grid[dy][x] = grid[y][x]
                    grid[y][x] = None
    if direction == 2:
        for x in range(1, 4):
            for y in range(4):
                if grid[y][x] is None:
                    continue
                dx = x
                while (dx >= 0):
                    dx -= 1
                    if grid[y][dx] and grid[y][dx] != grid[y][x]:
                        break
                dx += 1
                if dx == x:
                    continue
                if grid[y][dx] == grid[y][x] and not combined[y][dx]:
                    grid[y][dx] *= 2
                    grid[y][x] = None
                    combined[y][dx] = True
                elif grid[y][dx] is None:
                    grid[y][dx] = grid[y][x]
                    grid[y][x] = None
    if direction == 3:
        for x in range(2, -1, -1):
            for y in range(4):
                if grid[y][x] is None:
                    continue
                dx = x
                while (dx < 4):
                    dx += 1
                    if grid[y][dx] and grid[y][dx] != grid[y][x]:
                        break
                dx -= 1
                if dx == x:
                    continue
                if grid[y][dx] == grid[y][x] and not combined[y][dx]:
                    grid[y][dx] *= 2
                    grid[y][x] = None
                    combined[y][dx] = True
                elif grid[y][dx] is None:
                    grid[y][dx] = grid[y][x]
                    grid[y][x] = None
    return grid

def spawn_tile(grid, x, y, value):
    grid[y][x] = value
    return grid

def build_tree(grid, last_move, depth, max_depth):
    if depth == max_depth:
        return Tree(grid, last_move)
    root = Tree(grid, last_move)
    if depth % 2 == 0: # player turn
        for i in range(4):
            if try_move(grid, i):
                root.append_child(build_tree(move(grid.copy(), i), i, depth + 1, max_depth))
    else: # computer turn
        for y in range(4):
            for x in range(4):
                if grid[y][x] is None:
                    root.append_child(build_tree(spawn_tile(grid.copy(), x, y, 2), (x, y, 2), depth + 1, max_depth))
                    root.append_child(build_tree(spawn_tile(grid.copy(), x, y, 4), (x, y, 4), depth + 1, max_depth))
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
    tree = build_tree(numgrid, None, 0, 2)
    best_value, last_move = minimax(tree, 2, 1)
    return last_move

def calculate_empty_tiles(grid):
    empty = 0
    for x in range(4):
        for y in range(4):
            if grid[x][y].value is None:
                empty += 1
    return empty

def calculate_adjacent_differences(grid):
    diff = 0
    for x in range(4):
        for y in range(3):
            diff += abs(grid[x][y].value - grid[x][y+1].value)
    for y in range(4):
        for x in range(3):
            diff += abs(grid[x][y].value - grid[x+1][y].value)
    return diff

def calculate_middle_value(grid):
    return grid[1][1].value + grid[1][2].value + grid[2][1].value + grid[2][2].value

def calculate_heuristic_value(grid):
    weight_empty_tiles = 1000
    weight_adjacent_differences = 10
    weight_middle_value = 10
    empty_tiles = calculate_empty_tiles(grid)
    adjacent_differences = calculate_adjacent_differences(grid)
    middle_value = calculate_middle_value(grid)
    return weight_empty_tiles * empty_tiles - weight_adjacent_differences * adjacent_differences - weight_middle_value * middle_value

def minimax(node, depth, turn): # depth mau berapa banyak search kedalamannya
    if depth == 0: # leaf node
        return calculate_heuristic_value(node.grid), node.last_move
    if turn == 1: # player turn
        best_value = -999999
        last_move = None
        for child in node.child:
            val, mv = minimax(child, depth - 1, 2)
            if val > best_value:
                best_value = val
                last_move = mv
            best_value = max(best_value, val)
    else:
        best_value = +999999
        last_move = None
        for child in node.child:
            val, mv = minimax(child, depth - 1, 1)
            if val < best_value:
                best_value = val
                last_move = mv
    return best_value, last_move

def alphabeta_pruning(node, depth, alfa, beta, turn): # depth mau berapa banyak search kedalamannya
    if depth == 0: # leaf node
        return calculate_heuristic_value(node.grid)
    if turn == 1: # player turn
        for child in node.child:
            alfa = max(alfa, alphabeta_pruning(child, depth - 1, alfa, beta, 2))
            if alfa > beta:
                break
        return alfa
    else:
        for child in node.child:
            beta = min(beta, alphabeta_pruning(child, depth - 1, alfa, beta, 1))
            if beta < alfa:
                break
        return beta

def expectimax(node, depth, turn): # depth mau berapa banyak search kedalamannya
    if depth == 0: # leaf node
        return calculate_heuristic_value(node.grid)
    if turn == 1: # player turn
        best_value = -999999
        for child in node.child:
            val = expectimax(child, depth - 1, 2)
            best_value = max(best_value, val)
        return best_value
    else:
        expected_value = 0
        for child in node.child:
            val = expectimax(child, depth - 1, 1)
            expected_value += val / len(node.child)
        return expected_value
