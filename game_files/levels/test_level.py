import pygame

from .level_base import LevelBase
from .environment.platform import Platform
from ..screens.screen_colors import ScreenColors
from ..sprites.turret import Turret


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

        pygame.event.set_blocked(pygame.MOUSEMOTION)

        self.colors = ScreenColors()
        self.__load_env()
        self.player.set_position(self.floor.rect.midtop)
        self.__load_turret()
        self.__load_custom_events()
        self.__load_sprite_groups()
        self.turret.firing = True

        self.platform_speed = 2500
        self.turret_spawn_speed = 2500

        # To activate turret
        pygame.time.set_timer(self.start_turret_attack, self.turret.firing_speed)

    def __create_fireball(self, mouse_pos, element_type: str):
        """
        Create the players fireball attack
        """
        fireball = self.player.get_fireball(mouse_pos, element_type)
        self.fireballs.add(fireball)

    def __load_sprite_groups(self):
        """
        Create the sprite groups needed for the level
        """
        self.fireballs = pygame.sprite.Group()

    def __load_turret(self):
        """
        Load turret and set its position
        """
        #TODO: either put in sprie group or re-pos and switch is_alive
        self.turret = Turret(self.turret_assets)
        self.turret.rect.x, self.turret.rect.y = (self.width-self.turret.rect.width, 0)

    def __load_platforms(self):
        """
        Load base platforms for testing
        """
        # x_y
        platform_positions = [
            (0, 100),
            (self.width-50, 175),
            (self.width/2, 250),
            (200, 375),
            (300, 450)
        ]

        for pos in platform_positions:
            self.platforms.add(
                Platform(pos, image=self.platform_assets["floor_image"], w_h=(96, 36))
            )
        

    def __load_floor(self):
        """
        Load base floor
        """
        self.floor = Platform((0, self.height - 25), image=self.platform_assets["floor_image"])
        self.platforms.add(self.floor)

        # make the floor cover the entire width of the screen
        floor_tile_number = round(self.width / self.floor.width) + 1
        for i in range(1, floor_tile_number):
            self.platforms.add(
                Platform((self.floor.width*i, self.height - 25), image=self.platform_assets["floor_image"])
                )

    def __load_env(self):
        """
        Load initial environment
        and platform lists
        """
        self.platforms = pygame.sprite.Group()
        self.__load_floor()
        self.__load_platforms()

    def __load_custom_events(self):
        self.update_player_animation = pygame.USEREVENT + 7
        self.start_turret_attack = pygame.USEREVENT + 8
        self.player_fire_cooldown = pygame.USEREVENT + 9
        self.new_platform = pygame.USEREVENT + 10
        self.spawn_turret = pygame.USEREVENT + 11

    def check_level_events(self, event):
        if event.type == pygame.KEYDOWN:
            self.check_keydown_events(event)

        elif event.type == pygame.KEYUP:
            self.check_keyup_events(event)

        elif event.type == pygame.MOUSEBUTTONDOWN and self.player.can_fire:
            mouse_button = pygame.mouse.get_pressed(3)
            # if mouse left clicked
            if mouse_button[0]:
                self.__create_fireball(event.pos, self.game_ui.active_weapon_bar.element_type)

            elif mouse_button[2] and not self.player.defending:
                # if mouse right clicked
                self.player.shield.moving = True
                self.player.start_defend(event.pos)

            pygame.time.set_timer(self.player_fire_cooldown, self.player.cooldown_time)

        elif event.type == pygame.MOUSEBUTTONUP:
            self.player.defending = False
            self.player.falling = True
            self.player.reset_animation()

        else:
            self.check_user_events(event)

    def check_user_events(self, event):
        # CUSTOM EVENTS
        if event.type == self.start_turret_attack and self.turret.is_alive:
            self.turret.firing = True
            self.turret.create_laser(self.player.rect.center)

        if event.type == self.player_fire_cooldown:
            self.player.can_fire = True

        if event.type == self.new_platform:
            self.__load_platform()
        
        if event.type == self.spawn_turret:
            self.__load_turret()

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

    def __check_platforms(self):
        """
        this method will use logic needed to make the
        climbable platforms work
        """
        # this checks if the player is in the top half or so zone of the platform
        # and if the player is colliding
        # if true then have the player stand on top of the platform
        # This is for platforms the player can jump on top of from underneath
        for platform in self.platforms:
            if (  # If the player should be standing on the platform
                platform.rect.top <= self.player.rect.bottom <= platform.rect.top + 20
                    and pygame.sprite.collide_rect(self.player, platform)
            ):
                self.player.on_ground()
                self.player.rect.bottom = platform.rect.top
            elif pygame.sprite.collide_rect(  # if the player hits the bottom or sides of a platform with their body
                self.player, platform
            ) and (
                self.player.rect.top <= platform.rect.bottom
                or self.player.rect.right >= platform.rect.left
                or self.player.rect.left <= platform.rect.right
            ):
                self.player.stop_movement()
            elif (  # If the player is on the platform and moves off of the right side
                self.player.rect.bottom == platform.rect.top
                and self.player.rect.left >= platform.rect.right
            ):
                self.player.falling = True
            elif (  # If the player is on the platform and moves off of the left side
                self.player.rect.bottom == platform.rect.top
                and self.player.rect.right <= platform.rect.left
            ):
                self.player.falling = True

    def __check_grounded(self):
        """
        check if the player is on the ground
        """
        # If the player is on the floor ( The base platform )
        if pygame.sprite.collide_rect(self.player, self.floor) and self.player.rect.bottom >= self.floor.rect.top:
            self.player.on_ground()
            self.player.rect.bottom = self.floor.rect.top
        elif self.player.rect.bottom == self.floor.rect.top and (
                self.player.rect.right < self.floor.rect.left or self.player.rect.left > self.floor.rect.right
        ):
            self.player.falling = True
        # Check player interaction with climbable platforms
        self.__check_platforms()

        # if the player falls off the bottom of the screen
        if self.player.rect.top > self.rect.bottom:
            self.base_game_over()

    def __check_collisions(self):
        # Need impact sounds
        self.__check_grounded()
        if pygame.sprite.spritecollide(self.player, self.turret.lasers, True):
            self.player_collide_hit()
        if pygame.sprite.spritecollide(self.turret, self.fireballs, True):
            if self.turret.health_points == 0:
                self.turret.is_alive = False
            else:
                self.turret.health_points -= 1
        if pygame.sprite.groupcollide(self.turret.lasers, self.fireballs, True, True):
            pass
        if pygame.sprite.groupcollide(self.platforms, self.turret.lasers, False, True):
            pass
        if pygame.sprite.groupcollide(self.platforms, self.fireballs, False, True):
            pass
        if self.player.defending and (
            laser_list := pygame.sprite.spritecollide(
                self.player.shield, self.turret.lasers, False
            )
        ):
            # TODO: add laser reflection
            self.turret.lasers.remove(laser_list[0])
            pass

    def __blit__sprites(self):
        """
        Blit and update sprites
        """
        self.blit(self.player.image, self.player.rect)
        self.player.update()
        if self.player.defending:
            self.blit(self.player.shield.image, self.player.shield.rect)
        if self.turret.is_alive:
            self.blit(self.turret.image, self.turret.rect)
            self.turret.update()
        self.turret.lasers.update()
        self.fireballs.update()

        for laser in self.turret.lasers:
            self.blit(laser.image, laser.rect)
            if laser.rect.x < -250 or laser.rect.y > self.rect.height:
                self.turret.lasers.remove(laser)
        for fireball in self.fireballs:
            self.blit(fireball.image, fireball.rect)
            if fireball.rect.x < -250 or fireball.rect.y > self.rect.height:
                self.fireballs.remove(fireball)

    def __blit_environment(self):
        """
        blit test level env
        """
        self.blit(self.floor.image, self.floor.rect)
        for platform in self.platforms:
            self.blit(platform.image, platform.rect)

    def __blit_ui(self):
        """
        blit user interface
        """
        for img, rect in self.game_ui.get_ui_components():
            self.blit(img, rect)
        self.game_ui.update(self.player.health_points)

    def update(self):
        """
        Update level elements
        """
        self.check_levelbase_events(self.check_level_events)
        self.__check_collisions()
        self.blit(self.bg_image, self.bg_image_rect)
        self.__blit_environment()
        self.__blit__sprites()
        self.__blit_ui()
