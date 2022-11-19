# Chae DeLaRosa
import pygame
import sys

from game_files import *


class Xenotree:
    """My first platformer project"""

    def __init__(self):
        """Init game screens, clock, settings, and stats"""
        pygame.init()
        self.window = pygame.display.set_mode(
            (Settings.screen_width, Settings.screen_height),
            flags=pygame.DOUBLEBUF | pygame.SCALED,
        )

        self.window.fill(colors.BLACK)
        pygame.display.set_caption("Xenotree")
        self.clock = pygame.time.Clock()

        self.screens: dict = {
            "main_menu": MainMenu,
            "settings_menu": SettingsMenu,
            "game_over": GameOver,
            "test_level": TestLevel,
        }

        self.active_screen = MainMenu()

    def run_game(self):
        """main loop"""
        while True:
            self.clock.tick(60)

            if ScreenBase.change_screen:
                self.active_screen = self.screens[
                    self.active_screen.current_screen_key
                ]()
                ScreenBase.change_screen = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                else:
                    self.active_screen.check_events(event)

            self.active_screen.update()
            self.window.blit(self.active_screen.image, self.active_screen.rect)

            pygame.display.update()


if __name__ == "__main__":
    xenotree = Xenotree()
    xenotree.run_game()
