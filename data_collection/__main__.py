from datetime import datetime

from fpl_api import FplApi
from scraper import Scraper

if __name__ == "__main__":
    date = datetime.today().strftime("%Y-%m-%d")
    fpl = FplApi()
    fpl.get_data()
    fpl.combine_data()
    fpl.rename()
    fpl.combined_data.to_csv(f"data/raw_data/api/fpl_prices_{date}.csv")
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
    fpl_base_path = '//*[@id="gp-content"]/article/div[1]/table/tbody'
    fpl_scraper = Scraper(fpl_player_data, fpl_xpath_dict, fpl_base_path)
    fpl_scraper.scrape(
        url="https://www.premierfantasytools.com/2017-18-fpl-end-of-season-player-data/",
        filename="data/raw_data/fpl/fpl_2017.csv",
    )
    fpl_scraper.scrape(
        url="https://www.premierfantasytools.com/2018-19-fpl-end-of-season-player-data/",
        filename="data/raw_data/fpl/fpl_2018.csv",
    )
    fpl_scraper.scrape(
        url="https://www.premierfantasytools.com/2019-20-fpl-end-of-season-player-data/",
        filename="data/raw_data/fpl/fpl_2019.csv",
    )
    fpl_scraper.scrape(
        url="https://www.premierfantasytools.com/2020-21-fpl-end-of-season-player-data/",
        filename="data/raw_data/fpl/fpl_2020.csv",
    )
    fpl_scraper.scrape(
        url="https://www.premierfantasytools.com/2021-22-fpl-end-of-season-player-data/",
        filename="data/raw_data/fpl/fpl_2021.csv",
    )
    fpl_scraper.scrape(
        url="https://www.premierfantasytools.com/2022-23-fpl-end-of-season-player-data/",
        filename="data/raw_data/fpl/fpl_2022.csv",
    )
    fpl_scraper.scrape(
        url="https://www.premierfantasytools.com/2023-24-fpl-end-of-season-player-data/",
        filename="data/raw_data/fpl/fpl_2023.csv",
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
    fbref_base_path = '//*[@id="stats_standard"]/tbody'
    fbref_scraper = Scraper(fbref_player_data, fbref_xpath_dict, fbref_base_path)
    fbref_scraper.scrape(
        url="https://fbref.com/en/comps/9/2016-2017/stats/2016-2017-Premier-League-Stats",
        filename="data/raw_data/fbref/fbref_2016.csv",
    )
    fbref_scraper.scrape(
        url="https://fbref.com/en/comps/9/2017-2018/stats/2016-2017-Premier-League-Stats",
        filename="data/raw_data/fbref/fbref_2017.csv",
    )
    fbref_scraper.scrape(
        url="https://fbref.com/en/comps/9/2018-2019/stats/2016-2017-Premier-League-Stats",
        filename="data/raw_data/fbref/fbref_2018.csv",
    )
    fbref_scraper.scrape(
        url="https://fbref.com/en/comps/9/2019-2020/stats/2016-2017-Premier-League-Stats",
        filename="data/raw_data/fbref/fbref_2019.csv",
    )
    fbref_scraper.scrape(
        url="https://fbref.com/en/comps/9/2020-2021/stats/2016-2017-Premier-League-Stats",
        filename="data/raw_data/fbref/fbref_2020.csv",
    )
    fbref_scraper.scrape(
        url="https://fbref.com/en/comps/9/2021-2022/stats/2016-2017-Premier-League-Stats",
        filename="data/raw_data/fbref/fbref_2021.csv",
    )
    fbref_scraper.scrape(
        url="https://fbref.com/en/comps/9/2022-2023/stats/2016-2017-Premier-League-Stats",
        filename="data/raw_data/fbref/fbref_2022.csv",
    )
    fbref_scraper.scrape(
        url="https://fbref.com/en/comps/9/stats/Premier-League-Stats",
        filename="data/raw_data/fbref/fbref_2023.csv",
    )
