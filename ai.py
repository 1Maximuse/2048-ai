from copy import deepcopy

class Tree:
    grid = []
    child = None
    last_move = -1
    def __init__(self, grid, last_move, child):
        self.grid = deepcopy(grid)
        self.child = deepcopy(child)
        self.last_move = last_move

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

def move(oldgrid, direction):
    grid = deepcopy(oldgrid)
    done = [[False for x in range(4)] for y in range(4)]
    if direction == 0:
        for y in range(1, 4):
            for x in range(4):
                if not grid[y][x]:
                    continue
                nexty = y - 1
                while nexty >= 0 and not grid[nexty][x]:
                    nexty -= 1
                if nexty >= 0 and not done[nexty][x] and grid[y][x] == grid[nexty][x]:
                    grid[nexty][x] *= 2
                    done[nexty][x] = True
                    grid[y][x] = None
                elif y != nexty + 1:
                    grid[nexty + 1][x] = grid[y][x]
                    grid[y][x] = None
    elif direction == 1:
        for y in range(2, -1, -1):
            for x in range(4):
                if not grid[y][x]:
                    continue
                nexty = y + 1
                while nexty < 4 and not grid[nexty][x]:
                    nexty += 1
                if nexty < 4 and not done[nexty][x] and grid[y][x] == grid[nexty][x]:
                    grid[nexty][x] *= 2
                    done[nexty][x] = True
                    grid[y][x] = None
                elif y != nexty - 1:
                    grid[nexty - 1][x] = grid[y][x]
                    grid[y][x] = None
    elif direction == 2:
        for x in range(1, 4):
            for y in range(4):
                if not grid[y][x]:
                    continue
                nextx = x - 1
                while nextx >= 0 and not grid[x][nextx]:
                    nextx -= 1
                if nextx >= 0 and not done[y][nextx] and grid[y][x] == grid[y][nextx]:
                    grid[y][nextx] *= 2
                    done[y][nextx] = True
                    grid[y][x] = None
                elif x != nextx + 1:
                    grid[y][nextx + 1] = grid[y][x]
                    grid[y][x] = None
    elif direction == 3:
        for x in range(2, -1, -1):
            for y in range(4):
                if not grid[y][x]:
                    continue
                nextx = x + 1
                while nextx < 4 and not grid[x][nextx]:
                    nextx += 1
                if nextx < 4 and not done[y][nextx] and grid[y][x] == grid[y][nextx]:
                    grid[y][nextx] *= 2
                    done[y][nextx] = True
                    grid[y][x] = None
                elif x != nextx - 1:
                    grid[y][nextx - 1] = grid[y][x]
                    grid[y][x] = None
    return grid

def spawn_tile(oldgrid, x, y, value):
    grid = deepcopy(oldgrid)
    grid[y][x] = value
    return grid

def build_tree(grid, last_move, depth, max_depth):
    if depth == max_depth:
        return Tree(grid, last_move, [])
    child = []
    if depth % 2 == 0: # player turn
        for i in range(4):
            if try_move(grid, i):
                child.append(build_tree(move(grid, i), i, depth + 1, max_depth))
    else: # computer turn
        for y in range(4):
            for x in range(4):
                if grid[y][x] is None:
                    child.append(build_tree(spawn_tile(grid, x, y, 2), -2, depth + 1, max_depth))
                    child.append(build_tree(spawn_tile(grid, x, y, 4), -4, depth + 1, max_depth))
    return Tree(grid, last_move, child)

def convert_to_numgrid(grid):
    res = []
    for y in range(4):
        row = []
        for x in range(4):
            row.append(grid[y][x].value)
        res.append(row)
    return res

def calculate_next_move(grid, mode):
    depth = 2
    numgrid = convert_to_numgrid(grid)
    tree = build_tree(numgrid, None, 0, depth)
    if mode == 0:
        res_path = minimax(tree, depth, 1)[1]
    elif mode == 1:
        res_path = alphabeta_pruning(tree, depth, -999999, 999999, 1)[1]
    else:
        res_path = expectimax(tree, depth, 1)[1]
    return res_path[0]

