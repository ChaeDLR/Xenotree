import pygame
import os
from pygame.sprite import Sprite


class Player(Sprite):
    """ player sprite class """

    def __init__(self, level_surface):
        super().__init__()
        self.screen_rect = level_surface.rect
        self.screen_rows = self.screen_rect.bottom/14
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

    def _load_player_image(self):
        """ Load player image from assets folder """
        # set player image
        path = os.path.dirname(__file__)
        self.image = pygame.image.load(
            os.path.join(path, 'sprite_images/player_ship.png'))
        self.player_hit_images = [
            self.image, pygame.image.load(os.path.join(
                path, 'sprite_images/player_lighten.png'))
        ]

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

    def move_forward(self):
        """ move player forward """
        if not self.player_hit:
            self.y -= self.screen_rows
            self.rect.y = self.y

    def move_backward(self):
        """ move player backward """
        if not self.player_hit:
            if self.rect.bottom < self.screen_rect.bottom:
                self.y += self.screen_rows
            self.rect.y = self.y

    def move_left(self):
        if not self.player_hit and (self.x-self.movement_speed) >= 0:
            self.x -= self.movement_speed
            self.rect.x = self.x
        elif not self.player_hit:
            self.x = 0
            self.rect.x = self.x

    def move_right(self):
        if not self.player_hit and (self.x+self.movement_speed) <= self.screen_rect.right:
            self.x += self.movement_speed
            self.rect.x = self.x
        elif not self.player_hit:
            self.rect.right = self.screen_rect.right