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

        self.SCRX = self.player_x
        self.SCRY = self.player_y
        self.CAMX = self.player_x
        self.CAMY = self.player_y
        self.zoom = 1

        self.ground_positions = []
        self.ground_positions_rel = []
        self.ground_textures_to_render = []

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

    def check_collision(self, ground_texture, player_pos, ground_pos, type):
        px, py = player_pos
        gx, gy = ground_pos

        gmask = pygame.mask.from_surface(ground_texture)
        pmask = pygame.mask.from_surface(self.sprites[f"playerh {type}"])

        # goverlap = gmask.overlap_mask(pmask, (px-gx, py-gy))
        goverlap_showcase = pmask.overlap_mask(gmask, (gx-px, gy-py)) 
        goverlap = pmask.overlap(gmask, (gx-px, gy-py))


        if goverlap != None:
            if type == "right":
                if self.player_xs > 0:
                    self.player_xs = 0
            elif type == "left":
                if self.player_xs < 0:
                    self.player_xs = 0
            elif type == "top":
                if self.player_ys > 0:
                    self.player_ys = 0
            elif type == "bottom":
                if self.player_ys < 0:
                    self.player_ys = 0


        govtoprint = goverlap_showcase.to_surface(setcolor=(255, 255, 255, 255), unsetcolor=(0, 0, 0, 255))
        self.screen.blit(govtoprint, (0+(type=="y")*100, 0))
        

        print(goverlap)
        


    def player_move(self):
        keydir = 0
        if self.key_held[pygame.K_LEFT] == True:
            keydir -= 1
        if self.key_held[pygame.K_RIGHT] == True:
            keydir += 1
        self.player_xs += keydir
        self.player_xs *= 0.85
 
        self.player_ys = 0
        if self.key_held[pygame.K_UP] == True:
            self.player_ys -= 5
        if self.key_held[pygame.K_DOWN] == True:
            self.player_ys += 5



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




            # move and collide
            self.sprites["player"] = pygame.transform.scale(self.sprites["player"], (8*factor, 8*factor))
            self.player_move()

            self.SCRX += self.player_xs
            self.SCRY += self.player_ys

            # px = self.SCRX-self.player_x+320
            # py = self.SCRY-self.player_y+180
            # self.screen.blit(self.sprites["player"], (px, py))

            x = 128-self.SCRX
            y = 72-self.SCRY
            # self.screen.blit(self.sprites["ground0"], (x, y))

            # check right collision
            px = self.SCRX-self.player_x+320+  self.sprites["player"].get_width() + self.player_xs
            py = self.SCRY-self.player_y+180+  self.player_ys

            self.check_collision(self.sprites["ground0"], (px, py), (x, y), "right")
            
            # check left collision
            px = self.SCRX-self.player_x+320-  self.sprites["playerh left"].get_width() + self.player_xs
            py = self.SCRY-self.player_y+180+  self.player_ys

            self.check_collision(self.sprites["ground0"], (px, py), (x, y), "left")
        
            # check bottom collision
            px = self.SCRX-self.player_x+320+ self.player_xs
            py = self.SCRY-self.player_y+180+  self.sprites["player"].get_height() + self.player_ys

            self.check_collision(self.sprites["ground0"], (px, py), (x, y), "bottom")

            # check top collision
            px = self.SCRX-self.player_x+320+ self.player_xs
            py = self.SCRY-self.player_y+180-  self.sprites["playerh top"].get_height() + self.player_ys

            self.check_collision(self.sprites["ground0"], (px, py), (x, y), "top")




            # update pos and render
            self.player_x += self.player_xs
            self.player_y += self.player_ys
            self.SCRX = self.player_x
            self.SCRY = self.player_y
            px = self.SCRX-self.player_x+320
            py = self.SCRY-self.player_y+180

            self.screen.blit(self.sprites["player"], (px, py)) # render with cam var ofc
            self.screen.blit(self.sprites["ground0"], (x, y))


            self.CAMX += (self.player_x-self.CAMX)/3
            self.CAMY += (self.player_y-self.CAMY)/3

            if self.zoom != self.targ_zoom:
                # zoom
                self.zoom += (self.targ_zoom - self.zoom)/3


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
            pygame.display.update()

Game().game_run()




# was working on collision with all grounds 