import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import time


class Scholar(object):
    def __init__(self):
        pass

    def payload(self, keyword, st_page=0, pasize=50, start_year, end_year):

        params = (
            ("q", keyword),
            ("as_ylo", str(start_year)),
            ("as_yhi", str(end_year)),
            ("sortBy", "relevancy"),
            ("startPage", str(st_page)),
            ("pageSize", str(pasize)),
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
            "div", {"class": "col-lg-9 col-md-9 col-sm-8 sticko__side-content"}
        )
        main_c = main_class.find_all("li", {"class": "search__item issue-item-container"})
        for paper_ob in main_c:
            temp_data = {}
            doi_url = ["https://dl.acm.org", "doi", "pdf"]
            try:
                paper = paper_ob.find("div", {"class": "issue-item__content"})
                content_ = paper.find("h5", {"class": "issue-item__title"})
                paper_url = content_.find("a", href=True)["href"].split("/")
                paper_year = paper_ob.find("div",{"class":"bookPubDate simple-tooltip__block--b"}).text.split(" ")
                doi_url.extend(paper_url[2:])
                title = content_.text
                temp_data["title"] = title
                temp_data["link"] = "/".join(doi_url)
                temp_data["year"] = paper_year[1]
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
        api_wait=5,
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