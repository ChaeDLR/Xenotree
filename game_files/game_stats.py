

class GameStats:
    """ track and control game stats """

    def __init__(self):
        """ Initialize game stats """
        self.game_active = False

        self.active_level = 0

        # initial setup
        self.level = 1
        # These are all of the bools that
        # together determine which menu screen should be showing
        self.change_screen = False
        self.game_over = False
        self.game_paused = False
        self.settings_menu_active = False
        self.main_menu_active = True

    def set_active_screen(
        self,
        game_over=False,
        game_paused=False,
        settings_menu=False,
        main_menu=False,
        game_active=False,
    ):
        """
        This is meant to take only one optional argument of True at a time
        Every other bool value in here will be set to False
        """
        self.change_screen = True
        self.game_active = game_active
        self.game_over = game_over
        self.game_paused = game_paused
        self.settings_menu_active = settings_menu
        self.main_menu_active = main_menu

