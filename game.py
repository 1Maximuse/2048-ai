from random import randint
import pygame
import pygame.gfxdraw
from pygame import Rect

class Game:
    score = 0
    animSpeed = 5

    def __init__(self, screen):
        self.grid = [[Tile(x, y, None, self) for x in range(4)] for y in range(4)]
        self.spawn_first_tiles()
        self.screen = screen
        self.font55 = pygame.font.Font('font.ttf', 55)
        self.font45 = pygame.font.Font('font.ttf', 45)
        self.font35 = pygame.font.Font('font.ttf', 35)
        self.font30 = pygame.font.Font('font.ttf', 30)
        self.font20 = pygame.font.Font('font.ttf', 20)
        self.font15 = pygame.font.Font('font.ttf', 15)
        self.colors = {
            'background': (250, 248, 239),
            'game': (187, 173, 160),
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

    def is_game_over(self):
        for y in range(4):
            for x in range(4):
                if not self.grid[y][x].value:
                    return False
        for y in range(4):
            for x in range(4):
                if y < 3 and self.grid[y][x].value == self.grid[y+1][x].value:
                    return False
                if x < 3 and self.grid[y][x].value == self.grid[y][x+1].value:
                    return False
        return True

    def rounded_rect(self, x, y, width, height, radius, color):
        pygame.draw.rect(self.screen, self.colors[color], Rect(x, y + radius, width, height - radius - radius))
        pygame.draw.rect(self.screen, self.colors[color], Rect(x + radius, y, width - radius - radius, height))
        pygame.gfxdraw.filled_circle(self.screen, x + radius, y + radius, radius, self.colors[color])
        pygame.gfxdraw.aacircle(self.screen, x + radius, y + radius, radius, self.colors[color])
        pygame.gfxdraw.filled_circle(self.screen, x + radius, y + height - radius - 1, radius, self.colors[color])
        pygame.gfxdraw.aacircle(self.screen, x + radius, y + height - radius - 1, radius, self.colors[color])
        pygame.gfxdraw.filled_circle(self.screen, x + width - radius - 1, y + height - radius - 1, radius, self.colors[color])
        pygame.gfxdraw.aacircle(self.screen, x + width - radius - 1, y + height - radius - 1, radius, self.colors[color])
        pygame.gfxdraw.filled_circle(self.screen, x + width - radius - 1, y + radius, radius, self.colors[color])
        pygame.gfxdraw.aacircle(self.screen, x + width - radius - 1, y + radius, radius, self.colors[color])

    def move_up(self):
        new_dir = [[-1 for x in range(4)] for y in range(4)]
        changed = False
        done = [[False for x in range(4)] for y in range(4)]
        for y in range(1, 4):
            for x in range(4):
                if not self.grid[y][x].value:
                    continue
                nexty = y - 1
                while nexty >= 0 and not self.grid[nexty][x].value:
                    nexty -= 1
                if nexty >= 0 and not done[nexty][x] and self.grid[y][x].value == self.grid[nexty][x].value:
                    self.grid[nexty][x].value *= 2
                    self.score += self.grid[nexty][x].value
                    done[nexty][x] = True
                    self.grid[y][x].value = None
                    changed = True
                    new_dir[nexty][x] = y * 4 + x
                elif y != nexty + 1:
                    self.grid[nexty + 1][x].value = self.grid[y][x].value
                    self.grid[y][x].value = None
                    changed = True
                    new_dir[nexty + 1][x] = y * 4 + x
        if changed:
            self.reset_timer()
            for y in range(4):
                for x in range(4):
                    if new_dir[y][x] != -1:
                        self.grid[y][x].moving = new_dir[y][x]
                        self.grid[y][x].timer = self.animSpeed
            self.spawn_tile()

    def move_down(self):
        new_dir = [[-1 for x in range(4)] for y in range(4)]
        changed = False
        done = [[False for x in range(4)] for y in range(4)]
        for y in range(2, -1, -1):
            for x in range(4):
                if not self.grid[y][x].value:
                    continue
                nexty = y + 1
                while nexty < 4 and not self.grid[nexty][x].value:
                    nexty += 1
                if nexty < 4 and not done[nexty][x] and self.grid[y][x].value == self.grid[nexty][x].value:
                    self.grid[nexty][x].value *= 2
                    self.score += self.grid[nexty][x].value
                    done[nexty][x] = True
                    self.grid[y][x].value = None
                    changed = True
                    new_dir[nexty][x] = y * 4 + x
                elif y != nexty - 1:
                    self.grid[nexty - 1][x].value = self.grid[y][x].value
                    self.grid[y][x].value = None
                    changed = True
                    new_dir[nexty - 1][x] = y * 4 + x
        if changed:
            self.reset_timer()
            for y in range(4):
                for x in range(4):
                    if new_dir[y][x] != -1:
                        self.grid[y][x].moving = new_dir[y][x]
                        self.grid[y][x].timer = self.animSpeed
            self.spawn_tile()

    def move_left(self):
        new_dir = [[-1 for x in range(4)] for y in range(4)]
        changed = False
        done = [[False for x in range(4)] for y in range(4)]
        for x in range(1, 4):
            for y in range(4):
                if not self.grid[y][x].value:
                    continue
                nextx = x - 1
                while nextx >= 0 and not self.grid[y][nextx].value:
                    nextx -= 1
                if nextx >= 0 and not done[y][nextx] and self.grid[y][x].value == self.grid[y][nextx].value:
                    self.grid[y][nextx].value *= 2
                    self.score += self.grid[y][nextx].value
                    done[y][nextx] = True
                    self.grid[y][x].value = None
                    changed = True
                    new_dir[y][nextx] = y * 4 + x
                elif x != nextx + 1:
                    self.grid[y][nextx + 1].value = self.grid[y][x].value
                    self.grid[y][x].value = None
                    changed = True
                    new_dir[y][nextx + 1] = y * 4 + x
        if changed:
            self.reset_timer()
            for y in range(4):
                for x in range(4):
                    if new_dir[y][x] != -1:
                        self.grid[y][x].moving = new_dir[y][x]
                        self.grid[y][x].timer = self.animSpeed
            self.spawn_tile()

    def move_right(self):
        new_dir = [[-1 for x in range(4)] for y in range(4)]
        changed = False
        done = [[False for x in range(4)] for y in range(4)]
        for x in range(2, -1, -1):
            for y in range(4):
                if not self.grid[y][x].value:
                    continue
                nextx = x + 1
                while nextx < 4 and not self.grid[y][nextx].value:
                    nextx += 1
                if nextx < 4 and not done[y][nextx] and self.grid[y][x].value == self.grid[y][nextx].value:
                    self.grid[y][nextx].value *= 2
                    self.score += self.grid[y][nextx].value
                    done[y][nextx] = True
                    self.grid[y][x].value = None
                    changed = True
                    new_dir[y][nextx] = y * 4 + x
                elif x != nextx - 1:
                    self.grid[y][nextx - 1].value = self.grid[y][x].value
                    self.grid[y][x].value = None
                    changed = True
                    new_dir[y][nextx - 1] = y * 4 + x
        if changed:
            self.reset_timer()
            for y in range(4):
                for x in range(4):
                    if new_dir[y][x] != -1:
                        self.grid[y][x].moving = new_dir[y][x]
                        self.grid[y][x].timer = self.animSpeed
            self.spawn_tile()

    def spawn_tile(self):
        new = randint(0, 15)
        while self.grid[new // 4][new % 4].value:
            new = randint(0, 15)
        self.grid[new // 4][new % 4].value = 2 if randint(0, 99) < 90 else 4
        self.grid[new // 4][new % 4].new = self.animSpeed + self.animSpeed

    def reset_timer(self):
        for y in range(4):
            for x in range(4):
                self.grid[y][x].moving = -1
                self.grid[y][x].timer = 0
                self.grid[y][x].new = 0

    def spawn_first_tiles(self):
        pos1 = randint(0, 15)
        pos2 = randint(0, 15)
        while pos2 == pos1:
            pos2 = randint(0, 15)
        self.grid[pos1 // 4][pos1 % 4].value = 2 if randint(0, 99) < 90 else 4
        self.grid[pos2 // 4][pos2 % 4].value = 2 if randint(0, 99) < 90 else 4
        self.grid[pos1 // 4][pos1 % 4].new = self.animSpeed + self.animSpeed
        self.grid[pos2 // 4][pos2 % 4].new = self.animSpeed + self.animSpeed

    def iterate(self):
        for y in range(4):
            for x in range(4):
                if self.grid[y][x].new != 0:
                    self.grid[y][x].new -= 1
                if self.grid[y][x].moving != -1:
                    self.grid[y][x].timer -= 1
                    if self.grid[y][x].timer == 0:
                        self.grid[y][x].moving = -1

        self.rounded_rect((self.screen.get_width() - 470) // 2, (self.screen.get_height() - 470) // 2, 470, 470, 6, 'game')
        for y in range(4):
            for x in range(4):
                if self.grid[y][x].moving == -1:
                    self.grid[y][x].draw()
        for y in range(4):
            for x in range(4):
                if self.grid[y][x].moving != -1:
                    self.grid[y][x].draw()
class Tile:
    moving = -1
    timer = 0
    new = 0
    def __init__(self, x, y, value, game):
        self.x = x
        self.y = y
        self.value = value
        self.game = game
    def draw(self):
        offsetx = 0
        offsety = 0
        if self.moving != -1:
            movey = self.moving // 4
            movex = self.moving % 4
            if self.y == movey:
                movex -= self.x
                offsetx = (movex * 114 - 14) * self.timer // self.game.animSpeed
            elif self.x == movex:
                movey -= self.y
                offsety = (movey * 114 - 14) * self.timer // self.game.animSpeed

        size = 100 * max(self.game.animSpeed - self.new, 0) // self.game.animSpeed
        self.game.rounded_rect((self.game.screen.get_width() - 470) // 2 + 14 + 114 * self.x, (self.game.screen.get_height() - 470) // 2 + 14 + 114 * self.y, 100, 100, 6, 'empty')
        if size > 0:
            self.game.rounded_rect((self.game.screen.get_width() - 470) // 2 + 14 + 114 * self.x + offsetx + 50 - size // 2, (self.game.screen.get_height() - 470) // 2 + 14 + 114 * self.y + offsety + 50 - size // 2, size, size, 6, 'empty' if not self.value else str(self.value) if self.value <= 2048 else 'super')
        if self.value and size > 0:
            if self.value < 128:
                text = self.game.font55.render(str(self.value), True, self.game.colors['darktext'] if self.value < 8 else self.game.colors['lighttext'])
            elif self.value < 1024:
                text = self.game.font45.render(str(self.value), True, self.game.colors['darktext'] if self.value < 8 else self.game.colors['lighttext'])
            elif self.value <= 2048:
                text = self.game.font35.render(str(self.value), True, self.game.colors['darktext'] if self.value < 8 else self.game.colors['lighttext'])
            else:
                text = self.game.font30.render(str(self.value), True, self.game.colors['darktext'] if self.value < 8 else self.game.colors['lighttext'])
            self.game.screen.blit(text, text.get_rect(center=((self.game.screen.get_width() - 470) // 2 + 114 * self.x + 64 + offsetx, (self.game.screen.get_height() - 470) // 2 + 114 * self.y + 64 + offsety)))
