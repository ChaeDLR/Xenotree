import os
import pygame
from pygame.sprite import Sprite
from ..utils.spritesheet import SpriteSheet

class Fireball(Sprite):
    def __init__(self, start_x_y: tuple, dir_x_y: tuple):
        """
        Create fireball transformed based on direction
        """
        super().__init__()

        self.__load_fireball_imgs()

    def __fireball_coords(self) -> dict:
        coords = {"idle_purp": [
            (2, 1, 4, 7),
            (26, 3, 3, 5)
        ],
        "idle_blue": [
            (0, 0, 0, 0),
            (0, 0, 0, 0)
        ],
        "idle_red": [
            (0, 0, 0, 0),
            (0, 0, 0, 0)
        ],
        "purp_fire": [
            (8, 4, 7, 4),
            (18, 5, 5, 3)
        ],
        "blue_fire": [
            (0, 0, 0, 0),
            (0, 0, 0, 0)
        ],
        "red_fire": [
            (0, 0, 0, 0),
            (0, 0, 0, 0)
        ]}
        return coords

    def __load_fireball_imgs(self):
        """
        Load fireball images from spritesheet
        """
        path = os.path.dirname(__file__)
        fireballs_path = os.path.join(
            path, "sprite_assets/player_assets/fireballs.png"
        )
        ss_tool = SpriteSheet(fireballs_path)
        fireball_ss_coords: dict = self.__fireball_coords()
        p_colorkey = (0, 0, 0)

        def idle_purple_fireballs():
            #### idle images ####
            self.purp_fb_idle_imgs = []
            for coord in fireball_ss_coords["idle_purp"]:
                image = ss_tool.image_at(coord, p_colorkey)
                self.purp_fb_idle_imgs.append(image)

        def fire_purple_fireballs():
            self.purp_fb_fire_imgs = []
            for coord in fireball_ss_coords["purp_fire"]:
                image = ss_tool.image_at(coord, p_colorkey)
                self.purp_fb_fire_imgs.append(image)
        
        #### Lookz like purple is good to go
        idle_purple_fireballs()
        fire_purple_fireballs()
        #self.image = self.red_fb_idle_imgs[1]
        #self.image = self.purp_fb_fire_imgs[1]
        self.rect = self.image.get_rect()
