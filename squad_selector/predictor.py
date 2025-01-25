import logging
import pickle

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.impute import KNNImputer
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import GridSearchCV, train_test_split


class Predictor:
    """Train and use a model to predict how many points a player will achieve
    in a season
    """

    def __init__(self, player_data: pd.DataFrame) -> None:
        """Initialise logging, and attributes best_params and model"""
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
        self.best_params = None
        self.model = GradientBoostingRegressor()
        self.player_data = player_data

    def encode_data(self, player_data: pd.DataFrame) -> pd.DataFrame:
        """One hot encodes position of players"""
        player_data = pd.get_dummies(player_data, columns=["POSITION"])
        self.log.info("Data encoded")
        return player_data

    def impute_data(self, player_data: pd.DataFrame) -> np.array:
        """Uses KNN imputation to fill empty data

        Args:
            player_data (pd.DataFrame): formatted and encoded player_data

        Returns:
            np.array: imputed player_data
        """
        imputer = KNNImputer(n_neighbors=2)
        imputed_player_data = imputer.fit_transform(player_data)
        self.log.info("Data imputed")
        return imputed_player_data

    def split_x_y(self, player_data: np.array) -> np.array:
        """Splits player_data into x and y components

        Args:
            player_data (np.array): formatted, encoded and imputed player_data

        Returns:
            np.array: x component of player_data
            np.array: y component of player_data
        """
        player_data_x = player_data[:, :-1]
        player_data_y = player_data[:, -1]
        return player_data_x, player_data_y

    def find_best_params(
        self,
        train_x: np.array,
        train_y: np.array,
        params: dict = {
            "learning_rate": [0.01, 0.05, 0.1],
            "n_estimators": [165, 185, 205],
        },
    ) -> None:
        """Use a grid search to find optimal learning_rate and n_estimators

        Args:
            train_x (np.array): x train data
            train_y (np.array): y train_data
            params (dict, optional): learning_rate and N_estimators to search
            over.
            Defaults to {'learning_rate': [0.01, 0.05, 0.1],
            'n_estimators': [165, 185, 205]}.
        """
        self.log.info("Starting Grid Search")
        model = GradientBoostingRegressor()
        gd_search = GridSearchCV(model, params, scoring="neg_mean_absolute_error")
        gd_search.fit(train_x, train_y)
        self.log.info("Grid Search Complete")
        self.best_params = gd_search.best_params_
        self.model = GradientBoostingRegressor(
            learning_rate=self.best_params["learning_rate"],
            n_estimators=self.best_params["n_estimators"],
        )
        self.log.info(f"Best params: {self.best_params}")

    def train_model(self, train_x: np.array, train_y: np.array) -> None:
        """Train model

        Args:
            train_x (np.array): x train_data
            train_y (np.array): y train_data
        """
        self.model.fit(train_x, train_y)
        self.log.info("Model Trained")

    def build_model(self, test_size=0.2) -> None:
        """Complete process of formatting, encoding, imputing data, training
        and evaluating the model

        Args:
            test_size (float): proportion of data to use as test data
        """
        self.log.info("Starting to build model")
        encoded_data = self.encode_data(self.player_data)
        encoded_data = encoded_data[
            [
                "AGE",
                "TEAM_RANK",
                "POSITION_GK",
                "POSITION_DF",
                "POSITION_MF",
                "POSITION_FW",
                "MATCHES_PLAYED",
                "STARTS",
                "MINUTES",
                "GOALS",
                "ASSISTS",
                "PENALTIES",
                "PENALTIES_MISSED",
                "YELLOW_CARDS",
                "RED_CARDS",
                "xG",
                "xA",
                "OWN_GOALS",
                "GOALS_CONCEDED",
                "CLEAN_SHEETS",
                "SAVES",
                "POINTS",
                "MINUTES_PER_ASSIST",
                "MINUTES_PER_GOAL",
                "MINUTES_PER_GAME",
                "MINUTES_PER_POINT",
                "MINUTES_PER_XG",
                "MINUTES_PER_XA",
                "XG_DIFF",
                "XA_DIFF",
                "NEXT_SEASON_POINTS",
            ]
        ]
        imputed_player_data = self.impute_data(encoded_data)
        train, test = train_test_split(imputed_player_data, test_size=test_size)
        train_x, train_y = self.split_x_y(train)
        test_x, test_y = self.split_x_y(test)
        self.find_best_params(train_x, train_y)
        self.train_model(train_x, train_y)
        self.log.info("Model built")
        self.evaluate_model(test_x, test_y)
        self.visualise_results(test_x, test_y)

    def evaluate_model(self, test_x: np.array, test_y: np.array) -> None:
        """Evaluate model with MAE

        Args:
            test_x (np.array): X test data
            test_y (np.array): Y test data
        """
        predicted_y = self.model.predict(test_x)
        mae = mean_absolute_error(test_y, predicted_y)
        avg = np.average(test_y)
        self.log.info(f"MAE: {mae}, Average: {avg}")

    def visualise_results(self, test_x: np.array, test_y: np.array) -> None:
        """Creates visualisation of models performance

        Args:
            test_x (np.array): X test data
            test_y (np.array): Y test_data
        """
        self.log.info("Visualising Results")
        predicted_y = self.model.predict(test_x)
        plt.figure(figsize=(10, 6))
        plt.scatter(
            x=[range(0, len(test_y), 1)], y=test_y, label="True Values", marker="o"
        )
        plt.scatter(
            x=[range(0, len(predicted_y), 1)],
            y=predicted_y,
            label="Pred Values",
            marker="o",
        )
        true_avg = np.average(test_y)
        pred_avg = np.average(predicted_y)
        plt.axhline(
            y=true_avg,
            color="blue",
            linestyle="--",
            label=f"True Average:{true_avg:.2f}",
        )
        plt.axhline(
            y=pred_avg,
            color="orange",
            linestyle="--",
            label=f"Prediction Average:{pred_avg:.2f}",
        )
        plt.xlabel("Sample Index")
        plt.ylabel("Points")
        plt.title("Predicted Points vs Actual Points")
        plt.legend()
        plt.savefig("figures/predicted_actual.png")
        plt.show()

    def predict(self, to_predict_data: pd.DataFrame) -> pd.DataFrame:
        """Takes previous seasons data and predicts player points

        Args:
            filename (str): last seasons player stats

        Returns:
            pd.DataFrame: player_data with predicted_points
        """
        self.log.info("Starting predictions")
        encoded_data = self.encode_data(to_predict_data)
        encoded_data = encoded_data[
            [
                "AGE",
                "TEAM_RANK",
                "POSITION_GK",
                "POSITION_DF",
                "POSITION_MF",
                "POSITION_FW",
                "MATCHES_PLAYED",
                "STARTS",
                "MINUTES",
                "GOALS",
                "ASSISTS",
                "PENALTIES",
                "PENALTIES_MISSED",
                "YELLOW_CARDS",
                "RED_CARDS",
                "xG",
                "xA",
                "OWN_GOALS",
                "GOALS_CONCEDED",
                "CLEAN_SHEETS",
                "SAVES",
                "POINTS",
                "MINUTES_PER_ASSIST",
                "MINUTES_PER_GOAL",
                "MINUTES_PER_GAME",
                "MINUTES_PER_POINT",
                "MINUTES_PER_XG",
                "MINUTES_PER_XA",
                "XG_DIFF",
                "XA_DIFF",
            ]
        ]
        imputed_player_data = self.impute_data(encoded_data)
        self.log.info("Making prediction")
        prediction = self.model.predict(imputed_player_data)
        to_predict_data["Predicted_Points"] = prediction
        predicted_data = to_predict_data[
            ["NAME", "TEAM_RANK", "POSITION", "COST", "Predicted_Points"]
        ]
        self.log.info("Prediction finished")
        return predicted_data

    def save_model(self) -> None:
        """Saves model to 'models/season_model.sav'"""
        filename = "models/season_model.sav"
        self.log.info("Saving model to %s", filename)
        pickle.dump(self.model, open(filename, "wb"))

    def load_model(self, filename: str) -> None:
        """Loads model into self from file

        Args:
            filename (string): filename of model to load
        """
        self.model = pickle.load(open(filename, "rb"))
        self.log.info(f"Model {filename} loaded in")
