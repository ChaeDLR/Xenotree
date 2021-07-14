import pygame
import random

from .level_base import LevelBase
from .environment.platform import Platform
from ..screens.screen_colors import ScreenColors
from ..sprites.turret import Turret
from ..screens.pause_menu import PauseMenu


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
        self.player.set_position((25, self.height - 26))
        self.__load_turret()
        self.__load_custom_events()

        # has check events in update
        self.pause_menu = PauseMenu(
            (self.settings.screen_width, self.settings.screen_height),
            self.game_stats,
            self.settings,
            self.unpause
        )

        self.turret.firing = True

        # spawnspeed_movementspeed
        self.difficulty = [
            (0, 0),
            (3000, 2.0),
            (2800, 2.5),
            (2500, 3.0),
            (2200, 3.5),
            (2000, 4.0),
            (1800, 4.5),
        ]

        self.difficulty_mode: int = 0

        self.turret_spawn_speed = 2500

        self.__set_timers()
        pygame.time.set_timer(self.start, 3000, True)
        self.s_capture = pygame.time.get_ticks()

    def __start_movement(self):
        """
        start platform movement and timers
        """
        for platform in self.platforms:
            platform.moving = True
        # start platform spawning loop
        pygame.time.set_timer(
            self.spawn_platform, self.difficulty[self.difficulty_mode][0], True
        )
        self.sp_capture = pygame.time.get_ticks()

    def __set_timers(self):
        """ Set levels timers """
        # To activate turret
        pygame.time.set_timer(self.start_turret_attack, self.turret.firing_speed, True)
        self.sta_capture = pygame.time.get_ticks()

    def __disable_timers(self):
        """
        disable the levels custom timers
        """
        pygame.time.set_timer(self.start_turret_attack, 0)
        pygame.time.set_timer(self.difficulty_increase, 0)
        pygame.time.set_timer(self.player_fire_cooldown, 0)
        pygame.time.set_timer(self.player_dead, 0)
        pygame.time.set_timer(self.start, 0)
        pygame.time.set_timer(self.spawn_platform, 0)

    def __capture_timers(self):
        """
        Capture how much time a timer has waited
        and calculate how much time if left on it
        """
        current_time = pygame.time.get_ticks()

        if not self.player.can_fire:
            self.pfc_capture = current_time - self.pfc_capture

        if self.player.dying:
            self.pd_capture = current_time - self.pd_capture

        if self.turret.firing:
            self.sta_capture = current_time - self.sta_capture

        if self.difficulty_mode >= 1:
            self.s_capture = current_time - self.s_capture
            self.sp_capture = current_time - self.sp_capture

        self.di_capture = current_time - self.di_capture

    def __load_turret(self):
        """
        Load turret and set its position
        """
        # TODO: either put in sprite group or re-pos and switch is_alive
        self.turret = Turret(self.turret_assets)
        self.turret.rect.x, self.turret.rect.y = (
            self.width - self.turret.rect.width,
            0,
        )

    def __load_platforms(self):
        """
        Load base platforms for testing
        """
        platform_positions = [
            (self.width - 50, 175),
            (self.width / 2, 250),
            (200, 450),
            (300, 375),
        ]

        for pos in platform_positions:
            self.platforms.add(
                Platform(pos, image=self.platform_assets["floor_image"], w_h=(96, 36))
            )

    def __load_floor(self):
        """
        Load base floor
        """
        floor_image = self.platform_assets["floor_image"]
        floor_width = floor_image.get_width()

        # make the floor cover the entire width of the screen
        floor_tile_number = round(self.width / floor_width) + 1
        for i in range(0, floor_tile_number):
            if i == floor_tile_number - 1:
                connected_right = False
            else:
                connected_right = True

            floor_tile = Platform(
                (floor_width * i, self.height - 25),
                image=floor_image,
                connect_left=True,
                connect_right=connected_right,
            )
            self.platforms.add(floor_tile)

    def __load_env(self):
        """
        Load initial environment
        and platform lists
        """
        self.platforms = pygame.sprite.Group()
        self.__load_floor()
        self.__load_platforms()

    def __load_custom_events(self):
        """
        Load custom events and their capture variable if they need one
        """
        self.start_turret_attack = pygame.USEREVENT + 9
        self.spawn_turret = pygame.USEREVENT + 10
        self.spawn_platform = pygame.USEREVENT + 11
        self.start = pygame.USEREVENT + 12
        self.difficulty_increase = pygame.USEREVENT + 13

        self.sta_capture: int = 0
        self.sp_capture: int = 0
        self.s_capture: int = 0
        self.di_capture: int = 0

    def __check_platforms(self):
        """
        this method will use logic needed to make the
        climbable platforms work
        """
        if (
            self.player.rect.top > self.rect.bottom
            or (self.player.rect.x + self.player.rect.width) < 0
        ):
            self.game_over()

        for platform in self.platforms:
            if (platform.rect.x + platform.rect.width) < 0:
                self.platforms.remove(platform)
                continue

            if pygame.sprite.collide_mask(self.player, platform):
                self.player.dashing = False
                if self.player.dying:
                    self.player.falling = False
                    self.player.rect.bottom = platform.rect.top + 20
                elif (
                    platform.rect.top
                    <= self.player.rect.bottom
                    <= platform.rect.top + 20
                    and self.player.falling
                ):
                    self.player.on_ground()
                    self.player.rect.bottom = platform.rect.top - 2
                elif (
                    platform.rect.left + 20
                    > self.player.rect.right
                    >= platform.rect.left - 1
                    and self.player.moving_right
                ):
                    self.player.x = platform.rect.left - (self.player.rect.width + 2)
                    self.player.rect.x = self.player.x
                    self.player.stop_movement(self.player.moving_left, False)
                elif (
                    platform.rect.right - 20
                    < self.player.rect.left
                    <= platform.rect.right + 1
                    and self.player.moving_left
                ):
                    self.player.x = platform.rect.right + 2
                    self.player.rect.x = self.player.x
                    self.player.stop_movement(False, self.player.moving_right)
                elif (
                    self.player.rect.top <= platform.rect.bottom and self.player.jumping
                ):
                    self.player.jumping = False
                    self.player.falling = True
            elif self.player.rect.bottom == platform.rect.top - 2 and (
                (
                    self.player.rect.left >= platform.rect.right
                    and not platform.connected_right
                )
                or (
                    self.player.rect.right <= platform.rect.left
                    and not platform.connected_left
                )
            ):
                self.player.falling = True

    def __turret_laser_collisions(self):
        """
        Check the turret laser for collisions
        """
        if not self.player.dying and (
            pygame.sprite.spritecollide(
                self.player,
                self.turret.lasers,
                True,
                collided=pygame.sprite.collide_mask,
            )
            or pygame.sprite.collide_mask(self.player, self.turret)
        ):
            self.player_collide_hit()
        if pygame.sprite.groupcollide(
            self.turret.lasers,
            self.player.fireballs,
            True,
            True,
            collided=pygame.sprite.collide_mask,
        ):
            pass
        if pygame.sprite.groupcollide(
            self.platforms,
            self.turret.lasers,
            False,
            True,
            collided=pygame.sprite.collide_mask,
        ):
            pass

    def __fireballs_collisions(self):
        """
        Check for the fireball collisions
        """
        if pygame.sprite.groupcollide(
            self.platforms,
            self.player.fireballs,
            False,
            True,
            collided=pygame.sprite.collide_mask,
        ):
            pass
        if pygame.sprite.spritecollide(
            self.turret,
            self.player.fireballs,
            True,
            collided=pygame.sprite.collide_mask,
        ):
            if self.turret.health_points == 0:
                self.turret.is_alive = False
            else:
                self.turret.health_points -= 1

    def __create_new_platform(self):
        """
        Create a new platform starting on the right side of the screen
        """
        random.seed()
        screen_height_section: int = self.height / 6

        try:
            platform_y = random.randint(
                self.platform_min_limit, self.height - screen_height_section
            )
        except:
            platform_y = random.randint(
                screen_height_section, self.height - screen_height_section
            )

        self.platform_min_limit = platform_y - screen_height_section

        # randomly determine how many platforms to connect
        new_platforms: list = [
            Platform(
                (self.width, platform_y),
                image=self.platform_assets["floor_image"],
                moving=True,
            )
        ]
        platform_width = new_platforms[0].width

        if random.choice((0, 1)) == 1:  # add a connecting platform
            new_platforms[len(new_platforms) - 1].connected_right = True

            x_y: tuple = (
                (self.width + (platform_width * len(new_platforms))),
                platform_y,
            )

            self.platform_min_limit = x_y[1] - screen_height_section

            new_platforms.append(
                Platform(
                    x_y,
                    image=self.platform_assets["floor_image"],
                    connect_left=True,
                    moving=True,
                )
            )

        for newPlatform in new_platforms:
            self.platforms.add(newPlatform)

    def __check_collisions(self):
        # Need impact sounds
        self.__check_platforms()
        # only check for laser collisions if a laser exists
        if len(self.turret.lasers.sprites()) > 0:
            self.__turret_laser_collisions()
        if len(self.player.fireballs.sprites()):
            self.__fireballs_collisions()

    def __blit__sprites(self):
        """
        Blit and update sprites
        """
        self.blit(self.player.image, self.player.rect)
        self.player.update(self.difficulty[self.difficulty_mode][1])
        if self.turret.is_alive:
            self.blit(self.turret.image, self.turret.rect)
            self.turret.update()
        self.turret.lasers.update()
        self.player.fireballs.update()

        for laser in self.turret.lasers:
            self.blit(laser.image, laser.rect)
            if laser.rect.x < -250 or laser.rect.y > self.rect.height:
                self.turret.lasers.remove(laser)

        for fireball in self.player.fireballs:
            self.blit(fireball.image, fireball.rect)
            if fireball.rect.x < -250 or fireball.rect.y > self.rect.height:
                self.player.fireballs.remove(fireball)

    def __blit_environment(self):
        """
        blit test level env
        """
        for platform in self.platforms:
            self.blit(platform.image, platform.rect)

    def __blit_ui(self):
        """
        blit user interface
        """
        for img, rect in self.game_ui.get_ui_components():
            self.blit(img, rect)
        self.game_ui.update(self.player.health_points)

    def game_over(self):
        """ When the player loses """
        super().game_over()
        self.__disable_timers()

    def pause_events(self):
        super().pause_events()
        self.__capture_timers()
        self.__disable_timers()

    def unpause(self):
        """
        Start game timers with the captured time
        """
        super().unpause()
        if self.pfc_capture > 0:
            pygame.time.set_timer(self.player_fire_cooldown, self.pfc_capture, True)
        if self.pd_capture > 0:
            pygame.time.set_timer(self.player_dead, self.pd_capture, True)
        if self.sta_capture > 0:
            pygame.time.set_timer(self.start_turret_attack, self.sta_capture, True)
        if self.difficulty_mode < 1:
            pygame.time.set_timer(self.start, self.s_capture, True)
        elif self.sp_capture > 0:
            pygame.time.set_timer(self.spawn_platform, self.sp_capture, True)
        pygame.time.set_timer(self.difficulty_increase, self.di_capture, True)
        self.pfc_capture = 0
        self.pd_capture = 0
        self.sta_capture = 0
        self.s_capture = 0
        self.sp_capture = 0
        self.di_capture = 0
        self.game_stats.game_active = True
        self.game_stats.game_paused = False
        # TODO: It looks like the timers are still really out of sync and break if you pause often

    def check_level_events(self, event):
        if event.type == pygame.KEYDOWN:
            self.check_keydown_events(event)

        elif event.type == pygame.KEYUP:
            self.check_keyup_events(event)

        elif (
            event.type == pygame.MOUSEBUTTONDOWN
            and self.player.can_fire
            and not (self.player.hit or self.player.dying)
        ):
            self.player_mouse_controller(event)

        elif event.type == pygame.MOUSEBUTTONUP and not self.player.dying:
            self.player.reset_animation()

        else:
            self.check_user_events(event)

    def check_user_events(self, event):
        """ Custom events """
        if event.type == self.start_turret_attack and self.turret.is_alive:
            self.turret.firing = True
            self.turret.create_laser((self.player.rect.centerx, self.player.rect.top))
            pygame.time.set_timer(
                self.start_turret_attack, self.turret.firing_speed, True
            )
            self.sta_capture = pygame.time.get_ticks()

        if event.type == self.player_fire_cooldown:
            self.player.can_fire = True

        if event.type == self.spawn_turret:
            self.__load_turret()

        if event.type == self.player_dead:
            self.game_over()

        # create new platform and set the reset the timer
        if event.type == self.spawn_platform:
            self.__create_new_platform()
            pygame.time.set_timer(
                self.spawn_platform, self.difficulty[self.difficulty_mode][0], True
            )
            self.sp_capture = pygame.time.get_ticks()

        if event.type == self.start:
            pygame.time.set_timer(self.difficulty_increase, 10000)
            self.di_capture = pygame.time.get_ticks()
            self.difficulty_mode += 1
            self.__start_movement()

        if event.type == self.difficulty_increase:
            if self.difficulty_mode < len(self.difficulty) - 1:
                self.difficulty_mode += 1

    def check_keydown_events(self, event):
        """ check for and respond to player keydown input """
        if not self.player.dying:
            if event.key == pygame.K_ESCAPE:
                self.pause_events()
            else:
                # Player movement
                self.player_keydown_controller(event)

    def check_keyup_events(self, event):
        """ Check for and respond to player keyup events """
        if not self.player.dying:
            self.player_keyup_controller(event)

    def update(self):
        """
        Update level elements
        """
        if self.game_stats.game_paused:
            self.pause_menu.update()
            self.blit(self.pause_menu, self.pause_menu.rect)
        else:
            self.check_levelbase_events(self.check_level_events)
            self.__check_collisions()
            self.blit(self.bg_image, self.bg_image_rect)
            self.platforms.update(self.difficulty[self.difficulty_mode][1])
            self.__blit_environment()
            self.__blit__sprites()
            self.__blit_ui()
