from .menu_base import MenuBase
from .button import Button


class PauseMenu(MenuBase):
    def __init__(self, w_h: tuple, stats: object, settings: object, unpause_func):
        super().__init__(w_h, stats, settings)

        self.unpause_function = unpause_func

        self.buttons = self.__load_buttons()
        self.text_image, self.text_image_rect = self.create_text(
            (self.rect.centerx, 60), "PAUSED", boldtext=False
        )

    def __load_buttons(self) -> list:
        self.resume_button = Button(self, "Resume")
        self.quit_button = Button(self, "Quit")
        self.resume_button.set_position(y_pos=(self.height / 2))
        return [self.resume_button, self.quit_button]

    def check_button_down(self, mouse_pos):
        self.resume_button.check_button(mouse_pos)
        self.quit_button.check_button(mouse_pos)

    def check_button_up(self, mouse_pos):
        if self.resume_button.check_button(mouse_pos, True):
            self.unpause_function()
        elif self.quit_button.check_button(mouse_pos, True):
            self.stats.set_active_screen(main_menu=True)
        else:
            for button in self.buttons:
                button.reset_alpha()

    def update(self):
        self.check_base_events(self.check_button_down, self.check_button_up)
        self.fill(self.background_color, self.rect)
        self.blit(self.text_image, self.text_image_rect)
        self.quit_button.blitme()
        self.resume_button.blitme()
