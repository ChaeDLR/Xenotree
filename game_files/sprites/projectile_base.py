from pygame.sprite import Sprite
from pygame.rect import Rect
from pygame.transform import rotate
from abc import ABC, abstractmethod, ABCMeta

class Projectile(Sprite, ABC):
    def __init__(self):
        super().__init__()
        self.rect = Rect((0, 0), (10, 10))
        self.firing_speed = 25
    
    @abstractmethod
    def load_img(self):
        """
        Load the projectiles image or images
        and set the rect
        """
        pass

    def set_start(self, start_x_y: tuple, dir_x_y: tuple) -> None:
        """
        Set the variables needed to position the projectile
        """
        self.start_coords = start_x_y
        self.rect.center = start_x_y
        self.directions = (
            dir_x_y[0] * self.firing_speed,
            dir_x_y[1] * self.firing_speed
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
        rotated_image = rotate(self.image, rotation)
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

    