import pygame
import math
from .level_base import LevelBase
from .environment.wall import Wall
from ..screens.screen_colors import ScreenColors
from ..sprites.turret import Turret
from ..sprites.laser import Laser


class TestLevel(LevelBase):
    def __init__(
        self,
        width: int,
        height: int,
        settings: object,
        stats: object,
        game_sound: object,
    ):
        super().__init__(width, height, settings, stats, game_sound)

        self.colors = ScreenColors()
        self.__load_floor(width, height)
        self.player.rect.midbottom = self.floor.rect.midtop
        self.__load_turret()
        self.__load_custom_events()
        self.__load_sprite_groups()

        self.turret.firing = True

        # To test the turret animations
        pygame.time.set_timer(self.start_turret_attack, 5000)

    def __create_laser(self):
        """
        Create a laser for the turret to fire
        """
        # takes ypos of destination - ypos of start point then x
        rads = math.atan2(
            self.player.rect.y - self.turret.rect.y,
            self.player.rect.x - self.turret.rect.x,
        )

        # get directions for x and y
        directions = (math.cos(rads), math.sin(rads))
        # Create the laser and give it the starting point and it's directions
        laser = Laser(self.turret.rect.center, directions)

        angle = (180 / math.pi) * rads
        laser.rotate_image(angle)
        laser.update_rect()
        self.lasers.add(laser)

    def __load_sprite_groups(self):
        """
        Create the sprite groups needed for the level
        """
        self.lasers = pygame.sprite.Group()

    def __load_turret(self):
        """
        Load turret and set its position
        """
        self.turret = Turret(self.rect)
        self.turret.rect.top = self.rect.top
        self.turret.rect.right = self.rect.right

    def __load_floor(self, level_w: int, level_h: int):
        self.floor = Wall((level_w, 25), (0, level_h - 25))

    def __load_custom_events(self):
        self.update_player_animation = pygame.USEREVENT + 7
        self.start_turret_attack = pygame.USEREVENT + 8

    def check_level_events(self, event):
        if event.type == pygame.KEYDOWN:
            self.check_keydown_events(event)
        elif event.type == pygame.KEYUP:
            self.check_keyup_events(event)
        elif event.type == self.start_turret_attack:
            self.turret.firing = True
            self.__create_laser()

    def check_keydown_events(self, event):
        """ check for and respond to player keydown input """
        if event.key == pygame.K_ESCAPE:
            self.pause_events()
        # Player movement
        self.player_keydown_controller(event)

    def check_keyup_events(self, event):
        """ Check for and respond to player keyup events """
        self.player_keyup_controller(event)

    def __check_grounded(self):
        """
        check if the player is on the ground
        """
        if self.player.rect.bottom >= self.floor.rect.top:
            self.player.jumping = False
            self.player.rect.bottom = self.floor.rect.top

    def update(self):
        """
        Update level elements
        """
        self.check_levelbase_events(self.check_level_events)
        self.__check_grounded()
        self.fill(self.colors.level_one_bg, self.rect)
        self.blit(self.floor.image, self.floor.rect)
        self.blit(self.player.image, self.player.rect)
        self.player.update()
        self.blit(self.turret.image, self.turret.rect)
        self.turret.update()
        self.lasers.update()
        for laser in self.lasers:
            self.blit(laser.image, laser.rect)
            if laser.rect.x < -250 or laser.rect.y > self.rect.height:
                self.lasers.remove(laser)
