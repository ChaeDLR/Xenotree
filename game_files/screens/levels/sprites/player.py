import pygame

from pygame.sprite import Sprite
from game_files import math
from .fireball import Fireball


class Player(Sprite):
    """player sprite class"""

    movement_speed: float = 5.5
    jumping_velocity: float = -7.5
    falling_velocity: float = 1.0
    falling_speed_limit: float = 12.0
    dashing_speed: float = 13.5

    basic_cooldown: int = 500  # passed to the timer to reset attack available flag
    special_cooldown: int = 750
    health_points: int = 100

    def __init__(self, assets: dict, bound: int):
        super().__init__()

        # the animation variables
        self.animation_index = 0
        self.animation_index_limit = 0
        self.animation_counter = 0

        self.images = assets
        self.image, self.mask = self.images["idle_right"][1]

        self.fireballs = pygame.sprite.Group()
        self.special_fireballs = pygame.sprite.Group()

        #region bool flags
        # movement flags
        self.moving = False  # used in animation code
        self.jumping = False
        self.falling = False
        self.dashing = False
        self.dash_dir_right = False
        # Check which way the player is facing
        self.moving_left = False
        self.moving_right = False
        self.facing_right = True

        self.hit = False
        # dying will start the death animation and stop the users control
        self.dying = False
        # dead will end the game
        self.dead = False
        # track player cooldowns
        self.can_basic = True
        self.can_special = True
        # check that the play still has health points
        self.is_alive = True
        #endregion

        # animation trackers
        self.falling_index: int = 0
        self.death_frame: int = 1
        self.animation_index_limit: int = 3

        self.screen_bound: int = bound
        self.hit_angle: int = 0

        # counters
        self.jump_counter = 0
        self.dash_counter = 0

        self.rect = self.image.get_rect()

        self.y: float = float(self.rect.y)
        self.x: float = float(self.rect.x)

    def __move_left(self):
        """
        Check if the player is alive and in bounds
        """
        if (self.x - self.movement_speed) >= 0:
            self.x -= self.movement_speed
            self.rect.x = self.x
        elif not self.hit:
            self.x = 0
            self.rect.x = self.x

    def __move_right(self):
        """
        Check if the player is alive and in bounds
        """
        if self.rect.right <= self.screen_bound:
            self.x += self.movement_speed
            self.rect.x = self.x

    def __dash(self):
        """
        Player quickly move across the x axis
        """
        if self.dash_dir_right and (self.x + self.dashing_speed) < (
            self.screen_bound + self.rect.width
        ):
            self.x += self.dashing_speed
            self.rect.x = self.x
        elif (self.x - self.dashing_speed) > 0:
            self.x -= self.dashing_speed
            self.rect.x = self.x

        self.dash_counter += 1

        if self.dash_counter >= 10:
            self.dashing = False
            self.falling = True

    def __jump(self):
        """
        Start player jump
        """
        self.falling = False
        self.grounded = False
        self.jumping_velocity += 0.35
        if self.jumping_velocity >= 0:
            self.jumping = False
            self.falling = True

    def __fall(self):
        """
        Make the player fall
        """
        self.rect.y += self.falling_velocity
        if self.falling_velocity < self.falling_speed_limit:
            self.falling_velocity += 0.5

    def __stagger(self):
        """
        Staggered movement
        """
        self.stagger_counter += 1
        if self.stagger_counter >= 8:
            self.hit = False
            self.falling = True

    def start_dash(self):
        """
        Tell player to start dashing and start a counter
        """
        # Capture which way the player is facing when dash is pressed
        self.dash_dir_right = self.facing_right
        self.dashing = True
        self.falling = False
        self.dash_counter = 0

    def set_position(self, x_y: tuple = None, x: int = None, y: int = None):
        """
        x_y: tuple -> (x, y) Sets player position using midbottom
        x: int -> sets players x
        y: int -> sets players y
        """
        if x_y:
            self.rect.midbottom = x_y
        else:
            if x:
                self.rect.x = x
            elif y:
                self.rect.y = y
        self.x, self.y = self.rect.x, self.rect.y

    def create_fireball(self, mouse_pos, element_type: str, special: bool = False):
        """
        get a fireball
        """
        fireball_start_pos: list = [
            self.rect.center[0],
            self.rect.center[1] + 5,
        ]

        if self.facing_left:
            fireball_start_pos[0] -= 10
        elif self.facing_right:
            fireball_start_pos[0] += 10

        directions = math.get_directions(fireball_start_pos, mouse_pos)

        if special:
            key = f"{element_type}_sfb_fire_imgs"
        else:
            key = f"{element_type}_fb_fire_imgs"

        fireball = Fireball(
            self.images[key],
            element_type,
            math.get_angle_to(fireball_start_pos, mouse_pos),
            fireball_start_pos,
            directions,
            special,
        )

        self.fireballs.add(fireball)
        self.can_fire = False

    def stop_movement(self, left: bool, right: bool) -> None:
        """
        Stop the player movement in a given direction
        """
        self.moving_right = right
        self.moving_left = left
        if self.dashing:
            self.dashing = False
            if not self.current_platform.y - (self.rect.height + 3) == self.y:
                self.falling = True

    def reset_player(self):
        """reset player position"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)

    def check_position(self):
        """check that the player position is in bounds"""
        if self.rect.top < 31:
            return True
        else:
            return False

    def start_jump(self, velocity: float = -7.5):
        """
        Start the player jump
        Set jumping to True
        Reset animation
        Reset jump velocity
        """
        if self.jump_counter < 2:
            self.jumping = True
            self.reset_animation
            self.jumping_velocity = velocity
            self.falling_velocity = 1.0
            self.rect.y += self.jumping_velocity
            self.jump_counter += 1

    def damaged(self, angle: int = None):
        """
        Reduce player health and play hit animation
        """
        self.hit_angle = angle
        self.health_points -= 10
        if self.health_points <= 20:
            self.dying = True
            self.falling = True
        self.hit = True
        self.stagger_counter = 0
        self.x, self.y = self.rect.x, self.rect.y

    def on_ground(self, platform):
        """
        Call if the player is on the ground to reset the variables
        Adjust the players position so that they are on top of the platform
        """
        # store the platform that the playe is on so we can check the platform status
        self.current_platform = platform
        self.set_position(y=self.current_platform.y - (self.rect.height + 3))
        self.falling = False
        self.jumping = False
        self.jumping_velocity = -7.5
        self.falling_velocity = 1.0
        self.jump_counter = 0

    def switch_move_left(self, move: bool):
        """
        Set the movement left flag to true
        Reset the animation variables
        """
        self.moving_left = move
        self.moving = move
        self.reset_animation()

    def switch_move_right(self, move: bool):
        """
        Set the movement right flag to true
        Reset the animation variables
        """
        self.moving_right = move
        self.moving = move
        self.reset_animation()

    def reset_animation(self):
        """
        Reset the animation counter and index
        This will typically be used when the player changes animation lists
        """
        self.animation_counter = 0
        self.animation_index = 0

    def update_movement(self):
        """
        Update player position
        """
        if not self.dying:
            if self.hit:
                self.__stagger()
            elif not (self.hit or self.dead):
                if self.dashing:
                    self.__dash()
                if self.jumping:
                    self.__jump()
        if self.falling:
            self.__fall()

    def update_animation(self):
        """
        Update the player animation frame
        """
        if self.facing_right:
            if self.dying:
                key = "death_right"
            elif self.hit:
                key = "hit_right"
            elif self.dashing or self.jumping:
                key = "jump_right"
            elif self.moving:
                key = "walk_right"
            else:
                key = "idle_right"

        elif self.facing_left:
            if self.dying:
                key = "death_left"
            elif self.hit:
                key = "hit_left"
            elif self.dashing or self.jumping:
                key = "jump_left"
            elif self.moving:
                key = "walk_left"
            else:
                key = "idle_left"

        if self.animation_index >= len(self.images[key]):
            if self.dying:
                self.animation_index = len(self.images[key]) - 1
            elif self.hit:
                self.animation_index = len(self.images[key]) - 1
            else:
                self.reset_animation()

        self.image, self.mask = self.images[key][self.animation_index]
        self.animation_counter += 1

        if self.dying:
            if self.animation_counter % 24 == 0:
                self.animation_index += 1
        else:
            if self.animation_counter % 16 == 0:
                self.animation_index += 1

    def update_facing(self):
        """
        Check which way the player should be facing
        update bools if needed
        """
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos[0] < self.rect.center[0]:
            self.facing_left, self.facing_right = True, False
        else:
            self.facing_left, self.facing_right = False, True

    def update(self):
        """
        Update the player image and movement
        """
        if not self.dying:
            self.update_facing()
        self.update_movement()
        self.update_animation()
