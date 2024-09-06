import pandas as pd
from transfer import Transfer

if __name__ == "__main__":
    squad = pd.read_csv("data/squad.csv")[
        ["NAME", "RK", "POSITION", "COST", "Predicted_Points"]
    ]
    predictions = pd.read_csv("data/processed_data/PREDICTED_SEASON_2025.csv")[
        ["NAME", "RK", "POSITION", "COST", "Predicted_Points"]
    ]
    transfer = Transfer(squad=squad, season_predictions=predictions)
    print(transfer.transferrable_players("phil foden"))
    transfer.confirm_transfer(
        player_out="fabian schar", player_in="diogo dalot teixeira"
    )
    transfer.squad.to_csv("data/squad.csv")
