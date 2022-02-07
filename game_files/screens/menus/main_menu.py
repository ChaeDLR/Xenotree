import sys
import os

from pygame import MOUSEBUTTONDOWN, MOUSEBUTTONUP, mouse, cursors
from game_files import ScreenBase
from .button import Button
from ...asset_manager import AssetManager


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

        path = os.path.join(os.getcwd(), "game_files/screens/menus/images/buttons.png")

        # play=0, settings=1, quit=2
        button_imgs = AssetManager.cut_image(
            path, (2, 4), (200, 125), (10, 20, 10, 10)
        )[:3]

        button_row = self.height / 6
        self.buttons: list = [
            Button(self.image, "", size=(200, 125), image=button_imgs[i], name=name)
            for i, name in enumerate(["play", "settings", "quit"])
        ]
        for i in range(len(self.buttons)):
            self.buttons[i].set_position(y_pos=button_row * (i + 2))

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
                    print("EXE play")
                elif button.name == "settings":
                    print("EXE settings")
                    ScreenBase.change_screen = True
                    ScreenBase.current_screen_key = "settings_menu"
                elif button.name == "quit":
                    print("EXE quit")
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
        for button in self.buttons:
            button.blitme()
