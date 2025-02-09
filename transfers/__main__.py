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
    #     diogo dalot teixeira,8,DF,50,98.85580470756972
    # 1,william saliba,2,DF,60,98.1675231464469
    # 2,joachim andersen,10,DF,45,87.19177439585823
    # 3,antonee robinson,13,DF,45,98.09989021472484
    # 4,pedro porro,5,DF,55,116.72093157250032
    # 5,kai havertz,2,FW,80,116.01124994819456
    # 6,alexander isak,7,FW,85,161.93435963906367
    # 7,ollie watkins,4,FW,90,171.25006194619144
    # 8,jordan pickford,15,GK,50,108.02143809200982
    # 9,alphonse areola,9,GK,45,98.97977596880408
    # 10,anthony gordon,7,MF,75,139.80846803852444
    # 11,bukayo saka,2,MF,100,178.6949792339822
    # 12,phil foden,1,MF,95,180.2272638228368
    # 13,bryan mbeumo,16,MF,70,136.011767202393
    # 14,dwight mcneil
    squad = [
        "diogo dalot teixeira",
        "william saliba",
        "joachim andersen",
        "antonee robinson",
        "pedro porro",
        "kai havertz",
        "ollie watkins",
        "jordan pickford",
        "alphonse areola",
        "anthony gordon",
        "bukayo saka",
        "bryan mbeumo",
        "dwight mcneil",
        "nicolas jackson",
        "luis diaz",
    ]
    # transfer.update_squad(squad=squad)
    print(transfer.transferrable_players("joachim andersen", additional_budget=0))
    # transfer.squad.to_csv("data/squad.csv")
