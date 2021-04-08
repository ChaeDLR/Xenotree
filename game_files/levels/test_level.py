import pygame
from .level_base import LevelBase
from .environment.wall import Wall
from ..screens.screen_colors import ScreenColors


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

        self.colors = ScreenColors()
        self._load_floor(width, height)
        self.player.rect.midbottom = self.floor.rect.midtop

    def _load_floor(self, level_w: int, level_h: int):
        self.floor = Wall((level_w, 25), (0, level_h - 25))

    def _load_custom_events(self):
        self.update_player_animation = pygame.USEREVENT + 7
    
    def check_level_events(self, event):
        if event.type == pygame.KEYDOWN:
            self.check_keydown_events(event)
        elif event.type == pygame.KEYUP:
            self.check_keyup_events(event)
    
    def check_keydown_events(self, event):
        """ check for and respond to player keydown input """
        if event.key == pygame.K_ESCAPE:
            self.pause_events()
        # Player movement keys
        # call movement switch and pass true to make the player
        # movement flags True
        elif event.key == pygame.K_a:
            self.player.switch_move_left(True)
        elif event.key == pygame.K_d:
            self.player.switch_move_right(True)
        # check for player jump input
        if event.key == pygame.K_SPACE:
            self.player.jump(True)

    def check_keyup_events(self, event):
        """ Check for and respond to player keyup events """
        if event.key == pygame.K_a:
            self.player.switch_move_left(False)
        elif event.key == pygame.K_d:
            self.player.switch_move_right(False)
        # player jumping
        if event.key == pygame.K_SPACE:
            self.player.jump(False)

    def update(self):
        """
        Update level elements
        """
        self.check_levelbase_events(self.check_level_events)
        self.fill(self.colors.level_one_bg, self.rect)
        self.blit(self.floor.image, self.floor.rect)
        self.blit(self.player.image, self.player.rect)
        self.player.update()

        # Quick inital gravity code
        if self.player.rect.bottom < self.floor.rect.top:
            self.player.rect.y += 1
