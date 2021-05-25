import pygame
import os
from ..utils.spritesheet import SpriteSheet
from .projectile_base import Projectile


class Shield(Projectile):
    """
    Shield will move like a projectile until it reaches the end of the player
    """

    def __init__(self) -> None:
        super().__init__()
        self.__load_shield_img()
        # bool value that will control movement
        self.moving = False

    def __load_shield_img(self):
        path: str = os.getcwd()
        img_path = os.path.join(
            path, "game_files/sprites/sprite_assets/player_assets/wiz_shield.png"
        )
        self.sprite_sheet = SpriteSheet(img_path)
        self.base_image = self.sprite_sheet.image_at((2, 0, 10, 20), (0, 0, 0))
        self.base_image = pygame.transform.scale(self.base_image, (15, 45))
        self.image = self.base_image
        self.rect = self.image.get_rect()

    def rotate_image(self, rotation: float):
        """
        Rotate the image so that the front of the shield is facing the mouse
        """
        rotated_image = pygame.transform.rotate(self.base_image, rotation)
        rotated_rect = rotated_image.get_rect(
            center=self.image.get_rect(center=(self.rect.x, self.rect.y)).center
        )

        self.movement_counter = 0
        self.image = rotated_image
        self.rect = rotated_rect
        self.rect.center = self.start_coords

    def update(self):
        """
        Update position
        Override projectile update
        """
        if self.movement_counter >= 2:
            return
        elif self.moving:
            self.x = float(self.x + self.directions[0])
            self.y = float(self.y + self.directions[1])
            self.rect.x, self.rect.y = self.x, self.y
            self.movement_counter += 1
