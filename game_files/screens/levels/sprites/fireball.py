from pygame.rect import Rect
from .projectile_base import Projectile


class Fireball(Projectile):
    def __init__(
        self,
        images: dict,
        element_type: str,
        rotation: float,
        start: tuple,
        directions: tuple,
        special: bool = False,
    ):
        """
        Create fireball transformed based on direction
        images: dict -> {"key": Surface}
        element_type: str -> "red" | "blue" | "purple"
        rotation: float -> angle in degrees
        start: tuple -> (x, y)
        directions: tuple -> (rise, run)
        special: bool=False -> makes a spacial attack fb
        """
        if special:
            firing_speed = 10
        else:
            firing_speed = 15

        self.type = element_type
        self.images = images
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rotate_image(rotation)

        super().__init__(start, directions, firing_speed)

        # animation variables
        self.__counter: int = 1
        self.__index: int = 0
        self.__max_index: int = len(self.images) - 1

    def update(self, scroll_x: float, scroll_y: float):
        self.__counter += 1
        if self.__counter % 8 == 0:
            if self.__counter < self.__max_index:
                self.__index += 1
            else:
                self.__index = 0
            self.image = self.images[self.__index]
            self.__counter = 1

        super().update(scroll_x, scroll_y)
