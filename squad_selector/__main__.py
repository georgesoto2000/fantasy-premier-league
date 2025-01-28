import os

from dotenv import load_dotenv
from feature_importance import FeatureImportance
from optimiser import Optimiser
from pandas_gbq import read_gbq
from predictor import Predictor

if __name__ == "__main__":
    load_dotenv("env/.env")
    google_credentials = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = google_credentials
    project_id = os.getenv("PROJECT_ID")

    dataset_id = os.getenv("OUTPUT_DATASET_ID")
    table_id = os.getenv("TRAIN_DATA_TABLE_ID")

    train_query = f"SELECT * FROM {dataset_id}.{table_id}"
    train_data = read_gbq(train_query, project_id=project_id)

    table_id = os.getenv("TO_PREDICT")
    to_predict_query = f"SELECT * FROM {dataset_id}.{table_id}"
    predict = read_gbq(to_predict_query, project_id=project_id)

    predictor = Predictor(train_data)  # Error
    predictor.build_model()
    prediction = predictor.predict(predict)
    table_id = os.getenv("PREDICTED_TABLE_ID")
    table_ref = f"{project_id}.{dataset_id}.{table_id}"
    prediction.to_gbq(
        destination_table=table_ref,
        project_id=project_id,
        if_exists="replace",
    )
    model_importances = predictor.model.feature_importances_
    optimiser = Optimiser(prediction)
    optimiser.remove_player("julian alvarez")
    optimiser.remove_player("conor gallagher")
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
            "XG_DIFF",
            "XA_DIFF",
            "NEXT_SEASON_POINTS",
    ]
    encoded_data = predictor.encode_data(train_data)
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
    imputed_data = predictor.impute_data(encoded_data)
    x, y = predictor.split_x_y(imputed_data)
    FeatureImportance.plot_importance(
        importances=model_importances,
        feature_names=feature_names,
        fname="figures/feature_importance.png",
        x_data=x,
    )
    FeatureImportance.SHAP(model=predictor.model, X=x)
