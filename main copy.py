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
        # self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.screen = self.assets.screen
        # pygame.display.toggle_fullscreen()
        self.clock = pygame.time.Clock()
        self.run = True

        self.player_x = 60
        self.player_y = 60
        self.player_xs = 0
        self.player_ys = 0

        self.CAMX = 0
        self.CAMY = 0
        self.zoom = 1

        self.ground_positions = []
        self.ground_positions_rel = []
        self.ground_textures_to_render = []

        # y = 72
        # for i in range(3):
        #     x = -128
        #     for n in range(3):
        #         self.ground_positions.append((x*2,y*2))
        #         self.ground_positions_rel.append((x*2,y*2))
        #         x += 128
        #     y -= 72

        
        # y = -72
        # for i in range(3):
        #     x = -128
        #     for n in range(3):
        #         self.ground_positions.append((x,y))
        #         self.ground_positions_rel.append((x,y))
        #         x += 128
        #     y += 72

        y = -72
        for i in range(3):
            x = -128
            for n in range(3):
                self.ground_positions.append((x,y))
                self.ground_positions_rel.append((x,y))
                self.ground_textures_to_render.append("")
                x += 128
            y += 72

    def load_zoomed(self, img):
        self.sprites[img] = pygame.transform.scale(self.sprites[img], (128*self.zoom, 72*self.zoom))
        return self.sprites[img]

    def check_collision(self, i, x, y, ground_texture):
        player_mask = pygame.mask.from_surface(self.sprites["player"])

        # overlap = player_mask.overlap(ground_mask, ((self.player_xs), (self.player_ys)))
        ground_mask = pygame.mask.from_surface(ground_texture)
        x = self.ground_positions_rel[i][0]*self.zoom-self.SCRX
        y = self.ground_positions_rel[i][1]*self.zoom-self.SCRY
        overlap = ground_mask.overlap(player_mask, (x, y))
        # print(i, overlap)

        ground_texture = ground_mask.to_surface(setcolor=(255, 255, 255, 255), unsetcolor=(0, 0, 0, 255))
        player_texture = player_mask.to_surface(setcolor=(255, 255, 255, 255), unsetcolor=(0, 0, 0, 255))
        self.screen.blit(ground_texture, (x, y))
        self.screen.blit(player_texture, (x, y))
            

        # player_mask.invert()
        # ground_mask.invert()

        player_mask = player_mask.to_surface(setcolor=(255, 255, 255, 255), unsetcolor=(0, 0, 0, 255))
        ground_mask = ground_mask.to_surface(setcolor=(255, 255, 255, 255), unsetcolor=(0, 0, 0, 255))

        # self.screen.blit(ground_mask, (0, 0))
        # self.screen.blit(player_mask, (self.player_x, self.player_y))


        # overlap = ground_mask.overlap(player_mask, ((self.player_xs), (self.player_ys)))
        if overlap == None:
            print(i, None)
            pass
        else:
            print(i, overlap)
            pass
        pass

    def player_move(self):
        keydir = 0
        if self.key_held[pygame.K_LEFT] == True:
            keydir -= 1
        if self.key_held[pygame.K_RIGHT] == True:
            keydir += 1
        self.player_xs += keydir
        self.player_xs *= 0.85
 
        if self.key_held[pygame.K_UP] == True:
            self.player_y -= 5
        if self.key_held[pygame.K_DOWN] == True:
            self.player_y += 5


        self.player_x += self.player_xs
        self.player_y += self.player_ys

    def game_run(self):
        while self.run:

            self.clock.tick(self.fps_cap)
            self.key = pygame.key.get_just_pressed()
            self.key_held = pygame.key.get_pressed()
            self.screen.fill((55,55,55))

            factor = 1
            factor = (1/6)*10
            factor = 2
            self.targ_zoom = 2            
            self.targ_zoom = 1            


            self.sprites["player"] = pygame.transform.scale(self.sprites["player"], (8*factor, 8*factor))
            # self.player_x, self.player_y = pygame.mouse.get_pos()
            


            self.player_move()

            self.SCRX = self.player_x
            self.SCRY = self.player_y
            self.CAMX += (self.player_x-self.CAMX)/3
            self.CAMY += (self.player_y-self.CAMY)/3

            # print(self.SCRX, self.SCRY)

            # self.screen.blit(self.sprites["ground0"], (0, 0))
            
            # self.screen.blit(self.sprites["player"], (self.SCRX-self.player_x+320, self.SCRY-self.player_y+180))
            # self.screen.blit(self.sprites["player"], (self.SCRX-self.player_x+320, self.SCRY-self.player_y+180))
            self.screen.blit(self.sprites["player"], (self.SCRX-self.player_x, self.SCRY-self.player_y))

            
            for i in range(1):
                i = 8
                # replace the i in self.sprites[f"ground{i}"] with actual texture number
                x = self.ground_positions_rel[i][0]
                y = self.ground_positions_rel[i][1]

                x = self.ground_positions_rel[i][0]*self.zoom-self.SCRX
                y = self.ground_positions_rel[i][1]*self.zoom-self.SCRY

                # self.ground_positions[i] = (-(self.SCRX-x*factor-(128*factor)/2), -(self.SCRY-y*factor-(72*factor)/2))
                self.ground_positions[i] = (x, y)

                
                self.check_collision(i, x, y, self.sprites[f"ground{i}"])

                # update zooming on ground texture (so if your texture actually represents another one than before, it would update here, insert the ground)
                # there are 9 ground displays
                self.ground_textures_to_render[i] = i
            
                # self.screen.blit(self.sprites[f"ground{i}"], self.ground_positions[i])
                
                # print(i, self.ground_positions[i])  -((128*factor))   (72*factor)/2)

            if self.zoom != self.targ_zoom:
                # zoom
                self.zoom += (self.targ_zoom - self.zoom)/3
                for i in range(len(self.ground_textures_to_render)):
                    # if not initial
                    if self.ground_textures_to_render[i] != "":
                        self.sprites[f"ground{i}"] = self.load_zoomed(f"ground{i}")



            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
            pygame.display.update()

Game().game_run()




# was working on collision with all grounds 