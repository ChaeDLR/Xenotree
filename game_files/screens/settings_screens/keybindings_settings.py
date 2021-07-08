import os

from pygame import font, key
from ..menu_base import MenuBase
from ..button import Button

class KeybindSettings(MenuBase):

    def __init__(self, w_h: tuple, stats: object, settings: object, back: any, screen):
        super().__init__(w_h, stats, settings)

        self.main_screen = screen

        self.settings = settings

        self.back_func = back

        self.__load_title()
        self.__load_keybind_labels_buttons()
        self.__load_buttons()

    def __load_buttons(self):
        """
        Create apply and back buttons
        """
        self.back_button = Button(self.main_screen, "Back")
        self.back_button.set_position(self.rect.centerx-(self.back_button.width/2), self.screen_rows * 5)

    def __load_title(self):
        """ load settings title """
        title_font = font.SysFont(None, 56, bold=True)
        self.keybind_menu_img = title_font.render(
            "KEY BINDINGS", True, self.text_color, self.background_color
        )
        self.keybind_menu_img_rect = self.keybind_menu_img.get_rect()
        self.keybind_menu_img_rect.midtop = self.rect.midtop
        self.keybind_menu_img_rect.y += 60

    def __load_keybind_labels_buttons(self):
        """ Labels displaying the different keybindings available to change """
        options_strings = [
            "Move left - ",
            "Move right - ",
            "Jump - ",
            "Dash - ",
            "Cycle fireball type - "
        ]
        positions: dict = {
            "move_left": 0,
            "move_right": 0,
            "jump": 0,
            "dash": 0,
            "cycle_fireball": 0
        }
        self.options_image_dict: dict = {}
        options_font = font.SysFont(None, 24)
        for index, option in enumerate(positions):
            option_image =  options_font.render(
                options_strings[index], True, self.text_color, self.background_color
            )
            option_image_rect = option_image.get_rect()
            positions[option] = (
                (self.rect.centerx-(self.screen_columns), 
                (self.keybind_menu_img_rect.y+self.screen_rows)+((self.screen_rows/2)*index))
                )

            option_image_rect.center = positions[option]
            self.options_image_dict[option] = (
                option_image,
                option_image_rect
            )

        # keybind buttons
        self.keybind_button_dict: dict = {}
        for index, keybind in enumerate(self.settings.key_bindings):
            self.keybind_button_dict[keybind] = Button(
                self.main_screen, key.name(self.settings.key_bindings[keybind]), (75, 30), 20, keybind
                )

            self.keybind_button_dict[keybind].set_position(
                (positions[keybind][0]+(self.screen_columns*2)), 
                positions[keybind][1]-25
                )

    def check_button_up(self, mouse_pos):
        if self.back_button.check_button(mouse_pos, True):
            self.back_func()

    def check_button_down(self, mouse_pos):
        self.back_button.check_button(mouse_pos)

    def update(self):
        self.main_screen.blit(self.keybind_menu_img, self.keybind_menu_img_rect)
        self.back_button.blitme()
        for option in self.options_image_dict:
            self.main_screen.blit(
                self.options_image_dict[option][0], 
                self.options_image_dict[option][1]
                )
        for button in self.keybind_button_dict:
            self.keybind_button_dict[button].blitme()
