import pygame

from ..utils.game_math import GameMath
from ..game_assets import AssetManager
from .level_base import LevelBase
from .environment.platform import Platform
from ..screens.screen_colors import ScreenColors
from ..sprites.turret import Turret
from ..sprites.laser import Laser
from ..sprites.fireball import Fireball


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
        self.__load_env()
        self.player.rect.midbottom = self.floor.rect.midtop
        self.__load_turret()
        self.__load_custom_events()
        self.__load_sprite_groups()
        self.assets: dict = AssetManager.level_one_assets()
        self.turret.firing = True

        # To activate turret
        pygame.time.set_timer(self.start_turret_attack, 1600)

    def __create_laser(self):
        """
        Create a laser for the turret to fire
        """
        directions = GameMath.get_directions(
            (self.turret.rect.x, self.turret.rect.y),
            (self.player.rect.x, self.player.rect.y),
        )
        
        # Create the laser and give it the starting point and it's directions
        laser = Laser(self.assets["laser_img"])
        laser.set_start(self.turret.rect.center, directions)

        angle = GameMath.get_angle_to(
            (self.turret.rect.x, self.turret.rect.y),
            (self.player.rect.x, self.player.rect.y),
        )
        laser.rotate_image(angle)
        laser.update_rect()
        self.lasers.add(laser)
    
    def __create_fireball(self, mouse_pos):
        """
        Create the players fireball attack
        """
        fireball_start_pos: list = [self.player.rect.center[0], self.player.rect.center[1]+5]
        # set the x-axis offset of the fireball spawn position based on which way the player is facing
        if self.player.facing_left:
            fireball_start_pos[0] -= 10
        elif self.player.facing_right:
            fireball_start_pos[0] += 10

        directions = GameMath.get_directions(
            fireball_start_pos,
            mouse_pos
        )

        fireball = Fireball(self.assets["red_fb_fire_imgs"][0])
        fireball.set_start(fireball_start_pos, directions)

        angle = GameMath.get_angle_to(
            fireball_start_pos,
            mouse_pos
        )
        fireball.rotate_image(angle)
        fireball.update_rect()
        self.fireballs.add(fireball)


    def __load_sprite_groups(self):
        """
        Create the sprite groups needed for the level
        """
        self.lasers = pygame.sprite.Group()
        self.fireballs = pygame.sprite.Group()

    def __load_turret(self):
        """
        Load turret and set its position
        """
        self.turret = Turret(self.rect)
        self.turret.rect.top = self.rect.top
        self.turret.rect.right = self.rect.right
    
    def __load_climbable_platforms(self):
        """
        Load platforms that are climbable
        """
        platform = Platform((self.width / 2, 40), (0, self.height / 4))
        platform_2 = Platform((self.width/2, 40), (self.width/2, (self.height / 3)*2))
        self.climbable_platforms.append(platform)
        self.climbable_platforms.append(platform_2)

    def __load_floor(self):
        """
        Load base floor
        """
        self.floor = Platform((self.width, 50), (0, self.height - 25))
    
    def __load_env(self):
        """
        Load initial environment
        and platform lists
        """
        self.climbable_platforms = []
        self.__load_climbable_platforms()
        self.__load_floor()

    def __load_custom_events(self):
        self.update_player_animation = pygame.USEREVENT + 7
        self.start_turret_attack = pygame.USEREVENT + 8
        self.player_fire_cooldown = pygame.USEREVENT + 9

    def check_level_events(self, event):
        if event.type == pygame.KEYDOWN:
            self.check_keydown_events(event)
        elif event.type == pygame.KEYUP:
            self.check_keyup_events(event)
        elif event.type == pygame.MOUSEBUTTONDOWN and self.player.can_fire:
            self.__create_fireball(event.pos)
            self.player.can_fire = False
            pygame.time.set_timer(self.player_fire_cooldown, self.player.cooldown_time)
        elif event.type == self.start_turret_attack and self.turret.is_alive:
            self.turret.firing = True
            self.__create_laser()
        elif event.type == self.player_fire_cooldown:
            self.player.can_fire = True

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

    def __check_climb_platforms(self):
        """
        this method will use logic needed to make the
        climbable platforms work
        """
        # this checks if the player is in the top half or so zone of the platform
        # and if the player is colliding
        # if true then have the player stand on top of the platform
        # This is for platforms the player can jump on top of from underneath
        for platform in self.climbable_platforms:
            # If the player should be standing on the platform
            if (
                self.player.rect.bottom >= platform.rect.top
                and self.player.rect.bottom <= platform.rect.top + 20
                and pygame.sprite.collide_rect(self.player, platform)
            ):
                self.player.on_ground()
                self.player.rect.bottom = platform.rect.top
            # If the player is on the platform and moves off of the right side
            elif (
                self.player.rect.bottom == platform.rect.top
                and self.player.rect.left >= platform.rect.right
            ):
                self.player.falling = True
            # If the player is on the platform and moves off of the left side
            elif (
                self.player.rect.bottom == platform.rect.top
                and self.player.rect.right <= platform.rect.left
            ):
                self.player.falling = True

    def __check_grounded(self):
        """
        check if the player is on the ground
        """
        # If the player is on the floor ( The base platform )
        if self.player.rect.bottom >= self.floor.rect.top:
            self.player.on_ground()
            self.player.rect.bottom = self.floor.rect.top
        # Check player interaction with climbable platforms
        self.__check_climb_platforms()
        

    def __check_collisions(self):
        self.__check_grounded()
        if pygame.sprite.spritecollide(self.player, self.lasers, True):
            self.player_collide_hit()
        if pygame.sprite.spritecollide(self.turret, self.fireballs, True):
            if self.turret.health_points == 0:
                self.turret.is_alive = False
            else:
                self.turret.health_points -= 1
        for platform in self.climbable_platforms:
            if pygame.sprite.spritecollide(platform, self.lasers, True):
                # Add impact sound
                pass
            if pygame.sprite.spritecollide(platform, self.fireballs, True):
                pass


    def __blit__sprites(self):
        """
        Blit and update sprites
        """
        self.blit(self.player.image, self.player.rect)
        self.player.update()
        if self.turret.is_alive:
            self.blit(self.turret.image, self.turret.rect)
            self.turret.update()
        self.lasers.update()
        self.fireballs.update()

        for laser in self.lasers:
            self.blit(laser.image, laser.rect)
            if laser.rect.x < -250 or laser.rect.y > self.rect.height:
                self.lasers.remove(laser)
        for fireball in self.fireballs:
            self.blit(fireball.image, fireball.rect)
            if fireball.rect.x < -250 or fireball.rect.y > self.rect.height:
                self.fireballs.remove(fireball)

    def __blit_environment(self):
        """
        blit test level env
        """
        self.blit(self.floor.image, self.floor.rect)
        for platform in self.climbable_platforms:
            self.blit(platform.image, platform.rect)

    def update(self):
        """
        Update level elements
        """
        self.check_levelbase_events(self.check_level_events)
        self.__check_collisions()
        self.fill(self.colors.level_one_bg, self.rect)
        self.blit(self.bg_image, self.bg_image_rect)
        self.__blit_environment()
        self.__blit__sprites()
