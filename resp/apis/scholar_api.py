import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import time


class Scholar(object):
    def __init__(self):
        pass

    def payload(self, keyword, st_page=0, pasize=10, start_year=2018, end_year=2022):

        params = (
            ("q", keyword),
            ("as_ylo", str(start_year)),
            ("as_yhi", str(end_year)),
            ("start", str(st_page*pasize)),
        )

        response = requests.get(
            "https://scholar.google.com/scholar",
            params=params,
            headers={"accept": "application/json"},
        )
        soup = BeautifulSoup(response.text, "html.parser")

        return soup

    def soup_html(self, soup):

        all_papers = []

        main_class = soup.find(
            "div", {"id": "gs_res_ccl_mid"}
        )

        main_c = main_class.find_all("div", {"class": "gs_r gs_or gs_scl"})
        for paper in main_c:
            temp_data = {}

            try:
                content_ = paper.find("h3", {"class": "gs_rt"})
                paper_url = content_.find("a", href=True)["href"]
                paper_year = paper.find("div",{"class":"gs_a"}).text.split(",")
                title = content_.text

                temp_data["title"] = title
                temp_data["link"] = paper_url
                temp_data["year"] = paper_year[-1]
                temp_data["month"] = paper_year[0]
                all_papers.append(temp_data)
            except Exception as e:
                pass

        df = pd.DataFrame(all_papers)
        return df

    def query(
        self,
        keyword,
        max_pages=5,
        min_year=2015,
        max_year=2022,
        full_page_result=False,
        api_wait=2,
    ):
        "acm final call"
        all_pages = []

        for page in tqdm(range(max_pages)):
            acm_soup = self.payload(
                keyword, st_page=page, pasize=50, start_year=min_year, end_year=max_year
            )

            acm_result = self.soup_html(acm_soup)
            all_pages.append(acm_result)
            time.sleep(api_wait)

        df = pd.concat(all_pages)
        return df