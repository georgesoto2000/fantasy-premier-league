import pandas as pd
from tqdm import tqdm
import logging
from selenium import webdriver
from utils import StringsUtils
from selenium.webdriver.common.by import By
from gcp_utils import upload_dataframe_to_bigquery


class Scraper:
    def __init__(self, player_data: dict, xpath_dict: dict, base_path: str):
        self.base_path = base_path
        self.player_data = player_data
        self.xpath_dict = xpath_dict
        self.driver = None
        logger = logging.getLogger(self.__class__.__name__)
        logger.setLevel(10)
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
        self.logger = logger

    def get_element(self, path: str):
        """Gets an element from an xpath, if it doesn't exist, returns None

        Args:
            path (str): xpath of stat
            driver (webdriver): driver of fbref page

        Returns:
            _type_: stat
        """
        try:
            stat = self.driver.find_element(By.XPATH, path).text
        except:  # TODO specific exception
            stat = None
        return stat

    def get_player_stats_from_xpath(self, path: str) -> None:
        """Gets player data from xpath

        Args:
            path (str): xpath path to player
            driver (webdriver): driver with page open to scrape
            player_data (dict): dict to populate with data
            xpath_dict (dict): dict containing stat names and xpath suffix

        Returns:
            dict: populated player_data
        """
        for key, value in self.xpath_dict.items():
            stat = self.get_element(path + value)
            if key == "Name":
                stat = StringsUtils.replace_special_character(stat)
            elif key == "Nationality":
                try:
                    stat = stat.split()[1]
                except:  # TODO specific exception
                    pass
            self.player_data[key].append(stat)

    def scrape(self, url: str, project_id: str, dataset_id: str, table_id: str):
        """opens webdriver and extracts player data

        Args:
            url (str): url of website to scrape from
            filename (str): filename to save data to
        """
        self.logger.info("Scraping for %s", table_id)
        self.logger.info("Opening browser")
        self.driver = webdriver.Chrome()
        self.driver.get(url)
        table = self.driver.find_element(By.XPATH, self.base_path)
        table_length = len(table.find_elements(By.TAG_NAME, "tr"))
        self.logger.info("Scraping started")
        for i in tqdm(range(1, table_length)):
            xpath = self.base_path + f"/tr[{i}]"
            self.get_player_stats_from_xpath(xpath)
        self.logger.info("%s rows scrapped.", table_length)
        player_data = pd.DataFrame.from_dict(self.player_data)
        player_data.columns = player_data.columns.str.replace(" ", "_")
        upload_dataframe_to_bigquery(
            df=player_data,
            project_id=project_id,
            dataset_id=dataset_id,
            table_id=table_id,
            replace=True,
        )
        self.logger.info("Saved data to BQ")
        for key in self.player_data:
            self.player_data[key].clear()
