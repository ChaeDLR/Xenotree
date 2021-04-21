# Chae DeLaRosa
import pygame
import sys
import game_files


class Xenotree:
    """ Wizard puzzle game """

    def __init__(self):
        """ Init game screens, clock, settings, and stats """
        pygame.init()
        self.settings = game_files.Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption("Xenotree")
        self.clock = pygame.time.Clock()
        self.stats = game_files.GameStats()
        self.game_sound = game_files.GameSound()

        self._load_game_screens()

    def _load_game_screens(self):
        """ Load starting game screens and set the current screen to the main menu """

        # has check events in update
        self.main_menu = game_files.MainMenu(
            (self.settings.screen_width, self.settings.screen_height),
            self.stats,
            self.settings,
        )

        self.game_over = game_files.Game_Over(
            (self.settings.screen_width, self.settings.screen_height),
            self.stats,
            self.settings,
        )

        # has check events in update
        self.pause_menu = game_files.PauseMenu(
            (self.settings.screen_width, self.settings.screen_height),
            self.stats,
            self.settings,
        )
        # has check events in update
        self.settings_menu = game_files.SettingsMenu(
            (self.settings.screen_width, self.settings.screen_height),
            self.stats,
            self.settings,
            self.game_sound,
        )
        # Create the test level
        self.test_level = game_files.TestLevel(
            self.settings.screen_width,
            self.settings.screen_height,
            self.settings,
            self.stats,
            self.game_sound,
        )

        self.active_screen = self.main_menu

    def run_game(self):
        """ main loop """
        while True:
            self.clock.tick(60)
            self._update_screen()

    def _stop_game(self):
        """ Game Over """
        self.stats.game_active = False
        self.stats.game_over = True
        pygame.mouse.set_visible(True)

    def _get_active_level(self):
        """ return the active level """
        if self.stats.active_level == 1:
            return self.test_level

    def _set_active_screen(self):
        """ Check game bools to choose the active screen """
        # Else if the game is active we need to get the active level
        if self.stats.game_active:
            self.active_screen = self._get_active_level()
        # Else if the game is not active we need to know which menu screen we should show
        elif not self.stats.game_active:
            # if its the game over screen
            if self.stats.game_over:
                self.active_screen = self.game_over
            # Else if the user clicked on the settings menu button we should show that
            elif self.stats.settings_menu_active:
                self.active_screen = self.settings_menu
            # Else if the user is trying to return to the main menu
            elif self.stats.main_menu_active:
                self.active_screen = self.main_menu
        # We no longer want to change the screen after this code is run
        # So switch the bool to False so the loop doesn't trying grabbing a new screen again
        self.stats.change_screen = False

    def _update_screen(self):
        """ things to be updated """
        if self.stats.change_screen:
            self._set_active_screen()

        if not self.stats.game_paused:
            self.screen.fill(self.settings.bg_color)
            self.active_screen.update()
            self.screen.blit(self.active_screen, self.active_screen.rect)
        else:
            self.pause_menu.update()
            self.screen.blit(self.pause_menu, self.pause_menu.rect)
        pygame.display.update()


if __name__ == "__main__":
    xenotree = Xenotree()
    xenotree.run_game()
