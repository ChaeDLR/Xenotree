import pygame

from pygame.sprite import Sprite
from ..utils.game_math import GameMath
from .fireball import Fireball


class Player(Sprite):
    """ player sprite class """

    def __init__(self, assets: dict, bound: int):
        super().__init__()

        self.__create_animation_variables()
        self.images = assets
        self.image, self.mask = self.images["idle_right"][1]
        self.__load_sprites()

        # create players bool values
        self.__player_bools()
        self.falling_index: int = 0
        self.death_frame: int = 1
        self.animation_index_limit: int = 3
        self.screen_bound: int = bound

        # counters
        self.jump_counter = 0
        self.dash_counter = 0

        self.rect = self.image.get_rect()

        self.movement_speed: float = 5.5
        self.jumping_velocity: float = -7.5
        self.falling_velocity: float = 1.0
        self.falling_speed_limit: float = 12.0
        self.dashing_speed: float = 13.5

        # int passed to the pygame timer used to reset attack available flag
        self.cooldown_time: int = 1000
        self.health_points: int = 100

        self.y: float = float(self.rect.y)
        self.x: float = float(self.rect.x)

        # TESTING SWITCH
        self.testing = False

    def __load_sprites(self):
        """
        Load the players shield sprite and fireball group
        """
        self.fireballs = pygame.sprite.Group()

    def __player_bools(self) -> None:
        """
        bool values the player needs
        """
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
        self.can_fire = True
        # check that the play still has health points
        self.is_alive = True
        # If the player has their shield up
        self.defending = False

    def __create_animation_variables(self) -> None:
        """ These are the animation variables needed to animate the player smoothly """
        self.animation_index = 0
        self.animation_index_limit = 0
        self.animation_counter = 0

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
        if self.dash_dir_right and (self.x + self.dashing_speed) < (self.screen_bound + self.rect.width):
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
        self.rect.y += self.jumping_velocity
        if self.jumping_velocity < self.falling_speed_limit:
            self.jumping_velocity += 0.5

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
        
        if self.facing_right:
            self.x -= 3.0
        else:
            self.x += 3.0
        self.y -= 1.5
        self.rect.x, self.rect.y = self.x, self.y

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

    def set_position(self, x_y: tuple):
        """
        set player position using midbottom
        the players feet
        """
        self.rect.midbottom = x_y
        self.x, self.y = self.rect.x, self.rect.y

    def create_fireball(self, mouse_pos, type: str):
        """
        get a fireball
        """
        fireball_start_pos: list = [
            self.rect.center[0],
            self.rect.center[1] + 5,
        ]
        # set the x-axis offset of the fireball spawn position based on which way the player is facing
        if self.facing_left:
            fireball_start_pos[0] -= 10
        elif self.facing_right:
            fireball_start_pos[0] += 10

        directions = GameMath.get_directions(fireball_start_pos, mouse_pos)

        fireball = Fireball(self.images, type)
        fireball.set_start(fireball_start_pos, directions)

        angle = GameMath.get_angle_to(fireball_start_pos, mouse_pos)
        fireball.rotate_image(angle)
        fireball.update_rect()
        self.fireballs.add(fireball)

    def stop_movement(self, left: bool, right: bool) -> None:
        """
        Stop the player movement in a given direction
        """
        self.moving_right = right
        self.moving_left = left

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
            self.rect.y += self.jumping_velocity
            self.jump_counter += 1

    def start_defend(self, mouse_pos: tuple):
        """
        Activate shield and start defending
        """

        if self.facing_right:
            self.image, self.mask = self.images["jump_right"][2]
        elif self.facing_left:
            self.image, self.mask = self.images["jump_left"][2]

        directions = GameMath.get_directions(self.rect.center, mouse_pos)

        self.distance_limit = (
            directions[0] * 20 + self.rect.centerx,
            directions[1] * 20 + self.rect.centery,
        )

        self.shield.set_start(self.rect.center, directions)

        angle = GameMath.get_angle_to(self.rect.center, mouse_pos)

        self.shield.rotate_image(angle)
        self.shield.update_rect()
        self.can_fire = False
        self.defending = True

    def damaged(self):
        """
        Reduce player health and play hit animation
        """
        self.health_points -= 10
        if self.health_points <= 20:
            self.dying = True
            self.falling = True

        self.defending = False
        self.hit = True
        self.stagger_counter = 0
        self.x, self.y = self.rect.x, self.rect.y

    def on_ground(self):
        """
        Call if the player is on the ground to reset the variables
        """
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

    def update_movement(self, platform_speed: int):
        """
        Update player position
        """
        if not self.jumping and not self.falling:
            self.x -= platform_speed
            self.rect.x = self.x
        if not self.dying:
            if self.hit:
                self.__stagger()
            elif not (self.hit or self.dead):
                if self.dashing:
                    self.__dash()
                elif self.moving_right:
                    self.__move_right()
                elif self.moving_left:
                    self.__move_left()
                if self.jumping:
                    self.__jump()
        if self.falling:
            self.__fall()

    def update_animation(self):
        """
        Update the player animation frame
        """
        if self.testing:
            # place any images i want to test here and switch bool to True
            pass

        elif self.facing_right:
            if self.dying:
                key = "death_right"
            elif self.hit:
                key = "hit_right"
            elif self.defending:
                key = "idle_right"
                self.animation_index = 1
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
            elif self.defending:
                key = "idle_left"
                self.animation_index = 1
            elif self.dashing or self.jumping:
                key = "jump_left"
            elif self.moving:
                key = "walk_left"
            else:
                key = "idle_left"

        if self.animation_index >= len(self.images[key]):
            if self.dying:
                self.animation_index = len(self.images[key])-1
            elif self.hit:
                self.animation_index = len(self.images[key])-1
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

    def update(self, platform_speed: int):
        """
        Update the player image and movement
        """
        if not self.dying:
            self.update_facing()
        self.update_movement(platform_speed)
        self.update_animation()