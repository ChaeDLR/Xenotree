import pygame
from ..game_ui import Game_Ui
from ..sprites import Player


class LevelBase(pygame.Surface):
    """
        Base level class that will hold
        all of the basic code needed for a level
    """

    def __init__(
        self, width: int, height: int, settings: object, stats: object, game_sound: object
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

        self.load_player()

    def load_player(self):
        """ load the sprites needed for the level """
        self.player = Player(self)
    
    def load_base_custom_events(self):
        """ custom events that are the same in every level """
        self.player_hit = pygame.USEREVENT+5
        self.unpause_game = pygame.USEREVENT+6
    
    def check_keydown_events(self, event):
        """ check for and respond to player keydown input """
        if event.key == pygame.K_ESCAPE:
            self.pause_events()
        elif event.key == pygame.K_UP:
            self.game_sound.player_movement_sound.play()
            self.player.move_forward()
        elif event.key == pygame.K_DOWN:
            self.game_sound.player_movement_sound.play()
            self.player.move_backward()
        elif event.key == pygame.K_LEFT:
            self.player.move_left()
        elif event.key == pygame.K_RIGHT:
            self.player.move_right()

    def check_keyup_events(self, event):
        """ Check for and respond to player keyup events """
        if event.key == pygame.K_LEFT:
            self.player.moving_left = False
        elif event.key == pygame.K_RIGHT:
            self.player.moving_right = False

    def pause_events(self):
        self.game_stats.game_paused = True
        self.game_stats.game_active = False
        pygame.mixer.music.pause()
        pygame.mouse.set_visible(True)
        pygame.event.wait(self.unpause_game)

    def resume_game(self):
        """ Method call to set a timer that sets off the unpause_game custom event """
        pygame.time.set_timer(self.unpause_game, 1, True)

    def player_collide_hit(self):
        """
            If the player collides with something that hurts it
        """
        if self.player.player_hit == False:
            self.game_sound.player_impact_sound.play()
        self.player.player_hit = True
        pygame.time.set_timer(self.player_hit, 500, True)
    
    
    def base_game_over(self):
        """ Reset the current level """
        self.game_stats.set_high_score()
        self.game_stats.reset_stats()
        self.game_stats.active_level = 0
        self.game_stats.set_active_screen(game_over=True)
        pygame.mixer.music.stop()
        pygame.mouse.set_visible(True)

    def update_ui(self):
        """ Update everything in the player ui """
        self.game_ui.update_level()
        self.game_ui.update_lives()
        self.game_ui.display_ui()