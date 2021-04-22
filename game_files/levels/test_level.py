import pygame

from ..utils.game_math import GameMath
from .level_base import LevelBase
from .environment.platform import Platform
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

        # To activate turret
        # pygame.time.set_timer(self.start_turret_attack, 1700)

    def __create_laser(self):
        """
        Create a laser for the turret to fire
        """

        directions = GameMath.get_directions(
            (self.turret.rect.x, self.turret.rect.y),
            (self.player.rect.x, self.player.rect.y),
        )

        # Create the laser and give it the starting point and it's directions
        laser = Laser(self.turret.rect.center, directions)

        angle = GameMath.get_angle_to(
            (self.turret.rect.x, self.turret.rect.y),
            (self.player.rect.x, self.player.rect.y),
        )
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
        self.floor = Platform((level_w, 50), (0, level_h - 25))
        self.platform_one = Platform((level_w / 2, 50), (0, level_h / 4))

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
        else:
            # Player movement
            self.player_keydown_controller(event)

    def check_keyup_events(self, event):
        """ Check for and respond to player keyup events """
        self.player_keyup_controller(event)

    def __check_grounded(self):
        """
        check if the player is on the ground
        """
        # If the player is on the floor ( The base platform )
        if self.player.rect.bottom >= self.floor.rect.top:
            self.player.on_ground()
            self.player.rect.bottom = self.floor.rect.top
        # this checks if the player is in the top half or so zone of the platform
        # and if the player is colliding
        # if true then have the player stand on top of the platform
        # This is for platforms the player can jump on top of from underneath
        elif (
            self.player.rect.bottom >= self.platform_one.rect.top
            and self.player.rect.bottom <= self.platform_one.rect.top + 10
            and pygame.sprite.collide_rect(self.player, self.platform_one)
        ):
            self.player.on_ground()
            self.player.rect.bottom = self.platform_one.rect.top
        elif (
            self.player.rect.bottom == self.platform_one.rect.top
            and self.player.rect.left >= self.platform_one.rect.right
        ):
            self.player.falling = True

    def __check_collisions(self):
        self.__check_grounded()
        if pygame.sprite.spritecollide(self.player, self.lasers, True):
            self.player_collide_hit()

    def __blit__sprites(self):
        """
        Blit and update sprites
        """
        self.blit(self.player.image, self.player.rect)
        self.player.update()
        self.blit(self.turret.image, self.turret.rect)
        self.turret.update()
        self.lasers.update()
        for laser in self.lasers:
            self.blit(laser.image, laser.rect)
            if laser.rect.x < -250 or laser.rect.y > self.rect.height:
                self.lasers.remove(laser)

    def __blit_environment(self):
        """
        blit test level env
        """
        self.blit(self.floor.image, self.floor.rect)
        self.blit(self.platform_one.image, self.platform_one.rect)

    def update(self):
        """
        Update level elements
        """
        self.check_levelbase_events(self.check_level_events)
        self.__check_collisions()
        self.fill(self.colors.level_one_bg, self.rect)
        self.__blit_environment()
        self.__blit__sprites()
