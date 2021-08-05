from pygame import font, key, RLEACCEL
from ..menu_base import MenuBase
from ..button import Button


class KeybindSettings(MenuBase):
    def __init__(self, w_h: tuple, stats: object, settings: object, back: any, screen):
        super().__init__(w_h, stats, settings)

        self.main_screen = screen
        self.settings = settings
        self.back_func = back

        # track the display of the key unavailable message
        self.key_unavailable: bool = False
        self.listening = False
        self.listening_keybind = ""

        self.__load_messages()
        self.__load_keybind_labels_buttons()
        self.buttons: list = self.__load_buttons()

    def __load_messages(self):
        """
        Method that initializes the messages this surface may need to display to the user
        """
        # title text image
        self.keybind_menu_img, self.keybind_menu_img_rect = self.create_text(
            (self.rect.centerx, 60), "KEY BINDINGS"
        )

        # image that tells user we're listening for input
        self.set_keybind_img, self.set_keybind_rect = self.create_text(
            (self.rect.centerx, self.rect.height - 160), "Press key...", textsize=40
        )

        # image that tells user that the key they selected is unavailable
        self.key_unavailable_img, self.key_unavailable_rect = self.create_text(
            (self.rect.centerx, self.rect.height - 160), "Key is unavailable", textsize=40
        )

    def __load_buttons(self):
        """
        Create apply and back buttons
        """
        self.back_button = Button(self.main_screen, "Back")
        self.back_button.set_position(self.screen_columns, self.screen_rows * 5)
        self.reset_button = Button(self.main_screen, "Reset")
        self.reset_button.set_position(self.screen_columns * 4, self.screen_rows * 5)
        return [self.back_button, self.reset_button]

    def __load_keybind_labels_buttons(self):
        """ Labels displaying the different keybindings available to change """
        options_strings = [
            "Move left - ",
            "Move right - ",
            "Jump - ",
            "Dash - ",
            "Cycle fireball type - ",
        ]
        positions: dict = {
            "move_left": 0,
            "move_right": 0,
            "jump": 0,
            "dash": 0,
            "cycle_fireball": 0,
        }
        self.options_image_dict: dict = {}
        options_font = font.SysFont(None, 24)
        for index, option in enumerate(positions):
            option_image = options_font.render(
                options_strings[index], True, self.text_color, self.background_color
            )
            option_image_rect = option_image.get_rect()
            positions[option] = (
                self.rect.centerx - (self.screen_columns),
                (self.keybind_menu_img_rect.y + self.screen_rows)
                + ((self.screen_rows / 2) * index),
            )

            option_image_rect.center = positions[option]
            self.options_image_dict[option] = (option_image, option_image_rect)

        # keybind buttons
        self.keybind_button_dict: dict = {}
        for keybind in self.settings.key_bindings:
            self.keybind_button_dict[keybind] = Button(
                self.main_screen,
                key.name(self.settings.key_bindings[keybind]),
                (75, 30),
                20,
                keybind,
            )

            self.keybind_button_dict[keybind].set_position(
                (positions[keybind][0] + (self.screen_columns * 2)),
                positions[keybind][1] - 25,
            )

    def __reset_keybinds(self):
        self.settings.reset_keybinds()
        for keybind in self.settings.key_bindings:
            self.keybind_button_dict[keybind].set_text(
                key.name(self.settings.key_bindings[keybind]), 20
            )

    def __animate_set_keybind_text(self):
        """
        Blinks the set keybind text by adjusting alpha
        """
        if self.keybind_alpha >= 250:
            self.alpha_switch = -1
        elif self.keybind_alpha <= 200:
            self.alpha_switch = 1

        self.keybind_alpha += 1 * self.alpha_switch
        self.set_keybind_img.set_alpha(self.keybind_alpha * self.alpha_switch, RLEACCEL)

    def check_button_up(self, mouse_pos):
        if self.back_button.check_button(mouse_pos, True):
            self.settings.save_setting(self.settings.key_bindings, "keybinds.json")
            self.back_func()
        elif self.reset_button.check_button(mouse_pos, True):
            self.__reset_keybinds()
            self.listening = False
            self.key_unavailable = False
        else:
            for button in self.buttons:
                button.reset_alpha()
            for kb_button in self.keybind_button_dict.values():
                kb_button.reset_alpha()

        for button in self.keybind_button_dict:
            if self.keybind_button_dict[button].check_button(mouse_pos, True):
                self.listening = True
                self.listening_keybind_button = self.keybind_button_dict[button]
                self.keybind_button_dict[button].clear_text()
                self.keybind_alpha = 200
                self.set_keybind_img.set_alpha(self.keybind_alpha, RLEACCEL)

    def check_button_down(self, mouse_pos):
        self.back_button.check_button(mouse_pos)
        self.reset_button.check_button(mouse_pos)

        for kb_button in self.keybind_button_dict.values():
            kb_button.check_button(mouse_pos)

    def update(self, keydown_event):
        """
        Draw and update
        """
        self.main_screen.blit(self.keybind_menu_img, self.keybind_menu_img_rect)
        self.back_button.blitme()
        self.reset_button.blitme()
        for option in self.options_image_dict:
            self.main_screen.blit(
                self.options_image_dict[option][0], self.options_image_dict[option][1]
            )
        for button in self.keybind_button_dict:
            self.keybind_button_dict[button].blitme()

        if self.listening and keydown_event:
            pressed_key = keydown_event.key
            if not pressed_key in self.settings.key_bindings.values():
                self.keybind_button_dict[self.listening_keybind_button.name].set_text(
                    key.name(pressed_key), 20
                )
                self.listening_keybind_button.reset_alpha()
                # set keybind
                self.settings.key_bindings[self.listening_keybind_button.name] = pressed_key

            else:
                self.keybind_button_dict[self.listening_keybind_button.name].restore_text()
                self.key_unavailable = True
                self.keybind_alpha = 255
            self.listening = False

        elif self.listening:
            self.main_screen.blit(self.set_keybind_img, self.set_keybind_rect)
            self.__animate_set_keybind_text()

        elif not self.listening and self.key_unavailable:
            self.main_screen.blit(self.key_unavailable_img, self.key_unavailable_rect)
            self.keybind_alpha -= 1 + ((255 - self.keybind_alpha) * 0.05)
            if self.keybind_alpha > 0:
                self.key_unavailable_img.set_alpha(self.keybind_alpha)
            else:
                self.key_unavailable = False
