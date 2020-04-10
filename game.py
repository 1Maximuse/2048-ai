import sys, random, pygame
from random import randint
from pygame import gfxdraw, Rect, Color

screen = None

animSpeed = None

font55 = None
font45 = None
font35 = None
font30 = None
colors = None

def initConstants(scr):
    global screen, animSpeed, font55, font45, font35, font30, colors
    screen = scr
    animSpeed = 5
    font55 = pygame.font.Font('font.ttf', 55)
    font45 = pygame.font.Font('font.ttf', 45)
    font35 = pygame.font.Font('font.ttf', 35)
    font30 = pygame.font.Font('font.ttf', 30)
    colors = {
        'background': (250, 248, 239),
        'game': (187,173,160),
        'empty': (205, 192, 180),
        '2': (238, 228, 218),
        '4': (237, 224, 200),
        '8': (242, 177, 121),
        '16': (245, 149, 99),
        '32': (246, 124, 95),
        '64': (246, 94, 59),
        '128': (237, 207, 114),
        '256': (237, 204, 97),
        '512': (237, 200, 80),
        '1024': (237, 197, 63),
        '2048': (237, 194, 46),
        'super': (60, 58, 50),
        'darktext': (119, 110, 101),
        'lighttext': (249, 246, 242)
    }

def roundedRect(x, y, width, height, radius, color):
    pygame.draw.rect(screen, colors[color], Rect(x, y + radius, width, height - radius - radius))
    pygame.draw.rect(screen, colors[color], Rect(x + radius, y, width - radius - radius, height))
    pygame.gfxdraw.filled_circle(screen, x + radius, y + radius, radius, colors[color])
    pygame.gfxdraw.aacircle(screen, x + radius, y + radius, radius, colors[color])
    pygame.gfxdraw.filled_circle(screen, x + radius, y + height - radius - 1, radius, colors[color])
    pygame.gfxdraw.aacircle(screen, x + radius, y + height - radius - 1, radius, colors[color])
    pygame.gfxdraw.filled_circle(screen, x + width - radius - 1, y + height - radius - 1, radius, colors[color])
    pygame.gfxdraw.aacircle(screen, x + width - radius - 1, y + height - radius - 1, radius, colors[color])
    pygame.gfxdraw.filled_circle(screen, x + width - radius - 1, y + radius, radius, colors[color])
    pygame.gfxdraw.aacircle(screen, x + width - radius - 1, y + radius, radius, colors[color])

def moveUp(grid):
    newDir = [[-1 for x in range(4)] for y in range(4)]
    changed = False
    done = [[False for x in range(4)] for y in range(4)]
    for y in range(1, 4):
        for x in range(4):
            if not grid[y][x].value: continue
            ny = y - 1
            while ny >= 0 and not grid[ny][x].value: ny -= 1
            if ny >= 0 and not done[ny][x] and grid[y][x].value == grid[ny][x].value:
                grid[ny][x].value *= 2
                done[ny][x] = True
                grid[y][x].value = None
                changed = True
                newDir[ny][x] = y * 4 + x
            elif y != ny + 1:
                grid[ny + 1][x].value = grid[y][x].value
                grid[y][x].value = None
                changed = True
                newDir[ny + 1][x] = y * 4 + x
    if changed:
        grid = resetTimer(grid)
        for y in range(4):
            for x in range(4):
                if newDir[y][x] != -1:
                    grid[y][x].moving = newDir[y][x]
                    grid[y][x].timer = animSpeed
        grid = spawnTile(grid)
    return grid
    
def moveDown(grid):
    newDir = [[-1 for x in range(4)] for y in range(4)]
    changed = False
    done = [[False for x in range(4)] for y in range(4)]
    for y in range(2, -1, -1):
        for x in range(4):
            if not grid[y][x].value: continue
            ny = y + 1
            while ny < 4 and not grid[ny][x].value: ny += 1
            if ny < 4 and not done[ny][x] and grid[y][x].value == grid[ny][x].value:
                grid[ny][x].value *= 2
                done[ny][x] = True
                grid[y][x].value = None
                changed = True
                newDir[ny][x] = y * 4 + x
            elif y != ny - 1:
                grid[ny - 1][x].value = grid[y][x].value
                grid[y][x].value = None
                changed = True
                newDir[ny - 1][x] = y * 4 + x
    if changed:
        grid = resetTimer(grid)
        for y in range(4):
            for x in range(4):
                if newDir[y][x] != -1:
                    grid[y][x].moving = newDir[y][x]
                    grid[y][x].timer = animSpeed
        grid = spawnTile(grid)
    return grid
    
def moveLeft(grid):
    newDir = [[-1 for x in range(4)] for y in range(4)]
    changed = False
    done = [[False for x in range(4)] for y in range(4)]
    for x in range(1, 4):
        for y in range(4):
            if not grid[y][x].value: continue
            nx = x - 1
            while nx >= 0 and not grid[y][nx].value: nx -= 1
            if nx >= 0 and not done[y][nx] and grid[y][x].value == grid[y][nx].value:
                grid[y][nx].value *= 2
                done[y][nx] = True
                grid[y][x].value = None
                changed = True
                newDir[y][nx] = y * 4 + x
            elif x != nx + 1:
                grid[y][nx + 1].value = grid[y][x].value
                grid[y][x].value = None
                changed = True
                newDir[y][nx + 1] = y * 4 + x
    if changed:
        grid = resetTimer(grid)
        for y in range(4):
            for x in range(4):
                if newDir[y][x] != -1:
                    grid[y][x].moving = newDir[y][x]
                    grid[y][x].timer = animSpeed
        grid = spawnTile(grid)
    return grid

