# Chae DeLaRosa
import pygame
import sys
from game_files import Settings, ScreenColors
from game_files import ScreenBase
from game_files import MainMenu, SettingsMenu, GameOver
from game_files import TestLevel


class Xenotree:
    """My first platformer project"""

    def __init__(self):
        """Init game screens, clock, settings, and stats"""
        pygame.init()
        self.window = pygame.display.set_mode(
            (Settings.screen_width, Settings.screen_height),
            flags=pygame.DOUBLEBUF,
        )
        self.window.fill(ScreenColors.bg_color())
        pygame.display.set_caption("Xenotree")
        self.clock = pygame.time.Clock()

        self.screens: dict = {
            "main_menu": MainMenu,
            "settings_menu": SettingsMenu,
            "game_over": GameOver,
            "test_level": TestLevel,
        }

        self.active_screen = MainMenu()

    def __check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            else:
                self.active_screen.check_events(event)

    def __get_active_screen(self):
        """Reassign the active screen"""
        return self.screens[self.active_screen.current_screen_key]()

    def run_game(self):
        """main loop"""
        while True:
            self.clock.tick(60)
            if ScreenBase.change_screen:
                self.active_screen = self.__get_active_screen()
                ScreenBase.change_screen = False
            self.__check_events()
            self.active_screen.update()
            self.window.blit(self.active_screen.image, self.active_screen.rect)

            pygame.display.update()


if __name__ == "__main__":
    xenotree = Xenotree()
    xenotree.run_game()
