from .projectile_base import Projectile


class Fireball(Projectile):
    def __init__(self, images: dict, type: str):
        """
        Create fireball transformed based on direction
        """
        super().__init__()
        self.images = images
        self.firing_speed = 20
        self.type = type

        self.__set_type()
        self.rect = self.image.get_rect()

    def __set_type(self):
        """
        Set the fireball type
        """
        if self.type == "red":
            self.base_image = self.images["red_fb_fire_imgs"][1]
            self.image = self.base_image
        elif self.type == "blue":
            self.base_image = self.images["blue_fb_fire_imgs"][1]
            self.image = self.base_image
        elif self.type == "purple":
            self.base_image = self.images["purple_fb_fire_imgs"][1]
            self.image = self.base_image

    def update(self):
        super().update()
