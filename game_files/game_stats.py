import json
import os


class GameStats:
    """ track and control game stats """

    def __init__(self):
        """ Initialize game stats """
        self.player_life_limit = 3
        self.game_active = False
        self.high_score = 0

        self.active_level = 0

        # initial setup
        self._load_game_bools()
        self.reset_stats()
        self._read_high_score()

    def _load_game_bools(self):
        """
        Load active screen bools
        """
        # These are all of the bools that
        # together determine which menu screen should be showing
        self.change_screen = False
        self.game_over = False
        self.game_paused = False
        self.settings_menu_active = False
        self.new_high_score = False
        self.main_menu_active = True

    def _read_high_score(self):
        """
        Check if the high_score dir exists
        If it does, read the high score from the json file
        """

        directory = f"{os.getcwd()}/Stats_data"
        if os.path.isdir(directory):
            with open(f"{directory}/high_score.json", "r") as extracted_high_score:
                previous_high_score = json.load(extracted_high_score)
            extracted_high_score.close()
            self.high_score = previous_high_score["high_score"]

    def set_high_score(self):
        """
        Make the Stats_data dir if needed.
        If there is a new high score, write to json.
        """
        directory = f"{os.getcwd()}/Stats_data"
        if not os.path.isdir(directory):
            os.mkdir(directory)

        if self.level > self.high_score:
            self.high_score = self.level
            self.new_high_score = True
            high_score_json_data = {"high_score": self.high_score}
            with open(f"{directory}/high_score.json", "w") as hs_json_file:
                json.dump(high_score_json_data, hs_json_file, indent=4)
            hs_json_file.close()

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

    def reset_stats(self):
        """ reset the game stats """
        self.level = 1
        self.lives_left = self.player_life_limit
