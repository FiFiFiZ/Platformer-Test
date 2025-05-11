import pygame
from math import *
import sys
sys.path.append("./bin")

from assets import Assets # type: ignore

class Game:
    def __init__(self):
        pygame.init()

        self.assets = Assets()
        self.sprites = self.assets.sprites


        self.fps_cap = 60
        self.SCREEN_WIDTH = pygame.display.Info().current_w
        self.SCREEN_HEIGHT = pygame.display.Info().current_h
        self.SCREEN_WIDTH = 640
        self.SCREEN_HEIGHT = 360
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        # pygame.display.toggle_fullscreen()
        self.clock = pygame.time.Clock()
        self.run = True

    def game_run(self):
        while self.run:

            self.clock.tick(self.fps_cap)
            self.key = pygame.key.get_just_pressed()
            self.key_held = pygame.key.get_pressed()
            self.screen.fill((255,255,255))

            placeholder_player = pygame.transform.scale_by(self.sprites["player"], 5)
            placeholder_ground = pygame.transform.scale_by(self.sprites["ground"], 5)
            self.screen.blit(placeholder_ground, (0, 0))
            self.screen.blit(placeholder_player, (60, 60))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
            pygame.display.update()

Game().game_run()