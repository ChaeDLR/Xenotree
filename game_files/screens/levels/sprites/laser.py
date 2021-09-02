from .projectile_base import Projectile


class Laser(Projectile):
    def __init__(self, image, start: tuple, directions: tuple, angle: float):
        """
        Lazer projectile sprite
        """
        self.image = image
        self.rect = self.image.get_rect()
        self.angle_fired: float = angle
        self.rotate_image(angle)
        super().__init__(start, directions, firingspeed=20)

    def reflect_laser(self):
        pass
