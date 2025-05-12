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

        self.player_x = 60
        self.player_y = 60
        self.player_xs = 0
        self.player_ys = 0

        self.ground_positions = []
        y = -72
        for i in range(3):
            x = -128
            for n in range(3):
                self.ground_positions.append((x,y))
                x += 128
            y -= 72

    def check_collision(self):
        player_mask = pygame.mask.from_surface(self.sprites["player"])
        ground_mask = pygame.mask.from_surface(self.sprites["ground0"])

        for i in range(9):
            # overlap = player_mask.overlap(ground_mask, ((self.player_xs), (self.player_ys)))
            overlap = player_mask.overlap(ground_mask, ((self.player_xs), (self.player_ys)))

        # player_mask.invert()
        # ground_mask.invert()

        player_mask = player_mask.to_surface(setcolor=(255, 255, 255, 255), unsetcolor=(0, 0, 0, 255))
        ground_mask = ground_mask.to_surface(setcolor=(255, 255, 255, 255), unsetcolor=(0, 0, 0, 255))

        # self.screen.blit(ground_mask, (0, 0))
        # self.screen.blit(player_mask, (self.player_x, self.player_y))


        # overlap = ground_mask.overlap(player_mask, ((self.player_xs), (self.player_ys)))
        if overlap == None:
            pass
        else:
            print(overlap)

        pass

    def player_move(self):
        keydir = 0
        if self.key_held[pygame.K_LEFT] == True:
            keydir -= 1
        if self.key_held[pygame.K_RIGHT] == True:
            keydir += 1
        self.player_xs += keydir
        self.player_xs *= 0.98

        self.check_collision()

        self.player_x += self.player_xs
        self.player_y += self.player_ys

    def game_run(self):
        while self.run:

            self.clock.tick(self.fps_cap)
            self.key = pygame.key.get_just_pressed()
            self.key_held = pygame.key.get_pressed()
            self.screen.fill((255,255,255))

            factor = 1
            self.sprites["player"] = pygame.transform.scale(self.sprites["player"], (8*factor, 8*factor))
            self.sprites["ground0"] = pygame.transform.scale(self.sprites["ground0"], (128*factor, 72*factor))
            self.player_x, self.player_y = pygame.mouse.get_pos()

            self.player_move()
            self.check_collision()

            # self.screen.blit(self.sprites["ground0"], (0, 0))
            self.screen.blit(self.sprites["player"], (self.player_x, self.player_y))
            for i in range(9):
                self.screen.blit(self.sprites[f"ground{i}"], self.ground_positions[i])


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
            pygame.display.update()

Game().game_run()