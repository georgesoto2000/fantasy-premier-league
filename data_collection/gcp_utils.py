import pandas as pd


def upload_dataframe_to_bigquery(
    df: pd.DataFrame, project_id: str, dataset_id: str, table_id: str, replace: bool
) -> None:
    """Takes dataframe into BigQuery

    Args:
        df (pd.DataFrame): dataframe to be uploaded to BQ
        project_id (str): BQ project id
        dataset_id (str):BQ dataset id
        table_id (str): BQ table ID
        replace (bool): if it already exists, should it be replaced
    """
    if replace:
        if_exists = "replace"
    else:
        if_exists = "append"
    table_ref = f"{project_id}.{dataset_id}.{table_id}"
    df.to_gbq(
        destination_table=table_ref,
        project_id=project_id,
        if_exists=if_exists,
        location="EU",
    )
