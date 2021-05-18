import pygame
import os
from pygame.sprite import Sprite
from ..utils.spritesheet import SpriteSheet
from ..utils.game_math import GameMath


class Shield(Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.__load_shield_img()

    def __load_shield_img(self):
        path: str = os.getcwd()
        img_path = os.path.join(
            path, "game_files\sprites\sprite_assets\player_assets\wiz_shield.png"
        )
        self.sprite_sheet = SpriteSheet(img_path)
        self.base_image = self.sprite_sheet.image_at((2, 0, 10, 20), (0, 0, 0))
        self.base_image = pygame.transform.scale(self.base_image, (20, 30))
        self.image = self.base_image
        self.rect = self.image.get_rect()

    def __rotate_image(self, rotation: float):
        """
        Rotate the image so that the front of the shield is facing the mouse
        """
        rotated_image = pygame.transform.rotate(self.base_image, rotation)
        rotated_rect = rotated_image.get_rect(
            center=self.image.get_rect(center=(self.rect.x, self.rect.y)).center
        )

        self.image = rotated_image
        self.rect = rotated_rect

    def reset(self):
        """
        Reset the shields angle
        """
        self.__rotate_image(1.0)

    def set_position(self, pos: tuple, facing_right: bool, angle: float = None):
        """
        pos: sets shields position center
        angle: angles the shield
        """
        # TODO: I need to get the shield to move to the
        # top of the player of the mouse is above the player
        if angle:
            self.__rotate_image(angle)

        if facing_right:
            new_pos = pos[0] + 20, pos[1]
        else:
            new_pos = pos[0] - 20, pos[1]

        self.rect.center = new_pos