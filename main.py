import os, sys, random, threading, time
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame, game, ai
from game import Tile

aiEnabled = False
aiThread = None
grid = None

def processAI():
    global aiEnabled, grid
    while True:
        if not aiEnabled:
            break
        next = ai.calculateNextMove(grid)
        if next == 0: grid = game.moveUp(grid)
        elif next == 1: grid = game.moveDown(grid)
        elif next == 2: grid = game.moveLeft(grid)
        elif next == 3: grid = game.moveRight(grid)
        # sleep(0.1)
        break

def toggleAI():
    global aiEnabled, aiThread
    aiEnabled = not aiEnabled
    if aiEnabled:
        aiThread = threading.Thread(target=processAI)
        aiThread.daemon = True
        aiThread.start()
    else:
        aiThread = None

def initGame():
    pygame.init()
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('2048 AI')
    game.initConstants(screen)
    return screen

def processEvents():
    global grid, aiEnabled
    for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and not aiEnabled: game.moveLeft(grid)
                elif event.key == pygame.K_RIGHT and not aiEnabled: game.moveRight(grid)
                elif event.key == pygame.K_UP and not aiEnabled: grid = game.moveUp(grid)
                elif event.key == pygame.K_DOWN and not aiEnabled: game.moveDown(grid)
                elif event.key == pygame.K_SPACE: toggleAI()

def loop(screen):
    global grid
    clock = pygame.time.Clock()
    while True:    
        clock.tick(60)
        processEvents()
        screen.fill(game.colors['background'])
        game.gameLoop(grid, screen)
        if aiEnabled:
            text = game.font35.render('AI Mode', True, game.colors['2048'])
            screen.blit(text, text.get_rect(center=(screen.get_width() // 2, screen.get_height() - 35)))
        pygame.display.flip()

def main():
    global grid
    screen = initGame()
    grid = [[Tile(x, y, None) for x in range(4)] for y in range(4)]
    grid = game.spawnFirstTiles(grid)
    loop(screen)

if __name__ == "__main__":
    main()