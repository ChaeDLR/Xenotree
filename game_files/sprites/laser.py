from .projectile_base import Projectile


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

    def reflect_laser(self):
        pass
