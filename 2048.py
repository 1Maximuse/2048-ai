import sys, random, pygame
from random import randint
from pygame import gfxdraw, Rect, Color

pygame.init()
clock = pygame.time.Clock()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption('2048 AI')

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
    changed = False
    done = [[False for x in range(4)] for y in range(4)]
    for y in range(1, 4):
        for x in range(4):
            if done[y][x] or not grid[y][x].value: continue
            ny = y - 1
            while ny >= 0 and not grid[ny][x].value: ny -= 1
            if ny >= 0 and grid[y][x].value == grid[ny][x].value:
                grid[ny][x].value *= 2
                done[ny][x] = True
                grid[y][x].value = None
                changed = True
            elif y != ny + 1:
                grid[ny + 1][x].value = grid[y][x].value
                grid[y][x].value = None
                changed = True
    if changed: grid = spawnTile(grid)
    return grid
    
def moveDown(grid):
    changed = False
    done = [[False for x in range(4)] for y in range(4)]
    for y in range(2, -1, -1):
        for x in range(4):
            if done[y][x] or not grid[y][x].value: continue
            ny = y + 1
            while ny < 4 and not grid[ny][x].value: ny += 1
            if ny < 4 and grid[y][x].value == grid[ny][x].value:
                grid[ny][x].value *= 2
                done[ny][x] = True
                grid[y][x].value = None
                changed = True
            elif y != ny - 1:
                grid[ny - 1][x].value = grid[y][x].value
                grid[y][x].value = None
                changed = True
    if changed: grid = spawnTile(grid)
    return grid
    
def moveLeft(grid):
    changed = False
    done = [[False for x in range(4)] for y in range(4)]
    for x in range(1, 4):
        for y in range(4):
            if done[y][x] or not grid[y][x].value: continue
            nx = x - 1
            while nx >= 0 and not grid[y][nx].value: nx -= 1
            if nx >= 0 and grid[y][x].value == grid[y][nx].value:
                grid[y][nx].value *= 2
                done[y][nx] = True
                grid[y][x].value = None
                changed = True
            elif x != nx + 1:
                grid[y][nx + 1].value = grid[y][x].value
                grid[y][x].value = None
                changed = True
    if changed: grid = spawnTile(grid)
    return grid

def moveRight(grid):
    changed = False
    done = [[False for x in range(4)] for y in range(4)]
    for x in range(2, -1, -1):
        for y in range(4):
            if done[y][x] or not grid[y][x].value: continue
            nx = x + 1
            while nx < 4 and not grid[y][nx].value: nx += 1
            if nx < 4 and grid[y][x].value == grid[y][nx].value:
                grid[y][nx].value *= 2
                done[y][nx] = True
                grid[y][x].value = None
                changed = True
            elif x != nx - 1:
                grid[y][nx - 1].value = grid[y][x].value
                grid[y][x].value = None
                changed = True
    if changed: grid = spawnTile(grid)
    return grid

def spawnTile(grid):
    new = randint(0, 15)
    while grid[new // 4][new % 4].value: new = randint(0, 15)
    grid[new // 4][new % 4].value = 2 if randint(0, 99) < 90 else 4
    return grid

class Tile:
    value = None
    x = None
    y = None
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value
    def draw(self):
        roundedRect((screen.get_width() - 470) // 2 + 14 + 114 * x, (screen.get_height() - 470) // 2 + 14 + 114 * y, 100, 100, 6, 'empty' if not self.value else str(self.value) if self.value <= 2048 else 'super')
        if self.value:
            if self.value < 128:
                text = font55.render(str(self.value), True, colors['darktext'] if self.value < 8 else colors['lighttext'])
            elif self.value < 1024:
                text = font45.render(str(self.value), True, colors['darktext'] if self.value < 8 else colors['lighttext'])
            elif self.value <= 2048:
                text = font35.render(str(self.value), True, colors['darktext'] if self.value < 8 else colors['lighttext'])
            else:
                text = font30.render(str(self.value), True, colors['darktext'] if self.value < 8 else colors['lighttext'])
            screen.blit(text, text.get_rect(center = ((screen.get_width() - 470) // 2 + 114 * x + 64, (screen.get_height() - 470) // 2 + 114 * y + 64)))

grid = [[Tile(x, y, None) for x in range(4)] for y in range(4)]

s1 = randint(0, 15)
s2 = randint(0, 15)
while s2 == s1: s2 = randint(0, 16)
grid[s1 // 4][s1 % 4].value = 2 if randint(0, 99) < 90 else 4
grid[s2 // 4][s2 % 4].value = 2 if randint(0, 99) < 90 else 4

while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: moveLeft(grid)
            elif event.key == pygame.K_RIGHT: moveRight(grid)
            elif event.key == pygame.K_UP: grid = moveUp(grid)
            elif event.key == pygame.K_DOWN: moveDown(grid)

    screen.fill(colors['background'])

    roundedRect((screen.get_width() - 470) // 2, (screen.get_height() - 470) // 2, 470, 470, 6, 'game')
    for y in range(4):
        for x in range(4):
            grid[y][x].draw()

    pygame.display.flip()

