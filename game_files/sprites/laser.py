import os
import pygame

from .projectile_base import Projectile

class Laser(Projectile):
    def __init__(self, image):
        """
        Get the laser img asset
        Set image and rect
        """
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
