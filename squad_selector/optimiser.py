import logging

import pandas as pd
import pulp
from pulp import LpMaximize, LpProblem, LpVariable, lpSum


class Optimiser:
    """Select squad using optimisation for max points"""

    def __init__(self, season_data: pd.DataFrame):
        """initialise optimiser

        Args:
            season_data (pd.DataFrame): predicted data for optimisation
        """
        self.season_data = season_data
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

    def remove_player(self, player: str):
        """Remove a player from the data

        Args:
            player (str): player's name to remove from data
        """
        self.season_data = self.season_data[self.season_data["NAME"] != player]
        self.log.info(f"{str.upper(player)} removed")

    def change_position(self, player: str, position: str):
        """Change a player's position

        Args:
            player (str): player's name
            position (str): position to change to
        """
        self.season_data.loc[self.season_data["NAME"] == player, "POSITION"] = position
        self.log.info(f"{str.upper(player)} position changed to {position}")

    def encode_data(self):
        """one hot encode position and team in data and assign to
        self.season_data_encoded
        """
        self.season_data_encoded = pd.get_dummies(
            self.season_data, columns=["POSITION", "TEAM_RANK"]
        )
        self.log.info("Position and RK encoded")

    def add_constraint_cols(self):
        """add logical columns for a GK with cost<50 and outfield player <50"""
        self.season_data_encoded["GK_50"] = self.season_data_encoded["POSITION_GK"] & (
            self.season_data_encoded["COST"] < 50
        )
        self.season_data_encoded["OUTFIELD_50"] = (
            self.season_data_encoded["POSITION_DF"]
            | self.season_data_encoded["POSITION_MF"]
            | self.season_data_encoded["POSITION_FW"]
        ) & (self.season_data_encoded["COST"] <= 50)
        self.season_data_encoded["MID_60"] = (
            self.season_data_encoded["POSITION_MF"]
        ) & (self.season_data_encoded["COST"] <= 60)
        self.log.info("Constraint columns added")

    def create_problem(self):
        """Create optimisation model and add constraints"""
        self.model = LpProblem("Select Squad", LpMaximize)
        self.x = [
            LpVariable(f"x{i}", cat="Binary") for i in range(len(self.season_data))
        ]
        self.model += lpSum(
            [
                self.season_data_encoded.loc[i, "Predicted_Points"] * self.x[i]
                for i in range(len(self.season_data_encoded))
            ]
        )
        self.model += (
            lpSum(
                [
                    self.season_data_encoded.loc[i, "POSITION_GK"] * self.x[i]
                    for i in range(len(self.season_data_encoded))
                ]
            )
            == 2,
            "No. of GKs",
        )
        self.model += (
            lpSum(
                [
                    self.season_data_encoded.loc[i, "GK_50"] * self.x[i]
                    for i in range(len(self.season_data_encoded))
                ]
            )
            == 1,
            "Bench GK <5m",
        )
        self.model += (
            lpSum(
                [
                    self.season_data_encoded.loc[i, "POSITION_DF"] * self.x[i]
                    for i in range(len(self.season_data_encoded))
                ]
            )
            == 5,
            "No. of DEFs",
        )
        self.model += (
            lpSum(
                [
                    self.season_data_encoded.loc[i, "POSITION_MF"] * self.x[i]
                    for i in range(len(self.season_data_encoded))
                ]
            )
            == 5,
            "No. of MIDs",
        )
        self.model += (
            lpSum(
                [
                    self.season_data_encoded.loc[i, "POSITION_FW"] * self.x[i]
                    for i in range(len(self.season_data_encoded))
                ]
            )
            == 3,
            "No. of FWDs",
        )
        self.model += (
            lpSum(
                [
                    self.season_data_encoded.loc[i, "OUTFIELD_50"] * self.x[i]
                    for i in range(len(self.season_data_encoded))
                ]
            )
            == 2,
            "2 Outfield Bench Players",
        )
        self.model += (
            lpSum(
                [
                    self.season_data_encoded.loc[i, "MID_60"] * self.x[i]
                    for i in range(len(self.season_data_encoded))
                ]
            )
            == 1,
            "MID bench player",
        )
        self.model += (
            lpSum(
                [
                    self.season_data_encoded.loc[i, "COST"] * self.x[i]
                    for i in range(len(self.season_data_encoded))
                ]
            )
            <= 1000,
            "TOTAL VALUE IS 100M",
        )
        columns = list(self.season_data_encoded.columns)
        for col in columns:
            if col[:2] == "RK":
                constraint_name = "No more than 3 players for " + str(col)
                self.model += (
                    lpSum(
                        [
                            self.season_data_encoded.loc[i, col] * self.x[i]
                            for i in range(len(self.season_data_encoded))
                        ]
                    )
                    <= 3,
                    constraint_name,
                )
        self.log.info("Optimisation problem created")

    def solve_problem(self):
        """Solve optimisation problem"""
        self.model.solve()
        self.log.info("Problem solved")

    def get_squad(self):
        """from solved optimisation, saves selected squad as csv"""
        selected_rows = []
        for i in range(len(self.season_data)):
            if pulp.value(self.x[i]) == 1:
                selected_rows.append(i)
        squad = (
            self.season_data.loc[selected_rows]
            .sort_values(by="POSITION")
            .reset_index()[
                ["NAME", "TEAM_RANK", "POSITION", "COST", "Predicted_Points"]
            ]
        )
        self.log.info("Squad created")
        return squad
