import pygame
import os
from pygame.sprite import Sprite, Group
from ..utils.game_math import GameMath
from .laser import Laser


class Turret(Sprite):
    """ Turret enemy class """

    def __init__(self, images: dict):
        """
        image assets with keys 
        "laser_img": surface, "turret_images": list
        """
        super().__init__()
        self.images: list = images["turret_images"]
        self.mask = pygame.mask.from_surface(self.images[0])
        self.laser_image = images["laser_img"]
        # vars that will control the turret animations
        self.animation_counter = 0
        self.animation_index = 0
        # If firing is turned True the update method will change the image
        self.firing: bool = False
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.health_points: int = 3
        self.firing_speed = 1700
        self.is_alive: bool = True
        self.lasers = Group()
    
    def create_laser(self, target: tuple):
        """
        Create the laser and do the math to set starting position
        + angle + directions
        target: tuple -> (x, y)
        """
        directions = GameMath.get_directions(
            (self.rect.x, self.rect.y),
            target
        )

        laser = Laser(self.laser_image)
        laser.set_start(self.rect.center, directions)

        angle = GameMath.get_angle_to(
            (self.rect.x, self.rect.y),
            target
        )

        laser.rotate_image(angle)
        laser.update_rect()
        laser.angle_fired = angle
        self.lasers.add(laser)


    def set_position(self, x_y: tuple):
        """ Set the turret position """
        self.rect.x, self.rect.y = x_y[0], x_y[1]

    # TODO: Get the turrets to take and image from asset manager and spawn lasers
    # from within this class
    def __load_assets(self) -> list:
        """
        Load the turret images
        Return list of the images
        """
        current_path = os.path.dirname(__file__)
        turret_imgs_path = os.path.join(current_path, "sprite_assets/turret")
        images_list: list = os.listdir(turret_imgs_path)
        # Sort the images by the number value in the file name string
        images_list.sort(key=lambda img_string: img_string[7])

        loaded_images: list = []
        for img in images_list:
            img_path = os.path.join(turret_imgs_path, img)
            loaded_images.append(pygame.image.load(img_path).convert())
            
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

        if self.animation_index == 5:
            # Reset animation variables
            self.__reset_animation()
            self.firing = False

    def update(self):
        """
        Update the turret
        """
        # If the turret is attacking we want to play the attack animation
        if self.firing and self.is_alive:
            self.__attack_animation()
        self.image = self.images[self.animation_index]
