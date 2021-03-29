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
        self.main_menu = game_files.MainMenu(
            self.settings.screen_width, self.settings.screen_height
        )
        self.game_over = game_files.Game_Over(
            self.settings.screen_width, self.settings.screen_height
        )
        self.pause_menu = game_files.PauseMenu(
            self.settings.screen_width, self.settings.screen_height
        )
        self.settings_menu = game_files.SettingsMenu(
            self.settings.screen_width, self.settings.screen_height,
            self.game_sound
        )
        
        self.active_screen = self.main_menu

    def run_game(self):
        """ main loop """
        while True:
            self.clock.tick(60)

            if self.stats.game_paused:
                self._check_paused_events()
            elif self.stats.game_active == False:
                self._check_events()

            self._update_screen()

    def _check_paused_events(self):
        """
            Events to check when the game is paused
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_pause_menu_buttons(mouse_pos)

    def _check_events(self):
        """ check for events """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and not self.stats.game_active:
                mouse_pos = pygame.mouse.get_pos()

                if self.stats.game_over:
                    if self.stats.new_high_score:
                        self._check_new_hs_screen_buttons(mouse_pos)
                    else:
                        self._check_game_over_buttons(mouse_pos)

                elif self.stats.settings_menu_active:
                    self._check_settings_menu_buttons(mouse_pos)

                elif self.stats.main_menu_active:
                    self._check_main_menu_buttons(mouse_pos)

    def _check_keydown_events(self, event):
        """ check for and respond to player input """
        if event.key == pygame.K_ESCAPE:
            sys.exit()

    def _start_game(self):
        """ Reset the game """
        self._load_level_one()
        self.stats.set_active_screen(game_active=True)
        self.stats.active_level = 1
        pygame.mouse.set_visible(False)
        pygame.mixer.music.play()

    def _unpause_game(self):
        self.stats.game_active = True
        self.stats.game_paused = False
        self.level_one.resume_game()
        pygame.mouse.set_visible(False)

    def _check_pause_menu_buttons(self, mouse_pos):
        """
            if self.stats.game_paused
        """
        if self.pause_menu.check_buttons(mouse_pos) == 1:
            self._unpause_game()
        elif self.pause_menu.check_buttons(mouse_pos) == 2:
            sys.exit()

    def _check_game_over_buttons(self, mouse_pos):
        """
            self.stats.game_over
        """
        if self.game_over.check_buttons(mouse_pos) == 1:
            self._start_game()
        elif self.game_over.check_buttons(mouse_pos) == 2:
            sys.exit()

    def _check_settings_menu_buttons(self, mouse_pos):
        """
            self.stats.settings_menu_active
        """
        pressed_button = self.settings_menu.check_buttons(mouse_pos)
        if pressed_button == 1:
            self.settings_menu.music_plus_pressed = True
            self.game_sound.increase_music_volume()
            self.settings_menu.update_music_volume_string()
        elif pressed_button == 2:
            self.settings_menu.music_minus_pressed = True
            self.game_sound.decrease_music_volume()
            self.settings_menu.update_music_volume_string()
        elif pressed_button == 3:
            self.settings_menu.effects_plus_pressed = True
            self.game_sound.increase_effects_volume()
            self.settings_menu.update_effects_volume_string()
        elif pressed_button == 4:
            self.settings_menu.effects_minus_pressed = True
            self.game_sound.decrease_effects_volume()
            self.settings_menu.update_effects_volume_string()
        elif pressed_button == 5:
            self.stats.set_active_screen(main_menu=True)
        elif pressed_button == 6:
            self.game_sound.save_volumes()

    def _check_main_menu_buttons(self, mouse_pos):
        """
            self.stats.main_menu_active
        """
        if self.main_menu.check_buttons(mouse_pos) == 1:
            self._start_game()
        elif self.main_menu.check_buttons(mouse_pos) == 2:
            sys.exit()
        elif self.main_menu.check_buttons(mouse_pos) == 3:
            self.stats.set_active_screen(settings_menu=True)

    def _check_new_hs_screen_buttons(self, mouse_pos):
        if self.new_high_score_screen.check_buttons(mouse_pos) == 1:
            self.stats.new_high_score = False
            self._start_game()
        elif self.new_high_score_screen.check_buttons(mouse_pos) == 2:
            sys.exit()

    def _stop_game(self):
        """ Game Over """
        self.stats.game_active = False
        self.stats.game_over = True
        pygame.mouse.set_visible(True)

    def _get_active_level(self):
        """ return the active level """
        if self.stats.active_level == 1:
            return self.level_one
        elif self.stats.active_level == 2:
            self._load_level_two()
            return self.level_two

    def _set_active_screen(self):
        """ Check game bools to choose the active screen """
        if self.stats.lives_left == 0:
            self._stop_game()

        elif self.stats.game_active:
            self.active_screen = self._get_active_level()

        elif not self.stats.game_active and self.stats.game_over:

            if self.stats.new_high_score:
                self.new_high_score_screen.set_high_score_img(
                    self.stats.high_score)
                self.active_screen = self.new_high_score_screen
            else:
                self.active_screen = self.game_over

        elif not self.stats.game_active and self.stats.settings_menu_active:
            self.active_screen = self.settings_menu

        elif not self.stats.game_active and self.stats.main_menu_active:
            self.active_screen = self.main_menu
        
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


if __name__ == '__main__':
    xenotree = Xenotree()
    xenotree.run_game()
