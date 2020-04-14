import os, sys, random, time
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame, ai
from threading import Thread
from game import Game

class Main:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('2048 AI')
        self.size = width, height = 800, 600
        self.screen = pygame.display.set_mode(self.size)
        self.game = Game(self.screen)    
        self.aiEnabled = False
        self.aiThread = None
        self.gameover = False
        self.loop(self.screen)

    def processAI(self):
        while True:
            if not self.aiEnabled:
                break
            next = ai.calculateNextMove(self.game.grid)
            if next == 0: self.game.moveUp()
            elif next == 1: self.game.moveDown()
            elif next == 2: self.game.moveLeft()
            elif next == 3: self.game.moveRight()
            # sleep(0.1)
            break

    def toggleAI(self):
        self.aiEnabled = not self.aiEnabled
        if self.aiEnabled:
            self.aiThread = Thread(target=self.processAI)
            self.aiThread.daemon = True
            self.aiThread.start()
        else:
            self.aiThread = None

    def processEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            elif event.type == pygame.KEYDOWN and not self.gameover:
                if event.key == pygame.K_LEFT and not self.aiEnabled: self.game.moveLeft()
                elif event.key == pygame.K_RIGHT and not self.aiEnabled: self.game.moveRight()
                elif event.key == pygame.K_UP and not self.aiEnabled: self.game.moveUp()
                elif event.key == pygame.K_DOWN and not self.aiEnabled: self.game.moveDown()
                elif event.key == pygame.K_SPACE: self.toggleAI()

    def loop(self, screen):
        clock = pygame.time.Clock()
        while True:    
            clock.tick(60)
            self.processEvents()
            self.gameover = self.game.isGameOver()
            screen.fill(self.game.colors['background'])
            self.game.iterate()
            if self.aiEnabled:
                text = self.game.font35.render('AI Mode', True, self.game.colors['2048'])
                screen.blit(text, text.get_rect(center=(screen.get_width() // 2, screen.get_height() - 35)))
            scoreText = self.game.font30.render('Score: %d' % self.game.score, True, self.game.colors['darktext'])
            screen.blit(scoreText, scoreText.get_rect(center=(screen.get_width() // 2, 35)))
            if self.gameover:
                if self.aiEnabled: self.toggleAI()
                self.game.roundedRect((self.screen.get_width() - 470) // 2, (self.screen.get_height() - 470) // 2, 470, 470, 6, '2048')
                text = self.game.font55.render('Game Over', True, self.game.colors['darktext'])
                screen.blit(text, text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2)))

            pygame.display.flip()

if __name__ == "__main__":
    Main()