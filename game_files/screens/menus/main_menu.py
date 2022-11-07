import sys

from os import getcwd, path
from pygame import MOUSEBUTTONDOWN, MOUSEBUTTONUP, mouse, cursors, mixer
from game_files import ScreenBase


class MainMenu(ScreenBase):
    """
    Initial screen that allows user options to
    Play the game, Enter settings menu, or Quit the game
    """

    def __init__(self):
        super().__init__()
        self.main_menu_img, self.main_menu_img_rect = self.create_text(
            (self.rect.centerx, 60), "XENOTREE"
        )

        self.buttons = self.create_buttons(["play", "settings", "quit"])

        if not mixer.music.get_busy():
            mixer.music.load(filename=path.join(getcwd(), "assets/greentop.wav"))
            mixer.music.play(loops=-1)

    def __start_game(self):
        ScreenBase.change_screen = True
        ScreenBase.current_screen_key = "test_level"
        mouse.set_cursor(cursors.broken_x)

    def check_button_down(self, mouse_pos):
        """
        Respond to button clicks mouse down events
        """
        for button in self.buttons:
            button.check_button(mouse_pos)

    def check_button_up(self, mouse_pos):
        """
        Respond to button clicks mouse ip events
        """
        for button in self.buttons:
            if button.check_button(mouse_pos, True):
                if button.name == "play":
                    self.__start_game()
                elif button.name == "settings":
                    ScreenBase.change_screen = True
                    ScreenBase.current_screen_key = "settings_menu"
                elif button.name == "quit":
                    sys.exit()
            else:
                for button in self.buttons:
                    button.reset_alpha()

    def check_events(self, event):
        if event.type == MOUSEBUTTONDOWN:
            self.check_button_down(event.pos)
        elif event.type == MOUSEBUTTONUP:
            self.check_button_up(event.pos)

    def update(self):
        self.image.fill(self.background_color, self.rect)
        self.image.blit(self.main_menu_img, self.main_menu_img_rect)
        self.image.blits([(button.image, button.rect) for button in self.buttons])
