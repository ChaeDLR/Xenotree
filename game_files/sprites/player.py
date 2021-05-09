import pygame
import os
from pygame.sprite import Sprite
from ..utils.spritesheet import SpriteSheet


class Player(Sprite):
    """ player sprite class """

    def __init__(self, level_rect):
        super().__init__()
        self.screen_rect = level_rect
        self.screen_rows = self.screen_rect.bottom / 14

        self.__create_animation_variables()
        self._load_player_images()

        # create players bool values
        self.__player_bools()
        self.falling_index: int = 0
        self.death_frame: int = 1

        self.rect = self.image.get_rect()

        self.movement_speed: float = 6.0
        self.jumping_velocity: float = -7.5
        self.falling_velocity: float = 7.5

        self.cooldown_time: int = 1500

        # set player initial position
        self.rect.midbottom = self.screen_rect.midbottom
        self.y: float = float(self.rect.y)
        self.x: float = float(self.rect.x)

    def __player_bools(self):
        """
        bool values the player needs
        """
        self.moving_left = False
        self.moving_right = False
        self.moving = False
        # This bool will be used to choose which idle animation to play
        self.facing_right = True
        self.player_hit = False
        self.jumping = False
        self.falling = False
        # track player attack cooldown
        self.can_fire = True
        self.is_alive = True

    def __create_animation_variables(self) -> None:
        """ These are the animation variables needed to animate the player smoothly """
        self.animation_index = 0
        self.animation_index_limit = 0
        self.animation_counter = 0

    def _ss_idle_coords(self) -> list:
        """ Rect positions and sizes needed to cut the sprite sheet for the idle images """
        idle: list = [
            # (8, 1, 21, 30), Animation looks a lot smoother without this image
            (40, 0, 21, 30),
            (72, 0, 24, 30),
            (100, 1, 25, 30),
            (133, 2, 24, 30),
        ]
        return idle

    def _ss_walk_coords(self) -> list:
        """ Rect positions and sizes needed to cut the sprite sheet for walking images """
        walk: list = [
            (2, 32, 28, 30),
            (35, 33, 28, 30),
            (67, 34, 28, 30),
            (98, 34, 28, 30),
        ]
        return walk

    def _ss_jump_coords(self) -> list:
        """ Rect positions and sizes for jump animations """
        jump: list = [
            (2, 65, 28, 27),
            (33, 66, 30, 27),
            (65, 66, 30, 26),
            (98, 66, 28, 27),
        ]
        return jump

    def _load_player_images(self) -> None:
        """ Load player image from assets folder """
        p_colorkey = (0, 0, 0)
        # set player image
        current_path = os.path.dirname(__file__)
        player_ss_path = os.path.join(
            current_path, "sprite_assets/player_assets/MageSpriteSheet.png"
        )
        ss_tool = SpriteSheet(player_ss_path)

        # nested funcs to break the code up a bit
        def idle_animations():
            self.idle_right_images = []
            idle_coords = self._ss_idle_coords()
            for coord in idle_coords:
                image = ss_tool.image_at(coord, p_colorkey)
                image = pygame.transform.scale(image, (41, 54))
                self.idle_right_images.append(image)
            self.animation_index_limit = len(self.idle_right_images) - 1

            self.idle_left_images = self.idle_right_images[:]
            for i in range(0, len(self.idle_right_images)):
                self.idle_left_images[i] = pygame.transform.flip(
                    self.idle_left_images[i], True, False
                )

        def walk_animations():
            # walking right images
            self.walk_right_images = []
            walk_coords = self._ss_walk_coords()
            for coord in walk_coords:
                image = ss_tool.image_at(coord, p_colorkey)
                image = pygame.transform.scale(image, (41, 54))
                self.walk_right_images.append(image)

            # walking left images
            self.walk_left_images = self.walk_right_images[:]
            for i in range(0, len(self.walk_right_images)):
                self.walk_left_images[i] = pygame.transform.flip(
                    self.walk_left_images[i], True, False
                )

        def jump_animations():
            self.jump_right_images = []
            jump_coords = self._ss_jump_coords()
            for coord in jump_coords:
                image = ss_tool.image_at(coord, p_colorkey)
                image = pygame.transform.scale(image, (41, 54))
                self.jump_right_images.append(image)

            self.jump_left_images = self.jump_right_images[:]
            for i in range(0, len(self.jump_right_images)):
                self.jump_left_images[i] = pygame.transform.flip(
                    self.jump_left_images[i], True, False
                )

        # create image lists and set the limit to idle list
        idle_animations()
        walk_animations()
        jump_animations()
        self.animation_index_limit = len(self.idle_right_images) - 1
        self.image = self.idle_right_images[0]

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

    def __move_left(self):
        """
        Check if the player is alive and in bounds
        """
        if not self.player_hit and (self.x - self.movement_speed) >= 0:
            self.x -= self.movement_speed
            self.rect.x = self.x
        elif not self.player_hit:
            self.x = 0
            self.rect.x = self.x

    def __move_right(self):
        """
        Check if the player is alive and in bounds
        """
        if (
            not self.player_hit
            and (self.rect.right + self.movement_speed) <= self.screen_rect.right
        ):
            self.x += self.movement_speed
            self.rect.x = self.x
        elif not self.player_hit:
            self.rect.right = self.screen_rect.right

    def start_jump(self, velocity: float = -7.5):
        """
        Start the player jump
        Set jumping to True
        Reset animation
        Reset jump velocity
        """
        self.jumping = True
        self.reset_animation
        self.jumping_velocity = velocity
        self.rect.y += self.jumping_velocity

    def __jump(self):
        """
        Start player jump
        """
        self.rect.y += self.jumping_velocity
        self.jumping_velocity += 0.5

    def __fall(self):
        """
        Make the player fall
        """
        self.rect.y += self.falling_velocity
        self.falling_velocity += 0.5

    def on_ground(self):
        """
        Call if the player is on the ground to reset the variables
        """
        self.falling = False
        self.jumping = False
        self.falling_velocity = 0

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
        if self.moving_right:
            self.__move_right()
        elif self.moving_left:
            self.__move_left()
        if self.jumping:
            self.__jump()
        elif self.falling:
            self.__fall()

    def update_animation(self):
        """
        Update the player animation frame
        """
        # check if the animation is the last in the list
        if self.animation_index > self.animation_index_limit:
            self.reset_animation()

        if self.jumping and self.facing_right:
            if self.animation_index >= len(self.jump_right_images) - 1:
                self.reset_animation()
            self.image = self.jump_right_images[self.animation_index]

        elif self.jumping and not self.facing_right:
            if self.animation_index >= len(self.jump_left_images) - 1:
                self.reset_animation()
            self.image = self.jump_left_images[self.animation_index]

        elif self.facing_right and self.moving:
            if self.animation_index >= len(self.walk_right_images) - 1:
                self.reset_animation()
            self.image = self.walk_right_images[self.animation_index]

        elif self.facing_left:
            if self.animation_index >= len(self.walk_left_images) - 1:
                self.reset_animation()
            self.image = self.walk_left_images[self.animation_index]

        elif not self.facing_right:
            self.image = self.idle_left_images[self.animation_index]

        else:
            self.image = self.idle_right_images[self.animation_index]

        self.animation_counter += 1

        if self.animation_counter % 16 == 0:
            self.animation_index += 1
    
    def update_facing(self):
        """
        Check which way the player should be facing
        update bools if needed
        """
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos[0] < self.rect.center[0]:
            self.facing_left = True
            self.facing_right = False
        else:
            self.facing_left = False
            self.facing_right = True

    def update(self):
        """
        Update the player image and movement
        """
        self.update_facing()
        self.update_animation()
        self.update_movement()
