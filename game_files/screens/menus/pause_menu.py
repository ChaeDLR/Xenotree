from pygame import SRCALPHA
from pygame.constants import MOUSEBUTTONDOWN, MOUSEBUTTONUP
from game_files import ScreenBase
from .button import Button


class PauseMenu(ScreenBase):
    def __init__(self, unpause_func):
        super().__init__(flags=SRCALPHA)
        self.background_color = (
            self.background_color[0],
            self.background_color[1],
            self.background_color[2],
            175,
        )
        self.unpause_function = unpause_func
        self.buttons = self.__load_buttons()

        self.text_image, self.text_image_rect = self.create_text(
            (self.rect.centerx, 60), "PAUSED", boldtext=False
        )

    def __load_buttons(self) -> list:
        self.resume_button = Button(self.image, "Resume")
        self.resume_button.convert_alpha()
        self.quit_button = Button(self.image, "Quit")
        self.quit_button.convert_alpha()
        self.resume_button.set_position(y_pos=(self.height / 2))
        return [self.resume_button, self.quit_button]

    def __check_button_down(self, mouse_pos):
        self.resume_button.check_button(mouse_pos)
        self.quit_button.check_button(mouse_pos)

    def __check_button_up(self, mouse_pos):
        if self.resume_button.check_button(mouse_pos, True):
            self.unpause_function()
        elif self.quit_button.check_button(mouse_pos, True):
            ScreenBase.change_screen = True
            ScreenBase.current_screen_key = "main_menu"
        else:
            for button in self.buttons:
                button.reset_alpha()

    def check_events(self, event):
        if event.type == MOUSEBUTTONDOWN:
            self.__check_button_down(event.pos)
        elif event.type == MOUSEBUTTONUP:
            self.__check_button_up(event.pos)

    def update(self):
        self.image.fill(self.background_color)
        self.image.blit(self.text_image, self.text_image_rect)
        self.quit_button.blitme()
        self.resume_button.blitme()
