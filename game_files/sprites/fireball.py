import os
import pygame
from .projectile_base import Projectile
from ..utils.spritesheet import SpriteSheet

class Fireball(Projectile):
    def __init__(self, image):
        """
        Create fireball transformed based on direction
        """
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()

    def set_color(self, purple:bool=False, blue:bool=False, red:bool=False):
        """
        Set the color the fireball should be
        """
        if purple:
            self.color = purple
        elif blue:
            self.color = blue
        elif red:
            self.color = red
