import pygame

from .level_base import LevelBase
from .environment.env import Environment
from .environment.platform import Platforms
from ..screens.screen_colors import ScreenColors
from ..sprites.turret import Turret
from ..screens.pause_menu import PauseMenu
from game_files.game_assets import AssetManager


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

        self.__set_timers()

    def __set_timers(self):
        """Set levels timers"""
        # To activate turret
        # pygame.time.set_timer(self.start_turret_attack, self.turret.firing_speed, True)
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
        width = None
        for i in range(4):
            if not width:
                width: int = self.width
            platform_block: list = Platforms.tile_block(
                (2 * i, 4 * i), (width, 470 - (45 * i))
            )
            width = ((5 * i) * 32) + self.width
            self.platforms.add(platform_block)

    def __load_floor(self):
        """
        Load base floor
        """
        floor_tiles: list = Platforms.tile_block((5, 25), (0, self.height - 100))
        self.player.set_position(
            (floor_tiles[3].rect.midtop[0], floor_tiles[3].rect.midtop[1])
        )
        self.player.on_ground(floor_tiles[3])
        self.platforms.add(floor_tiles)

    def __load_env(self):
        """
        Load initial environment
        and platform lists
        """
        self.background_images = AssetManager.background_assets(
            (self.width, self.height)
        )
        self.env_assets = AssetManager.level_env_assets()
        self.environment = Environment(
            background=self.background_images["background_layers"],
            foreground=self.background_images["foreground_layers"],
            w_h=(self.width, self.height),
            wave_img=self.env_assets["wave_image"],
        )
        self.platforms = pygame.sprite.Group()
        self.frozen_platforms = pygame.sprite.Group()
        self.__load_floor()
        self.__load_platforms()

    def __load_custom_events(self):
        """
        Load custom events and their capture variable if they need one
        """
        self.start_turret_attack = pygame.USEREVENT + 9
        self.spawn_turret = pygame.USEREVENT + 10

        self.sta_capture: int = 0
        self.di_capture: int = 0

        self.sta_timeleft: int = 0
        self.di_timeleft: int = 0
        self.pfc_timeleft: int = 0
        self.pd_timeleft: int = 0

    def __check_platforms(self, platform_group):
        """
        this method will use logic needed to make the
        climbable platforms work
        """
        if self.player.rect.centery > self.environment.get_bottom():
            self.game_over()

        if platform := pygame.sprite.spritecollideany(self.player, platform_group):

            # if the player is dying position them low on the platform
            # while they finish their animation
            if self.player.dying:
                self.player.falling = False
                self.player.rect.bottom = platform.rect.centery
                self.player.y = self.player.rect.y

            # check if plater hit a platform jumping or falling (y-axis)
            if platform.rect.top <= self.player.rect.bottom and self.player.falling:
                self.player.on_ground(platform)
            elif self.player.rect.top <= platform.rect.bottom and self.player.jumping:
                self.player.jumping = False
                self.player.falling = True

            # check if the player has hit the side of a platform moving across the x axis
            if (  # check if the top or the bottom of the platform are in range of the players top or bottom
                self.player.rect.bottom
                > (platform.rect.bottom or platform.rect.top)
                > self.player.rect.top
            ):
                if (  # check if the player hit a platform while moving right
                    self.player.moving_right
                ) or (self.player.dashing and self.player.facing_right):
                    self.player.set_position(
                        x=(platform.rect.left - (self.player.rect.width + 2))
                    )
                    self.player.stop_movement(self.player.moving_left, False)
                elif (  # check if the player hit a platform while moving left
                    self.player.moving_left
                ) or (self.player.dashing and self.player.facing_left):
                    self.player.set_position(x=platform.rect.right + 2)
                    self.player.stop_movement(False, self.player.moving_right)
        # check if player is moving off of a platform
        if (
            self.player.rect.left >= self.player.current_platform.rect.right
        ):  # going off the right side
            if self.player.current_platform.connected_right:
                self.player.current_platform = (
                    self.player.current_platform.connected_right_platform
                )
            else:
                self.player.falling = True
        elif (
            self.player.rect.right <= self.player.current_platform.rect.left
        ):  # going off the left side
            if self.player.current_platform.connected_left:
                self.player.current_platform = (
                    self.player.current_platform.connected_left_platform
                )
            else:
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

    def __check_collisions(self):
        # Need impact sounds
        self.__check_platforms(self.platforms)
        self.__check_platforms(self.frozen_platforms)
        # only check for laser collisions if a laser exists
        if len(self.turret.lasers.sprites()) > 0:
            self.__turret_laser_collisions()
        if len(self.player.fireballs.sprites()):
            self.__fireballs_collisions()

    def __blit__sprites(self):
        """
        Blit and update sprites
        player, enemies, & projectiles
        """
        self.player.fireballs.update()
        self.player.update()
        self.blit(self.player.image, self.player.rect)

        if self.turret.is_alive:
            self.blit(self.turret.image, self.turret.rect)
            self.turret.update()
        self.turret.lasers.update()

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
        blit test level environment
        place sprites bliting inbetween the background and foreground
        """
        # a layer groups images instance variable is a tuple containing (image, rect)
        for layerGroup in self.environment.bg_layers:
            self.blits(layerGroup.images)
        self.__blit__sprites()
        for platform in self.platforms:
            self.blit(platform.image, platform.rect)
        for layerGroup in self.environment.fg_layers:
            self.blits(layerGroup.images)

    def __blit_ui(self):
        """
        blit user interface
        """
        for img, rect in self.game_ui.get_ui_components():
            self.blit(img, rect)
        self.game_ui.update(self.player.health_points)

    def __update_environment(self):
        """Update level's env and scroll"""
        scroll_x, scroll_y = 0.0, 0.0
        if not self.player.dying:
            if self.player.moving_left:
                scroll_x = self.player.movement_speed
            elif self.player.moving_right:
                scroll_x = self.player.movement_speed * -1

        if self.player.jumping:
            scroll_y = self.player.jumping_velocity * -1
        elif self.player.falling:
            scroll_y = self.player.falling_velocity * -1

        player_scroll_values: list = [0.0, 0.0]
        # adjust game objects x values
        if not self.player.rect.centerx in range(
            self.rect.centerx - 5, self.rect.centerx + 5
        ):
            player_scroll_values[0] = float(
                (self.rect.centerx - self.player.rect.centerx) / 5
            )
            self.player.x += player_scroll_values[0]
            self.player.rect.x = int(self.player.x)
        scroll_x += player_scroll_values[0]
        # adjust game objects y values
        if not self.player.rect.centery in range(
            self.rect.centery + 125, self.rect.centery + 126
        ):
            player_scroll_values[1] = float(
                (self.rect.centery + 126 - self.player.rect.centery) / 5
            )
            self.player.y += player_scroll_values[1]
            self.player.rect.y = int(self.player.y)
        scroll_y += player_scroll_values[1]
        self.platforms.update(scroll_x, scroll_y)
        self.environment.scroll(scroll_x, scroll_y)

    def game_over(self):
        """When the player loses"""
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
        """Custom events"""
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
        """check for and respond to player keydown input"""
        if not self.player.dying:
            if event.key == pygame.K_ESCAPE:
                self.pause_events()
            else:
                # Player movement
                self.player_keydown_controller(event)

    def check_keyup_events(self, event):
        """Check for and respond to player keyup events"""
        if not self.player.dying:
            self.player_keyup_controller(event)

    def update(self):
        """
        Update level elements
        """
        if self.game_stats.game_paused:
            # checks its own pygame event loop
            self.pause_menu.update()
            self.blit(
                self.pause_menu,
                self.pause_menu.rect,
                special_flags=pygame.BLEND_RGBA_MAX,
            )
        else:
            self.check_levelbase_events(self.check_level_events)
            self.__update_environment()
            self.__check_collisions()
            self.__blit_environment()
            self.__blit_ui()
