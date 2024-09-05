import pandas as pd
import numpy as np
import logging


class FactorEngineering:
    def __init__(self, player_data: pd.DataFrame) -> None:
        self.player_data = player_data
        logger = logging.getLogger(self.__class__.__name__)
        logger.setLevel("INFO")
        console_handler = logging.StreamHandler()
        format = logging.Formatter(
            "{asctime} - {levelname} - {message}", style="{", datefmt="%Y-%m-%d %H:%M"
        )
        console_handler.setFormatter(format)
        console_handler.setLevel("INFO")
        file_handler = logging.FileHandler("logs/app.log", mode="a", encoding="utf-8")
        file_handler.setLevel("INFO")
        file_handler.setFormatter(format)
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        self.log = logger

    def format_data(self) -> None:
        """Corrects positional data in filename"""
        self.player_data[self.player_data["POSITION"] == "FW,MF"]["POSITION"] = "MF"
        self.player_data["POSITION"] = self.player_data["POSITION"].str[:2]

    def add_xg_difference(self) -> None:
        self.player_data["xg_diff"] = self.player_data["GOALS"] - self.player_data["xG"]

    def add_xa_difference(self) -> None:
        self.player_data["xa_diff"] = (
            self.player_data["ASSISTS"] - self.player_data["xA"]
        )

    def add_minutes_per_game(self) -> None:
        self.player_data["MINUTES_PER_GAME"] = self.player_data["MINUTES"].div(
            self.player_data["MATCHES_PLAYED"], axis=0
        )

    def add_minutes_xg(self) -> None:
        self.player_data["MINUTES_PER_XG"] = self.player_data["MINUTES"].div(
            self.player_data["xG"], axis=0
        )

    def add_minutes_xa(self) -> None:
        self.player_data["MINUTES_PER_XA"] = self.player_data["MINUTES"].div(
            self.player_data["xA"], axis=0
        )

    def add_minutes_goals(self) -> None:
        self.player_data["MINUTES_PER_GOAL"] = self.player_data["MINUTES"].div(
            self.player_data["GOALS"], axis=0
        )

    def add_minutes_assist(self) -> None:
        self.player_data["MINUTES_PER_ASSIST"] = self.player_data["MINUTES"].div(
            self.player_data["ASSISTS"], axis=0
        )

    def add_minutes_points(self) -> None:
        self.player_data["MINUTES_PER_POINT"] = self.player_data["MINUTES"].div(
            self.player_data["POINTS"], axis=0
        )

    def replace_inf_values(self) -> None:
        self.player_data[["MINUTES_PER_ASSIST", "MINUTES_PER_GOAL"]] = self.player_data[
            ["MINUTES_PER_ASSIST", "MINUTES_PER_GOAL"]
        ].replace(np.inf, 3510)
        self.player_data[["MINUTES_PER_XA", "MINUTES_PER_XG"]] = self.player_data[
            ["MINUTES_PER_XA", "MINUTES_PER_XG"]
        ].replace(np.inf, 35100)
        self.player_data["MINUTES_PER_GAME"] = self.player_data[
            ["MINUTES_PER_GAME"]
        ].replace(np.inf, 0)
        self.player_data["MINUTES_PER_POINT"] = self.player_data[
            ["MINUTES_PER_POINT"]
        ].replace(np.inf, 270)

    def remove_incorrect_rows(self) -> None:
        before_len = len(self.player_data)
        self.player_data = self.player_data[self.player_data["MATCHES_PLAYED"] < 39]
        after_len = len(self.player_data)
        rows_removed = before_len - after_len
        self.log.warning(f"{rows_removed} rows removed")
