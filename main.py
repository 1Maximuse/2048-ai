import os, sys, random, pygame
import game
from game import Tile
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

ai = False

def toggleAI():
    global ai
    ai = not ai

def initGame():
    pygame.init()
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('2048 AI')
    game.initConstants(screen)
    return screen

def processEvents(grid):
    for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and not ai: game.moveLeft(grid)
                elif event.key == pygame.K_RIGHT and not ai: game.moveRight(grid)
                elif event.key == pygame.K_UP and not ai: grid = game.moveUp(grid)
                elif event.key == pygame.K_DOWN and not ai: game.moveDown(grid)
                elif event.key == pygame.K_SPACE: toggleAI()

def loop(grid, screen):
    clock = pygame.time.Clock()
    while True:    
        clock.tick(60)
        processEvents(grid)
        screen.fill(game.colors['background'])
        game.gameLoop(grid, screen)
        if ai:
            text = game.font35.render('AI Mode', True, game.colors['2048'])
            screen.blit(text, text.get_rect(center = (screen.get_width() // 2, screen.get_height() - 35)))
        pygame.display.flip()

def main():
    screen = initGame()
    grid = [[Tile(x, y, None) for x in range(4)] for y in range(4)]
    grid = game.spawnFirstTiles(grid)
    loop(grid, screen)

if __name__ == "__main__":
    main()