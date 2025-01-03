import pandas as pd
from optimiser import Optimiser
from predictor import Predictor
from factorengineering import FactorEngineering
from feature_importance import FeatureImportance
from dotenv import load_dotenv
import os
from pandas_gbq import read_gbq


if __name__ == "__main__":
    load_dotenv("env/.env")
    google_credentials = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = google_credentials
    project_id = os.getenv("PROJECT_ID")

    dataset_id = os.getenv("OUTPUT_DATASET_ID")
    table_id = os.getenv("TRAIN_DATA_TABLE_ID")

    train_query = f"SELECT * FROM {dataset_id}.{table_id}"
    player_data = read_gbq(train_query, project_id=project_id)

    table_id = os.getenv("YEAR_2024_TABLE_ID")
    to_predict_query = f"SELECT * FROM {dataset_id}.{table_id}"
    to_predict = read_gbq(to_predict_query, project_id=project_id)

    pd_fe = FactorEngineering(player_data)
    pd_fe.format_data()
    pd_fe.add_minutes_assist()
    pd_fe.add_minutes_goals()
    pd_fe.add_minutes_per_game()
    pd_fe.add_minutes_points()
    pd_fe.add_minutes_xg()
    pd_fe.add_minutes_xa()
    pd_fe.add_xg_difference()
    pd_fe.add_xa_difference()
    pd_fe.replace_inf_values()
    pd_fe.remove_incorrect_rows()
    formatted_player_data = pd_fe.player_data
    pred_fe = FactorEngineering(to_predict)
    pred_fe.add_minutes_assist()
    pred_fe.add_minutes_goals()
    pred_fe.add_minutes_per_game()
    pred_fe.add_minutes_points()
    pred_fe.add_minutes_xg()
    pred_fe.add_minutes_xa()
    pred_fe.add_xg_difference()
    pred_fe.add_xa_difference()
    pred_fe.replace_inf_values()
    pred_fe.remove_incorrect_rows()
    to_predict = pred_fe.player_data
    predictor = Predictor(formatted_player_data)  # Error
    predictor.build_model()
    print(to_predict.columns)
    prediction = predictor.predict(to_predict)
    table_id = os.getenv("PREDICTED_TABLE_ID")
    table_ref = f"{project_id}.{dataset_id}.{table_id}"
    formatted_player_data.to_gbq(
        destination_table=table_ref,
        project_id=project_id,
        if_exists="replace",
    )
    model_importances = predictor.model.feature_importances_
    optimiser = Optimiser(prediction)
    optimiser.remove_player("julian alvarez")
    optimiser.season_data.reset_index(inplace=True)
    optimiser.encode_data()
    optimiser.add_constraint_cols()
    optimiser.create_problem()
    optimiser.solve_problem()
    squad = optimiser.get_squad()
    squad.to_csv("SQUAD.csv")
    feature_names = [
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
        "xg_diff",
        "xa_diff",
        "NEXT_SEASON_POINTS",
    ]
    encoded_data = predictor.encode_data(formatted_player_data)
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
            "xg_diff",
            "xa_diff",
            "NEXT_SEASON_POINTS",
        ]
    ]
    imputed_data = predictor.impute_data(encoded_data)
    x, y = predictor.split_x_y(imputed_data)
    FeatureImportance.plot_importance(
        importances=model_importances,
        feature_names=feature_names,
        fname="figures/feature_importance.png",
        x_data=x,
    )
    FeatureImportance.SHAP(model=predictor.model, X=x)
