import pygame

class Assets:
    def __init__(self):
        self.sprites = {}
        to_load = [ # Load Images from the Images folder
            ("player", ""),
            ("ground", "")
        ]  # names with special second (or more) item get special treatment in loading (like loading both 0 and 1 name-ending variants)

        for i in range (len(to_load)):
            image_path = "src/sprites/"
            if to_load[i][1] == "add_n":
                # add_n special (starts at 1):
                image_path += f"{to_load[i][0]}"
                for j in range (to_load[i][2]):
                    self.sprites[to_load[i][0] + str(j+1)] = pygame.image.load(image_path + str(j+1) + ".png")
            else:
                image_path += f"{to_load[i][0]}.png"
                if to_load[i][1] == "keep_transparency":
                    # keep_transparency:
                    self.sprites[to_load[i][0]] = pygame.image.load(image_path)
                else:
                    # standard load:
                    self.sprites[to_load[i][0]] = pygame.image.load(image_path)