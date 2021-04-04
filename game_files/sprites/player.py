import pygame
import os
from pygame import image
from pygame.sprite import Sprite
from ..utils.spritesheet import SpriteSheet


class Player(Sprite):
    """ player sprite class """

    def __init__(self, level_surface):
        super().__init__()
        self.screen_rect = level_surface.rect
        self.screen_rows = self.screen_rect.bottom / 14

        self.__create_animation_variables()
        self._load_player_image()
        self.player_hit = False
        self.death_frame = 1

        self.rect = self.image.get_rect()

        self.movement_speed = 64.0

        # set player initial position
        self.rect.midbottom = self.screen_rect.midbottom
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)

        self.moving_left = False
        self.moving_right = False

    def __create_animation_variables(self):
        """ These are the animation variables needed to animate the player smoothly """
        self.animation_index = 0
        self.animation_index_limit = 0
        self.animation_counter = 0

    def _ss_idle_coords(self) -> list:
        """ Rect positions and sizes needed to cut the sprite sheet for the idle images """
        idle: list = [
            (8, 1, 21, 30),
            (40, 0, 21, 30),
            (72, 0, 24, 30),
            (100, 1, 25, 30),
            (133, 2, 24, 30),
        ]
        return idle

    def _load_player_image(self):
        """ Load player image from assets folder """
        p_colorkey = (0, 0, 0)
        # set player image
        current_path = os.path.dirname(__file__)
        player_ss_path = os.path.join(
            current_path, "sprite_assets/player_assets/MageSpriteSheet.png"
        )
        ss_tool = SpriteSheet(player_ss_path)

        self.idle_images = []
        idle_coords = self._ss_idle_coords()
        for coord in idle_coords:
            image = ss_tool.image_at(coord, p_colorkey)
            image = pygame.transform.scale(image, (38, 56))
            self.idle_images.append(image)
        self.image = self.idle_images[0]
        self.animation_index_limit = len(self.idle_images)-1

    def reset_player(self):
        """ reset player position """
        # set player initial position
        self.rect.midbottom = self.screen_rect.midbottom
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)

    def check_position(self):
        """ check that the player position is in bounds """
        if self.rect.top < 31:
            return True
        else:
            return False

    def move_left(self):
        if not self.player_hit and (self.x - self.movement_speed) >= 0:
            self.x -= self.movement_speed
            self.rect.x = self.x
        elif not self.player_hit:
            self.x = 0
            self.rect.x = self.x

    def move_right(self):
        if (
            not self.player_hit
            and (self.x + self.movement_speed) <= self.screen_rect.right
        ):
            self.x += self.movement_speed
            self.rect.x = self.x
        elif not self.player_hit:
            self.rect.right = self.screen_rect.right

    # TODO: Need to fix the player animation speed
    def update_animation(self):
        """
        Update the player animation frame
        """
        self.image = self.idle_images[self.animation_index]
        self.animation_counter += 1

        # if we get told to change the animation 
        if self.animation_counter % 16 == 0:
            # check if the animation is the last in the list
            if self.animation_index == self.animation_index_limit:
                self.animation_counter = 0
                self.animation_index = 1 # if i cut off the first image in the list the animation looks a lot smoother
            else:
                self.animation_index += 1
