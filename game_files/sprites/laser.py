from pygame.sprite import Sprite
from pygame import Surface
import time
import pygame


class Laser(Sprite):
    def __init__(self, start_x_y: tuple, dir_x_y: tuple):
        """
        Give the x_y position it should spawn at.
        """
        super().__init__()

        self.image = Surface((12, 28))
        self.image.fill((250, 10, 10))
        self.rect = self.image.get_rect()
        # Set position
        self.rect.x, self.rect.y = start_x_y[0], start_x_y[1]
        self.start_coords = start_x_y
        self.firing_speed = 15
        self.directions = self.__set_directions(dir_x_y)
        self.x = self.rect.x
        self.y = self.rect.y

    def __set_directions(self, dir_x_y: tuple) -> tuple:
        """
        return tuple of directions with the speed modifer
        """

        return (
            dir_x_y[0] * self.firing_speed,
            dir_x_y[1] * self.firing_speed,
        )

    def update_rect(self):
        """
        Update the laser rect after rotation
        """
        self.rect = self.image.get_rect()
        self.rect.center = self.start_coords

    def rotate_image(self, rotation: float):
        """
        Pass the angle that the laser image needs to be rotated
        """
        rotated_image = pygame.transform.rotate(self.image, rotation)
        rotated_rect = rotated_image.get_rect(
            center=self.image.get_rect(center=(self.rect.x, self.rect.y)).center
        )
        self.image = rotated_image
        self.rect = rotated_rect

    def update(self):
        """
        Update laser position
        """
        self.x = float(self.x + self.directions[0])
        self.y = float(self.y + self.directions[1])

        self.rect.x, self.rect.y = self.x, self.y