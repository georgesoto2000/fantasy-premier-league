import pandas as pd
import logging


class Transfer:
    def __init__(self, squad: pd.DataFrame, season_predictions: pd.DataFrame):
        logger = logging.getLogger(self.__class__.__name__)
        logger.setLevel("INFO")
        console_handler = logging.StreamHandler()
        format = logging.Formatter("{asctime} - {levelname} - {message}", 
                                   style="{", datefmt="%Y-%m-%d %H:%M")
        console_handler.setFormatter(format)
        console_handler.setLevel("INFO")
        file_handler = logging.FileHandler("logs/app.log", 
                                           mode="a", 
                                           encoding='utf-8')
        file_handler.setLevel("INFO")
        file_handler.setFormatter(format)
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        self.log = logger
        self.squad = squad
        self.season_predictions = season_predictions

    def transferrable_players(self, player: str) -> pd.DataFrame:
        """List the top transfer available for a player

        Args:
            player (str): player to transfer

        Returns:
            pd.DataFrame: _description_
        """
        predicted_season = self.season_predictions
        team_counts = self.squad['RK'].value_counts()
        team_counts_3 = team_counts[team_counts == 3].index.tolist()
        squad_members = self.squad['NAME'].to_list()
        for member in squad_members:
            predicted_season = predicted_season[predicted_season['NAME'] != member]
        for team in team_counts_3:
            predicted_season = predicted_season[predicted_season['RK'] != team]
        position = self.squad.loc[self.squad['NAME'] == player, 'POSITION'].values[0]
        cost = self.squad.loc[self.squad['NAME'] == player, 'COST'].values[0]
        potential_transfers = predicted_season[(predicted_season['POSITION'] == position) & (predicted_season['COST'] <= cost)]
        return potential_transfers.sort_values(by='Predicted_Points', ascending=False)
    
    def confirm_transfer(self, player_in: str, player_out: str) -> None:
        self.squad = self.squad[self.squad['NAME'] != player_out]
        self.squad = pd.concat([self.season_predictions[self.season_predictions['NAME'] == player_in], self.squad])
        self.squad = self.squad.sort_values(by='POSITION').reset_index()[['NAME', 'RK', 'POSITION', 'COST', 'Predicted_Points']]

    def update_prices(self):
        pass