import pygame

class Assets:
    def __init__(self):
        self.sprites = {}
        to_load = [ # Load Images from the Images folder
            ("player", ""),
            ("ground", "add_n", 9),
            ("playerh ", "add_list", ["bottom", "top", "right", "left"])
        ]  # names with special second (or more) item get special treatment in loading (like loading both 0 and 1 name-ending variants)

        self.SCREEN_WIDTH = pygame.display.Info().current_w
        self.SCREEN_HEIGHT = pygame.display.Info().current_h
        self.SCREEN_WIDTH = 640
        self.SCREEN_HEIGHT = 360
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        for i in range (len(to_load)):
            image_path = "src/sprites/"
            if to_load[i][1] == "add_n":
                # add_n special (starts at 1):
                image_path += f"{to_load[i][0]}"
                self.add_n(to_load[i], image_path)

            elif to_load[i][1] == "add_list":
                # concatenate string with every list element
                image_path += f"{to_load[i][0]}"
                self.add_list(to_load[i], image_path)
            else:
                image_path += f"{to_load[i][0]}.png"
                if to_load[i][1] == "keep_transparency":
                    # keep_transparency:
                    self.sprites[to_load[i][0]] = pygame.image.load(image_path).convert()
                else:
                    # standard load:
                    self.sprites[to_load[i][0]] = pygame.image.load(image_path)

                    # self.sprites[to_load[i]].colorkey((153, 102, 255))

    def add_n(self, to_load, image_path):
        for j in range (to_load[2]):
            self.sprites[to_load[0] + str(j)] = pygame.image.load(image_path + str(j) + ".png")

    def add_list(self, to_load, image_path):
        for items in to_load[2]:
            self.sprites[to_load[0] + str(items)] = pygame.image.load(image_path + str(items) + ".png")

