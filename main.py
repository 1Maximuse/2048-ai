import sys
from threading import Lock, Thread
import pygame
from game import Game
import ai

class Main:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('2048 AI')
        self.size = (800, 600)
        self.screen = pygame.display.set_mode(self.size)
        self.game = Game(self.screen)
        self.ai_enabled = False
        self.ai_thread = None
        self.ai_next_move = -1
        self.lock = Lock()
        self.gameover = False
        self.loop(self.screen)

    def process_ai(self):
        while True:
            if not self.ai_enabled:
                break
            if self.ai_next_move != -1:
                continue
            next_move = ai.calculate_next_move(self.game.grid)
            self.lock.acquire()
            self.ai_next_move = next_move   
            self.lock.release()

    def toggle_ai(self):
        self.ai_enabled = not self.ai_enabled
        if self.ai_enabled:
            self.ai_thread = Thread(target=self.process_ai)
            self.ai_thread.daemon = True
            self.ai_thread.start()
        else:
            self.ai_thread = None

    def retry(self):
        self.game = Game(self.screen)
        self.ai_enabled = False
        self.ai_thread = None
        self.ai_next_move = -1
        self.lock = Lock()
        self.gameover = False
        self.loop(self.screen)

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN and not self.gameover:
                if event.key == pygame.K_LEFT and not self.ai_enabled:
                    self.game.move_left()
                elif event.key == pygame.K_RIGHT and not self.ai_enabled:
                    self.game.move_right()
                elif event.key == pygame.K_UP and not self.ai_enabled:
                    self.game.move_up()
                elif event.key == pygame.K_DOWN and not self.ai_enabled:
                    self.game.move_down()
                elif event.key == pygame.K_SPACE:
                    self.toggle_ai()
            elif event.type == pygame.KEYDOWN and self.gameover:
                if event.key == pygame.K_r:
                    self.retry()

    def loop(self, screen):
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            self.process_events()
            self.lock.acquire()
            if self.ai_enabled and self.ai_next_move != -1:
                if self.ai_next_move == 0:
                    self.game.move_up()
                elif self.ai_next_move == 1:
                    self.game.move_down()
                elif self.ai_next_move == 2:
                    self.game.move_left()
                elif self.ai_next_move == 3:
                    self.game.move_right()
                self.ai_next_move = -1
            self.lock.release()
            self.gameover = self.game.is_game_over()
            screen.fill(self.game.colors['background'])
            self.game.iterate()
            if self.ai_enabled:
                text = self.game.font35.render('AI Mode', True, self.game.colors['2048'])
                screen.blit(text, text.get_rect(center=(screen.get_width() // 2, screen.get_height() - 35)))
            score_text = self.game.font30.render('Score: %d' % self.game.score, True, self.game.colors['darktext'])
            screen.blit(score_text, score_text.get_rect(center=(screen.get_width() // 2, 35)))
            if self.gameover:
                if self.ai_enabled:
                    self.toggle_ai()
                self.game.rounded_rect((self.screen.get_width() - 470) // 2, (self.screen.get_height() - 470) // 2, 470, 470, 6, '2048')
                text = self.game.font55.render('Game Over', True, self.game.colors['darktext'])
                screen.blit(text, text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2)))
                text = self.game.font30.render('Press R to retry', True, self.game.colors['darktext'])
                screen.blit(text, text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 200)))

            pygame.display.flip()

if __name__ == "__main__":
    Main()
