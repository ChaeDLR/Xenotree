import pygame
import random

from itertools import chain
from .level_base import LevelBase
from .environment.platform import Platform, Wave
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
        self.__load_turret()
        self.__load_custom_events()

        # has check events in update
        self.pause_menu = PauseMenu(
            (self.settings.screen_width, self.settings.screen_height),
            self.game_stats,
            self.settings,
            self.unpause,
        )

        self.turret.firing = True
        self.turret_spawn_speed: int = 2500
        self.__set_timers()

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
        pygame.time.set_timer(self.player_fire_cooldown, 0)
        pygame.time.set_timer(self.player_dead, 0)

    def __capture_timers(self):
        """
        Capture how much time a timer has waited
        and calculate how much time if left on it
        """
        current_time = pygame.time.get_ticks()

        if not self.player.can_fire:
            self.pfc_timeleft = 1000 - (current_time - self.pfc_capture)
            if self.pfc_timeleft <= 0:
                self.pfc_timeleft = 1

        if self.player.dying:
            self.pd_timeleft = 2000 - (current_time - self.pd_capture)
            if self.pd_timeleft <= 0:
                self.pd_timeleft = 1

        if self.turret.is_alive:
            self.sta_timeleft = self.turret.firing_speed - (
                current_time - self.sta_capture
            )
            if self.sta_timeleft <= 0:
                self.sta_timeleft = 1

        self.di_timeleft = 10000 - (current_time - self.di_capture)
        if self.di_timeleft < -1:
            self.di_timeleft = 1

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
                Platform(
                    pos, images=self.platform_assets["platform_images"], w_h=(96, 36)
                )
            )

    def __load_floor(self):
        """
        Load base floor
        """
        platform_images = self.platform_assets["platform_images"]
        floor_width = platform_images["normal"].get_width()

        # make the floor cover the entire width of the screen
        floor_tile_number = round(self.width / floor_width) - 4
        previous_platform = None
        for i in range(0, floor_tile_number):
            if previous_platform:
                floor_tile = Platform(
                    (floor_width * i, self.height - 25), images=platform_images
                )
                floor_tile.connect_left(previous_platform)
            else:
                floor_tile = Platform(
                    (floor_width * i, self.height - 25), images=platform_images
                )

            previous_platform = floor_tile

            if i == 0:
                self.player.set_position(
                    (floor_tile.rect.midtop[0], floor_tile.rect.midtop[1] - 2)
                )
                self.player.on_ground(floor_tile)
            self.platforms.add(floor_tile)

    def __load_env(self):
        """
        Load initial environment
        and platform lists
        """
        self.platforms = pygame.sprite.Group()
        self.frozen_platforms = pygame.sprite.Group()
        self.waves = pygame.sprite.Group()
        self.__load_floor()
        self.__load_platforms()
        self.__load_waves()

    def __load_custom_events(self):
        """
        Load custom events and their capture variable if they need one
        """
        self.start_turret_attack = pygame.USEREVENT + 9
        self.spawn_turret = pygame.USEREVENT + 10
        self.spawn_platform = pygame.USEREVENT + 11

        self.sta_capture: int = 0
        self.sp_capture: int = 0
        self.s_capture: int = 0
        self.di_capture: int = 0

        self.sta_timeleft: int = 0
        self.sp_timeleft: int = 0
        self.s_timeleft: int = 0
        self.di_timeleft: int = 0
        self.pfc_timeleft: int = 0
        self.pd_timeleft: int = 0

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

        for platform in chain(self.platforms, self.frozen_platforms):

            if pygame.sprite.collide_mask(self.player, platform):
                # check if plater ht a platform jumping or falling (y-axis)
                if self.player.dying:
                    self.player.falling = False
                    self.player.rect.bottom = platform.rect.top + 20
                elif (
                    platform.rect.top
                    <= self.player.rect.bottom
                    <= platform.rect.top + 20
                    and self.player.falling
                ):
                    self.player.on_ground(platform)
                    self.player.rect.bottom = platform.rect.top - 2
                elif (
                    self.player.rect.top <= platform.rect.bottom and self.player.jumping
                ):
                    self.player.jumping = False
                    self.player.falling = True
                # check if player hit a platform moving left or moving right (x-axis)
                if (
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
            # check if player is moving off of a platform
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
            collided_laser := pygame.sprite.spritecollide(
                self.player,
                self.turret.lasers,
                True,
                collided=pygame.sprite.collide_mask,
            )
            or pygame.sprite.collide_mask(self.player, self.turret)
        ):
            if collided_laser:
                angle = collided_laser[0].angle_fired
            else:
                angle = 0
            self.player_collide_hit(angle)
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
        if collide_dict := pygame.sprite.groupcollide(
            self.platforms,
            self.player.fireballs,
            False,
            True,
            collided=pygame.sprite.collide_mask,
        ):
            for collide_items in collide_dict.items():
                coll_fb = collide_items[1][0]
                coll_platform = collide_items[0]
            if coll_fb.type == "blue":
                coll_platform.freeze()
                self.platforms.remove(coll_platform)
                self.frozen_platforms.add(coll_platform)
                if coll_platform.connected_right:
                    self.platforms.remove(coll_platform.connected_right_platform)
                    self.frozen_platforms.add(coll_platform.connected_right_platform)
                if coll_platform.connected_left:
                    self.platforms.remove(coll_platform.connected_left_platform)
                    self.frozen_platforms.add(coll_platform.connected_left_platform)

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
                images=self.platform_assets["platform_images"],
                moving=True,
            )
        ]
        platform_width = new_platforms[0].width

        if random.choice((0, 1)) == 1:  # add a connecting platform
            x_y: tuple = (
                (self.width + (platform_width * len(new_platforms))),
                platform_y,
            )

            self.platform_min_limit = x_y[1] - screen_height_section

            new_platforms.append(
                Platform(
                    x_y,
                    images=self.platform_assets["platform_images"],
                    moving=True,
                )
            )
            new_platforms[0].connect_right(new_platforms[1])

        for newPlatform in new_platforms:
            self.platforms.add(newPlatform)

    def __load_waves(self):
        """
        run the water at the bottom of the screen
        """
        water_rect = self.platform_assets["wave_image"].get_rect()
        wave_width = water_rect.width
        num_of_waves: int = int(self.width / water_rect.width) + 2

        for i in range(num_of_waves, -1, -1):
            new_wave = Wave(
                (wave_width * i, self.height - 20),
                images=self.platform_assets,
            )

            if i == 0:
                Wave.first = new_wave
                new_wave.next = previous_wave
            elif i == num_of_waves:
                Wave.last = new_wave
            else:
                new_wave.next = previous_wave

            previous_wave = new_wave

            self.waves.add(new_wave)

    def __run_water(self):
        """
        Move the waves
        """
        if Wave.first.rect.x < -Wave.first.rect.width:
            # set first waves new position
            Wave.first.set_position(x_pos=(Wave.last.rect.x + Wave.last.rect.width))
            # Set the old lasts next to the new last
            Wave.last.next = Wave.first
            # make the old first the new last
            Wave.last = Wave.first
            # make the new first the old firsts next
            Wave.first = Wave.first.next

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
        self.player.update()
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
        for wave in self.waves:
            self.blit(wave.image, wave.rect)
        for platform in self.platforms:
            self.blit(platform.image, platform.rect)
        for frozen_platform in self.frozen_platforms:
            self.blit(frozen_platform.image, frozen_platform.rect)

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
        self.__capture_timers()
        self.__disable_timers()
        super().pause_events()

    def unpause(self):
        """
        Start game timers with the captured time
        """
        super().unpause()
        if self.pfc_timeleft >= 1:
            pygame.time.set_timer(self.player_fire_cooldown, self.pfc_timeleft, True)
        if self.pd_timeleft >= 1:
            pygame.time.set_timer(self.player_dead, self.pd_timeleft, True)
        if self.sta_timeleft >= 1:
            pygame.time.set_timer(self.start_turret_attack, self.sta_timeleft, True)

        self.player.moving_left, self.player.moving_right, self.player.moving = (
            False,
            False,
            False,
        )
        self.game_stats.game_active = True
        self.game_stats.game_paused = False

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
            self.platforms.update()
            self.frozen_platforms.update()
            self.__run_water()  # Loop the waves
            self.waves.update(4.5)  # wave speed
            self.__blit__sprites()
            self.__blit_environment()
            self.__blit_ui()