def calculate_empty_tiles(grid):
    empty = 0
    for x in range(4):
        for y in range(4):
            if grid[x][y] is None:
                empty += 1
    return empty

def calculate_adjacent_differences(grid):
    diff = 0
    for x in range(4):
        for y in range(3):
            diff += abs(0 if grid[x][y] is None else grid[x][y] - 0 if grid[x][y+1] is None else grid[x][y+1])
    for y in range(4):
        for x in range(3):
            diff += abs(0 if grid[x][y] is None else grid[x][y] - 0 if grid[x+1][y] is None else grid[x+1][y])
    return diff

def calculate_middle_value(grid):
    a11 = 0 if grid[1][1] is None else grid[1][1]
    a12 = 0 if grid[1][2] is None else grid[1][2]
    a21 = 0 if grid[2][1] is None else grid[2][1]
    a22 = 0 if grid[2][2] is None else grid[2][2]
    return a11 + a12 + a21 + a22

def calculate_heuristic_value(grid):
    weight_empty_tiles = 1000
    weight_adjacent_differences = 10
    weight_middle_value = 10
    empty_tiles = calculate_empty_tiles(grid)
    adjacent_differences = calculate_adjacent_differences(grid)
    middle_value = calculate_middle_value(grid)
    return weight_empty_tiles * empty_tiles - weight_adjacent_differences * adjacent_differences - weight_middle_value * middle_value

def minimax(node, depth, turn): # depth mau berapa banyak search kedalamannya
    # print(depth)
    if depth == 0: # leaf node
        return calculate_heuristic_value(node.grid), [node.last_move] if node.last_move is not None and node.last_move >= 0 else []
    last_move = []
    if node.last_move is not None and node.last_move >= 0:
        last_move.append(node.last_move)
    if turn == 1: # player turn
        best_value = -999999
        max_move = []
        for child in node.child:
            val, mv = minimax(child, depth - 1, 2)
            if val > best_value:
                best_value = val
                max_move = mv
    else:
        best_value = +999999
        max_move = []
        for child in node.child:
            val, mv = minimax(child, depth - 1, 1)
            if val < best_value:
                best_value = val
                max_move = mv
    last_move += max_move
    return best_value, last_move

def alphabeta_pruning(node, depth, alfa, beta, turn): # depth mau berapa banyak search kedalamannya
    if depth == 0: # leaf node
        return calculate_heuristic_value(node.grid), [node.last_move] if node.last_move is not None and node.last_move >= 0 else []
    last_move = []
    if node.last_move is not None and node.last_move >= 0:
        last_move.append(node.last_move)
    if turn == 1: # player turn
        max_move = []
        for child in node.child:
            val, mv = alphabeta_pruning(child, depth - 1, alfa, beta, 2)
            if val > alfa:
                alfa = val
                max_move = mv
            if alfa > beta:
                break
        last_move += max_move
        return alfa, last_move
    else:
        max_move = []
        for child in node.child:
            val, mv = alphabeta_pruning(child, depth - 1, alfa, beta, 1)
            if val < beta:
                beta = val
                max_move = mv
            if beta < alfa:
                break
        last_move += max_move
        return beta, last_move

def expectimax(node, depth, turn): # depth mau berapa banyak search kedalamannya
    if depth == 0: # leaf node
        return calculate_heuristic_value(node.grid), [node.last_move] if node.last_move is not None and node.last_move >= 0 else []
    last_move = []
    if node.last_move is not None and node.last_move >= 0:
        last_move.append(node.last_move)
    if turn == 1: # player turn
        max_move = []
        best_value = -999999
        for child in node.child:
            val, mv = expectimax(child, depth - 1, 2)
            if val > best_value:
                best_value = val
                max_move = mv
        last_move += max_move
        return best_value, last_move
    else:
        expected_value = 0
        next_move = []
        for child in node.child:
            val, mv = expectimax(child, depth - 1, 1)
            expected_value += val * 0.9 if child.last_move == -2 else 0.1
            next_move = mv
        expected_value /= len(node.child) / 2
        last_move += next_move
        return expected_value, last_move
