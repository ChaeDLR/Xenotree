from .projectile_base import Projectile
from pygame import mask

class Laser(Projectile):
    def __init__(self, image):
        """
        Get the laser img asset
        Set image and rect
        """
        super().__init__()
        self.base_image = image
        self.image = self.base_image
        self.rect = self.image.get_rect()

    def rotate_image(self, angle: float):
        """
        override parents rotate image so we can add the change in mask
        """
        super().rotate_image(angle)
        self.mask = mask.from_surface(self.image)

    def reflect_laser(self):
        pass
