from datetime import datetime
import os
from dotenv import load_dotenv
from fpl_api import FplApi
from scraper import Scraper
from gcp_utils import upload_dataframe_to_bigquery

if __name__ == "__main__":
    load_dotenv("env/.env")
    google_credentials = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = google_credentials
    project_id = os.getenv("PROJECT_ID")

    dataset_id = os.getenv("LIVE_DATASET_ID")
    table_id = os.getenv("PRICES_TABLE_ID")

    date = datetime.today().strftime("%Y-%m-%d")
    fpl = FplApi()
    fpl.get_data()
    fpl.combine_data()
    fpl.rename()
    upload_dataframe_to_bigquery(
        df=fpl.combined_data,
        project_id=project_id,
        dataset_id=dataset_id,
        table_id=table_id,
        replace=True,
    )
    # Lines above to form part of airflow tasks

    fpl_player_data = {
        "Name": [],
        "Clean Sheets": [],
        "Goals Conceded": [],
        "Own Goals": [],
        "Saves": [],
        "Cost": [],
        "Points": [],
    }
    fpl_xpath_dict = {
        "Name": "/td[1]",
        "Clean Sheets": "/td[5]",
        "Goals Conceded": "/td[6]",
        "Own Goals": "/td[7]",
        "Saves": "/td[8]",
        "Cost": "/td[9]",
        "Points": "/td[10]",
    }

    dataset_id = os.getenv("FPL_DATASET_ID")
    table_id = os.getenv("YEAR_2017_TABLE_ID")
    if not all([google_credentials, project_id, dataset_id, table_id]):
        raise ValueError("One or more required environment variables are missing!")
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = google_credentials

    fpl_base_path = '//*[@id="gp-content"]/article/div[1]/table/tbody'
    fpl_scraper = Scraper(fpl_player_data, fpl_xpath_dict, fpl_base_path)
    fpl_scraper.scrape(
        url="https://www.premierfantasytools.com/2017-18-fpl-end-of-season-player-data/",
        project_id=project_id,
        dataset_id=dataset_id,
        table_id=table_id,
    )
    table_id = os.getenv("YEAR_2018_TABLE_ID")
    fpl_scraper.scrape(
        url="https://www.premierfantasytools.com/2018-19-fpl-end-of-season-player-data/",
        project_id=project_id,
        dataset_id=dataset_id,
        table_id=table_id,
    )
    table_id = os.getenv("YEAR_2019_TABLE_ID")
    fpl_scraper.scrape(
        url="https://www.premierfantasytools.com/2019-20-fpl-end-of-season-player-data/",
        project_id=project_id,
        dataset_id=dataset_id,
        table_id=table_id,
    )
    table_id = os.getenv("YEAR_2020_TABLE_ID")
    fpl_scraper.scrape(
        url="https://www.premierfantasytools.com/2020-21-fpl-end-of-season-player-data/",
        project_id=project_id,
        dataset_id=dataset_id,
        table_id=table_id,
    )
    table_id = os.getenv("YEAR_2021_TABLE_ID")
    fpl_scraper.scrape(
        url="https://www.premierfantasytools.com/2021-22-fpl-end-of-season-player-data/",
        project_id=project_id,
        dataset_id=dataset_id,
        table_id=table_id,
    )
    table_id = os.getenv("YEAR_2022_TABLE_ID")
    fpl_scraper.scrape(
        url="https://www.premierfantasytools.com/2022-23-fpl-end-of-season-player-data/",
        project_id=project_id,
        dataset_id=dataset_id,
        table_id=table_id,
    )
    table_id = os.getenv("YEAR_2023_TABLE_ID")
    fpl_scraper.scrape(
        url="https://www.premierfantasytools.com/2023-24-fpl-end-of-season-player-data/",
        project_id=project_id,
        dataset_id=dataset_id,
        table_id=table_id,
    )
    fbref_player_data = {
        "Name": [],
        "Nationality": [],
        "Position": [],
        "Team": [],
        "Age": [],
        "Matches Played": [],
        "Starts": [],
        "Minutes": [],
        "Goals": [],
        "Assists": [],
        "Penalties": [],
        "Penalty Attempts": [],
        "Yellow Cards": [],
        "Red Cards": [],
        "xG": [],
        "xA": [],
    }
    fbref_xpath_dict = {
        "Name": "/td[1]",
        "Nationality": "/td[2]",
        "Position": "/td[3]",
        "Team": "/td[4]",
        "Age": "/td[5]",
        "Matches Played": "/td[7]",
        "Starts": "/td[8]",
        "Minutes": "/td[9]",
        "Goals": "/td[11]",
        "Assists": "/td[12]",
        "Penalties": "/td[15]",
        "Penalty Attempts": "/td[16]",
        "Yellow Cards": "/td[17]",
        "Red Cards": "/td[18]",
        "xG": "/td[19]",
        "xA": "/td[21]",
    }
    project_id = os.getenv("PROJECT_ID")
    dataset_id = os.getenv("FBREF_HISTORIC_DATASET_ID")
    table_id = os.getenv("YEAR_2016_TABLE_ID")
    fbref_base_path = '//*[@id="stats_standard"]/tbody'
    fbref_scraper = Scraper(fbref_player_data, fbref_xpath_dict, fbref_base_path)
    fbref_scraper.scrape(
        url="https://fbref.com/en/comps/9/2016-2017/stats/2016-2017-Premier-League-Stats",
        project_id=project_id,
        dataset_id=dataset_id,
        table_id=table_id,
    )
    table_id = os.getenv("YEAR_2017_TABLE_ID")
    fbref_scraper.scrape(
        url="https://fbref.com/en/comps/9/2017-2018/stats/2016-2017-Premier-League-Stats",
        project_id=project_id,
        dataset_id=dataset_id,
        table_id=table_id,
    )
    table_id = os.getenv("YEAR_2018_TABLE_ID")
    fbref_scraper.scrape(
        url="https://fbref.com/en/comps/9/2018-2019/stats/2016-2017-Premier-League-Stats",
        project_id=project_id,
        dataset_id=dataset_id,
        table_id=table_id,
    )
    table_id = os.getenv("YEAR_2019_TABLE_ID")
    fbref_scraper.scrape(
        url="https://fbref.com/en/comps/9/2019-2020/stats/2016-2017-Premier-League-Stats",
        project_id=project_id,
        dataset_id=dataset_id,
        table_id=table_id,
    )
    table_id = os.getenv("YEAR_2020_TABLE_ID")
    fbref_scraper.scrape(
        url="https://fbref.com/en/comps/9/2020-2021/stats/2016-2017-Premier-League-Stats",
        project_id=project_id,
        dataset_id=dataset_id,
        table_id=table_id,
    )
    table_id = os.getenv("YEAR_2021_TABLE_ID")
    fbref_scraper.scrape(
        url="https://fbref.com/en/comps/9/2021-2022/stats/2016-2017-Premier-League-Stats",
        project_id=project_id,
        dataset_id=dataset_id,
        table_id=table_id,
    )
    table_id = os.getenv("YEAR_2022_TABLE_ID")
    fbref_scraper.scrape(
        url="https://fbref.com/en/comps/9/2022-2023/stats/2016-2017-Premier-League-Stats",
        project_id=project_id,
        dataset_id=dataset_id,
        table_id=table_id,
    )
    table_id = os.getenv("YEAR_2023_TABLE_ID")
    fbref_scraper.scrape(
        url="https://fbref.com/en/comps/9/2023-2024/stats/2023-2024-Premier-League-Stats",
        project_id=project_id,
        dataset_id=dataset_id,
        table_id=table_id,
    )