def moveRight(grid):
    newDir = [[-1 for x in range(4)] for y in range(4)]
    changed = False
    done = [[False for x in range(4)] for y in range(4)]
    for x in range(2, -1, -1):
        for y in range(4):
            if not grid[y][x].value: continue
            nx = x + 1
            while nx < 4 and not grid[y][nx].value: nx += 1
            if nx < 4 and not done[y][nx] and grid[y][x].value == grid[y][nx].value:
                grid[y][nx].value *= 2
                done[y][nx] = True
                grid[y][x].value = None
                changed = True
                newDir[y][nx] = y * 4 + x
            elif x != nx - 1:
                grid[y][nx - 1].value = grid[y][x].value
                grid[y][x].value = None
                changed = True
                newDir[y][nx - 1] = y * 4 + x
    if changed:
        grid = resetTimer(grid)
        for y in range(4):
            for x in range(4):
                if newDir[y][x] != -1:
                    grid[y][x].moving = newDir[y][x]
                    grid[y][x].timer = animSpeed
        grid = spawnTile(grid)
    return grid

def spawnTile(grid):
    new = randint(0, 15)
    while grid[new // 4][new % 4].value: new = randint(0, 15)
    grid[new // 4][new % 4].value = 2 if randint(0, 99) < 90 else 4
    grid[new // 4][new % 4].new = animSpeed + animSpeed
    return grid

def resetTimer(grid):
    for y in range(4):
        for x in range(4):
            grid[y][x].moving = -1
            grid[y][x].timer = 0
            grid[y][x].new = 0
    return grid

class Tile:
    value = None
    x = None
    y = None
    moving = -1
    timer = 0
    new = 0
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value
    def draw(self):
        offsetx = 0
        offsety = 0
        if self.moving != -1:
            my = self.moving // 4
            mx = self.moving % 4
            if self.y == my:
                mx -= self.x
                offsetx = (mx * 114 - 14) * self.timer // animSpeed
            elif self.x == mx:
                my -= self.y
                offsety = (my * 114 - 14) * self.timer // animSpeed

        size = 100 * max(animSpeed - self.new, 0) // animSpeed
        roundedRect((screen.get_width() - 470) // 2 + 14 + 114 * self.x, (screen.get_height() - 470) // 2 + 14 + 114 * self.y, 100, 100, 6, 'empty')
        if size > 0:
            roundedRect((screen.get_width() - 470) // 2 + 14 + 114 * self.x + offsetx + 50 - size // 2, (screen.get_height() - 470) // 2 + 14 + 114 * self.y + offsety + 50 - size // 2, size, size, 6, 'empty' if not self.value else str(self.value) if self.value <= 2048 else 'super')
        if self.value and size > 0:
            if self.value < 128:
                text = font55.render(str(self.value), True, colors['darktext'] if self.value < 8 else colors['lighttext'])
            elif self.value < 1024:
                text = font45.render(str(self.value), True, colors['darktext'] if self.value < 8 else colors['lighttext'])
            elif self.value <= 2048:
                text = font35.render(str(self.value), True, colors['darktext'] if self.value < 8 else colors['lighttext'])
            else:
                text = font30.render(str(self.value), True, colors['darktext'] if self.value < 8 else colors['lighttext'])
            screen.blit(text, text.get_rect(center = ((screen.get_width() - 470) // 2 + 114 * self.x + 64 + offsetx, (screen.get_height() - 470) // 2 + 114 * self.y + 64 + offsety)))

def spawnFirstTiles(grid):
    s1 = randint(0, 15)
    s2 = randint(0, 15)
    while s2 == s1: s2 = randint(0, 15)
    grid[s1 // 4][s1 % 4].value = 2 if randint(0, 99) < 90 else 4
    grid[s2 // 4][s2 % 4].value = 2 if randint(0, 99) < 90 else 4
    grid[s1 // 4][s1 % 4].new = animSpeed + animSpeed
    grid[s2 // 4][s2 % 4].new = animSpeed + animSpeed
    return grid

def gameLoop(grid, screen):

    for y in range(4):
        for x in range(4):
            if grid[y][x].new != 0: grid[y][x].new -= 1
            if grid[y][x].moving != -1:
                grid[y][x].timer -= 1
                if grid[y][x].timer == 0:
                    grid[y][x].moving = -1

    roundedRect((screen.get_width() - 470) // 2, (screen.get_height() - 470) // 2, 470, 470, 6, 'game')
    for y in range(4):
        for x in range(4):
            if grid[y][x].moving == -1: grid[y][x].draw()
    for y in range(4):
        for x in range(4):
            if grid[y][x].moving != -1: grid[y][x].draw()
