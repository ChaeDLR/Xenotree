from game_files.sprites.player import Player
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
        self.player.set_position((25, self.height - 26))
        self.__load_turret()
        self.__load_custom_events()
        self.turret.firing = True

        self.platform_speed = 2500
        self.turret_spawn_speed = 2500

        # To activate turret
        pygame.time.set_timer(self.start_turret_attack, self.turret.firing_speed)

    def __load_turret(self):
        """
        Load turret and set its position
        """
        # TODO: either put in sprie group or re-pos and switch is_alive
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
            (0, 100),
            (self.width - 50, 175),
            (self.width / 2, 250),
            (200, 375),
            (300, 450),
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
            floor_tile = Platform(
                (floor_width * i, self.height - 25),
                image=floor_image,
                connect_left=True,
                connect_right=True,
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
        self.update_player_animation = pygame.USEREVENT + 8
        self.start_turret_attack = pygame.USEREVENT + 9
        self.player_fire_cooldown = pygame.USEREVENT + 10
        self.spawn_turret = pygame.USEREVENT + 11

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
            mouse_button = pygame.mouse.get_pressed(3)
            # if mouse left clicked
            if mouse_button[0]:
                self.player.create_fireball(
                    event.pos, self.game_ui.active_weapon_bar.element_type
                )

            elif mouse_button[2] and not self.player.defending:
                # if mouse right clicked
                self.player.shield.moving = True
                self.player.start_defend(event.pos)

            pygame.time.set_timer(self.player_fire_cooldown, self.player.cooldown_time)

        elif event.type == pygame.MOUSEBUTTONUP and not self.player.dying:
            self.player.defending = False
            if self.player.jumping:
                self.player.falling = True
            self.player.reset_animation()

        else:
            self.check_user_events(event)

    def check_user_events(self, event):
        # CUSTOM EVENTS
        if event.type == self.start_turret_attack and self.turret.is_alive:
            self.turret.firing = True
            self.turret.create_laser((self.player.rect.centerx, self.player.rect.top))

        if event.type == self.player_fire_cooldown:
            self.player.can_fire = True

        if event.type == self.spawn_turret:
            self.__load_turret()

        if event.type == self.player_dead:
            self.base_game_over()

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

    def __check_platforms(self):
        """
        this method will use logic needed to make the
        climbable platforms work
        """
        if self.player.rect.top > self.rect.bottom:
            self.base_game_over()

        for platform in self.platforms:
            if pygame.sprite.collide_mask(self.player, platform):
                if self.player.dying:
                    self.player.falling = False
                    self.player.rect.bottom = platform.rect.top + 25
                elif (
                    platform.rect.top
                    <= self.player.rect.bottom
                    <= platform.rect.top + 25
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
                    self.player.x = platform.rect.left - self.player.rect.width
                    self.player.rect.x = self.player.x
                    self.player.stop_movement(self.player.moving_left, False)
                elif (
                    platform.rect.right - 20
                    < self.player.rect.left
                    <= platform.rect.right + 1
                    and self.player.moving_left
                ):
                    self.player.x = platform.rect.right + 1
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
        if self.player.defending and pygame.sprite.spritecollide(
            self.player.shield,
            self.turret.lasers,
            True,
            collided=pygame.sprite.collide_mask,
        ):
            # TODO: add laser reflection
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
        if self.player.defending and not self.player.hit:
            self.blit(self.player.shield.image, self.player.shield.rect)
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
