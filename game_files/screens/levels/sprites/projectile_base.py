from pygame.sprite import Sprite
from pygame.transform import rotate
from pygame import Vector2
from pygame import mask


class Projectile(Sprite):
    def __init__(self, start: tuple, directions: tuple, firingspeed: int):
        """
        start: tuple -> (x, y)
        directions: tuple -> (run | x, rise | y)
        firingspeed: int -> speed modifier
        """
        super().__init__()
        self.rect.center = start
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.firing_speed: int = firingspeed

        self.directions = (
            directions[0] * self.firing_speed,
            directions[1] * self.firing_speed,
        )

    def rotate_image(self, rotation: float) -> tuple:
        """
        Pass the angle that the laser image needs to be rotated
        """
        if hasattr(self, "images"):
            rotated_imgs: list = []
            for img in self.images:
                rotated_image = rotate(img, rotation)
                rotated_imgs.append(rotated_image)
            self.images = rotated_imgs
        else:
            rotated_image = rotate(self.image, rotation)

        self.image = rotated_image
        self.rect = rotated_image.get_rect(center=self.rect.center)
        self.mask = mask.from_surface(self.image)

    def update(self, scroll_x: float, scroll_y: float):
        """
        Update position
        """
        self.x += float(self.directions[0] + scroll_x)
        self.y += float(self.directions[1] + scroll_y)
        self.rect.x, self.rect.y = self.x, self.y
