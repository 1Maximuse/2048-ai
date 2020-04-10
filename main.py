import os, sys, random, pygame
from game import *
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

def initGame():
    pygame.init()
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('2048 AI')
    initConstants(screen)
    return screen

def processEvents(grid):
    for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT: moveLeft(grid)
                elif event.key == pygame.K_RIGHT: moveRight(grid)
                elif event.key == pygame.K_UP: grid = moveUp(grid)
                elif event.key == pygame.K_DOWN: moveDown(grid)

def loop(grid, screen):
    clock = pygame.time.Clock()
    while True:    
        clock.tick(60)
        processEvents(grid)
        gameLoop(grid, screen)

def main():
    screen = initGame()
    grid = [[Tile(x, y, None) for x in range(4)] for y in range(4)]
    grid = spawnFirstTiles(grid)
    loop(grid, screen)

if __name__ == "__main__":
    main()