from pygame.sprite import Sprite
from pygame import Surface
import pygame


class Laser(Sprite):
    def __init__(self, x_y: tuple):
        """
        Give the x_y position it should spawn at.
        """
        super().__init__()

        self.image = Surface((12, 28))
        self.image.fill((250, 10, 10))
        self.rect = self.image.get_rect()
        self.rect.x = x_y[0] + 16
        self.rect.y = x_y[1] + 16
        self.firing_speed = 25
        self._rotate_image(90)

    def _rotate_image(self, rotation: float):
        """
        Pass the angle that the laser image needs to be rotated
        """
        rotated_image = pygame.transform.rotate(self.image, rotation)
        rotated_rect = rotated_image.get_rect(
            center=self.image.get_rect(center=(self.rect.x, self.rect.y)).center
        )
        self.image = rotated_image
        self.rect = rotated_rect

    # TODO: Get the laser to spawn and update across a line to it's target
    def update(self):
        """
        Update laser position
        """
        pass
        # self.rect.x, self.rect.y =
