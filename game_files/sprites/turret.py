import pygame
import os
from pygame.sprite import Sprite

# TODO: Collect all of the turret images into a spritesheet
# from ..utils.spritesheet import SpriteSheet


class Turret(Sprite):
    """ Turret enemy class """

    def __init__(self, level_rect):
        super().__init__()
        self.screen_rect = level_rect

        self.images: list = self.__load_assets()

        # vars that will control the turret animations
        self.animation_counter = 0
        self.animation_index = 0
        # If firing is turned True the update method will change the image
        self.firing = False
        self.image = self.images[0]
        self.rect = self.image.get_rect()

    def set_position(self, x_y: tuple):
        """ Set the turret position """
        self.rect.x, self.rect.y = x_y[0], x_y[1]

    def __load_assets(self) -> list:
        """
        Load the turret images
        Return list of the images
        """
        current_path = os.path.dirname(__file__)
        turret_imgs_path = os.path.join(current_path, "sprite_assets/turret")
        images_list: list = os.listdir(turret_imgs_path)

        loaded_images: list = []
        for img in images_list:
            img_path = os.path.join(turret_imgs_path, img)
            loaded_images.append(pygame.image.load(img_path))
        return loaded_images

    def __reset_animation(self):
        """
        Reset animation vars
        """
        self.animation_counter = 0
        self.animation_index = 0

    def __attack_animation(self):
        """
        Start the attack animation
        """
        # Turret animates pretty well at this pace
        self.animation_counter += 1

        if self.animation_counter == 20:
            self.animation_index += 1
            self.animation_counter = 0

        if self.animation_index > 4:
            # Reset animation variables
            self.__reset_animation()
            self.firing = False

    def update(self):
        """
        Update the turret
        """
        # If the turret is attacking we want to play the attack animation
        if self.firing:
            self.__attack_animation()
        self.image = self.images[self.animation_index]
