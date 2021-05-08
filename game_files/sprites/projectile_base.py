from pygame.sprite import Sprite
from pygame.rect import Rect
from pygame.transform import rotate

class Projectile(Sprite):
    def __init__(self):
        super().__init__()
        self.firing_speed = 20

    def set_start(self, start_x_y: tuple, dir_x_y: tuple) -> None:
        """
        Set the variables needed to position the projectile
        """
        self.start_coords = start_x_y
        self.rect.center = start_x_y
        self.x = self.rect.x
        self.y = self.rect.y
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
        self.rect.center = self.start_coords

    def update(self):
        """
        Update laser position
        """
        self.x = float(self.x + self.directions[0])
        self.y = float(self.y + self.directions[1])

        self.rect.x, self.rect.y = self.x, self.y

    