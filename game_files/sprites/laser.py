import os
import pygame

from .projectile_base import Projectile

class Laser(Projectile):
    def __init__(self, start_x_y: tuple, dir_x_y: tuple):
        """
        Give the x_y position it should spawn at.
        """
        super().__init__()

        self.image = self.load_img()
        self.rect = self.image.get_rect()
        self.set_start(start_x_y, dir_x_y)
        self.x = self.rect.x
        self.y = self.rect.y

    def load_img(self):
        """
        Load the laser image
        """
        current_path = os.path.dirname(__file__)
        laser_img_path = os.path.join(
            current_path, "sprite_assets/laser.png"
            )
        return pygame.image.load(laser_img_path)
