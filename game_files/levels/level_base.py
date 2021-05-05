import pygame
import sys
import os

from abc import ABC, abstractmethod
from ..game_ui import Game_Ui
from ..sprites.player import Player
from ..sprites.fireball import Fireball


class LevelBase(pygame.Surface, ABC):
    """
    Base level class that will hold
    all of the basic code needed for a level
    """

    def __init__(
        self,
        width: int,
        height: int,
        settings: object,
        stats: object,
        game_sound: object,
    ):
        super().__init__((width, height))

        self.rect = pygame.Rect(0, 0, width, height)
        self.width, self.height = width, height

        self.settings = settings
        self.game_sound = game_sound
        self.game_stats = stats
        self.game_ui = Game_Ui(self, settings, self.game_stats)

        self.difficulty_tracker = 1
        self.patroller_difficulty = 0

        self.__load_base_custom_events()
        self.__load_player()
        self.__load_background()

    def __load_background(self):
        """
        Load levels background image
        """
        path = os.path.dirname(__file__)
        # 256px by 300px
        bg_path = os.path.join(
            path, "environment/env_assets/exterior-parallaxBG1.png"
        )
        self.bg_image = pygame.image.load(bg_path)
        self.bg_image = pygame.transform.scale(self.bg_image, (self.width, self.height))
        self.bg_image_rect = self.bg_image.get_rect()
        self.bg_image_rect.center = self.rect.center

    def __load_player(self):
        """ load the sprites needed for the level """
        self.player = Player(self.rect)
        self.idle_fireball = Fireball((0, 0), (0, 0))

    def __load_base_custom_events(self):
        """ custom events that are the same in every level """
        self.player_hit = pygame.USEREVENT + 5
        self.unpause_game = pygame.USEREVENT + 6

    def check_levelbase_events(self, level_event_check):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == self.player_hit:
                self.base_game_over()
            else:
                level_event_check(event)

    def player_keydown_controller(self, event):
        """ Take event to control the player """
        if event.key == pygame.K_a:
            self.player.switch_move_left(True)
        elif event.key == pygame.K_d:
            self.player.switch_move_right(True)
        # check for player jump input
        if event.key == pygame.K_SPACE and self.player.rect.top >= 0:  # and not self.player.jumping:
            self.player.start_jump()

    def player_keyup_controller(self, event):
        """ Take event to control the player """
        if event.key == pygame.K_a:
            self.player.switch_move_left(False)
        elif event.key == pygame.K_d:
            self.player.switch_move_right(False)

    def pause_events(self):
        self.game_stats.game_paused = True
        self.game_stats.game_active = False
        pygame.mixer.music.pause()
        pygame.mouse.set_cursor(pygame.cursors.arrow)
        #pygame.mouse.set_visible(True)
        # pygame.event.wait(self.unpause_game)

    def resume_game(self):
        """ Method call to set a timer that sets off the unpause_game custom event """
        pygame.time.set_timer(self.unpause_game, 1, True)
        pygame.mouse.set_cursor(pygame.cursors.broken_x)

    def player_collide_hit(self):
        """
        If the player collides with something that hurts it
        """
        # TODO: Need player sound
        # if self.player.player_hit == False:
        #   self.game_sound.player_impact_sound.play()
        self.player.player_hit = True
        pygame.time.set_timer(self.player_hit, 1, True)

    def base_game_over(self):
        """ Reset the current level """
        self.game_stats.set_high_score()
        self.game_stats.reset_stats()
        self.game_stats.active_level = 0
        self.game_stats.set_active_screen(game_over=True)
        pygame.mixer.music.stop()
        pygame.mouse.set_cursor(pygame.cursors.arrow)

    def update_ui(self):
        """ Update everything in the player ui """
        self.game_ui.update_ui()

    def update_background(self):
        """
        Update the levela background image
        """
        pass

    @abstractmethod
    def update(self):
        """
        Each level needs an update method that with contain all of blits for it
        This method is called from the main game loop
        """
        pass
