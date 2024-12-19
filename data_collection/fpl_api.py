import pandas as pd
import logging
import requests
from utils import StringsUtils


class FplApi:
    """Class for accessing and manipulating data from FPL API"""

    def __init__(self):
        logger = logging.getLogger(self.__class__.__name__)
        logger.setLevel("INFO")
        console_handler = logging.StreamHandler()
        format = logging.Formatter(
            "{asctime} - {levelname} - {message}", style="{", datefmt="%Y-%m-%d %H:%M"
        )
        console_handler.setFormatter(format)
        console_handler.setLevel("INFO")
        # TODO add file handler
        logger.addHandler(console_handler)
        self.log = logger
        self.base_url = "https://fantasy.premierleague.com/api/"

    def get_data(self):
        """gets data from api and creates players, positions and teams DFs"""
        self.log.info(f"Get request to {self.base_url + 'bootstrap-static/'}")
        r = requests.get(self.base_url + "bootstrap-static/").json()
        self.players = pd.json_normalize(r["elements"])
        self.positions = pd.json_normalize(r["element_types"])
        self.teams = pd.json_normalize(r["teams"])

    def combine_data(self):
        """Combines player, teams, and position data"""
        self.log.info("Combining data")
        self.players = self.players[
            [
                "id",
                "first_name",
                "second_name",
                "web_name",
                "element_type",
                "team",
                "now_cost",
            ]
        ]
        player_position = pd.merge(
            self.players,
            self.positions[["id", "singular_name_short"]],
            left_on="element_type",
            right_on="id",
        )
        player_position = player_position[
            [
                "id_x",
                "first_name",
                "second_name",
                "web_name",
                "team",
                "singular_name_short",
                "now_cost",
            ]
        ]
        self.combined_data = pd.merge(
            player_position, self.teams[["id", "name"]], left_on="team", right_on="id"
        )

    def rename(self):
        """Rename columns and add full name column"""
        self.log.info("Renaming columns")
        rename = {
            "id_x": "player_id",
            "singular_name_short": "POSITION",
            "now_cost": "COST",
            "name": "TEAM",
        }
        self.combined_data = self.combined_data.rename(columns=rename)
        self.combined_data["NAME"] = (
            self.combined_data["first_name"] + " " + self.combined_data["second_name"]
        )
        self.combined_data["NAME"] = self.combined_data["NAME"].apply(
            StringsUtils.replace_special_character
        )
