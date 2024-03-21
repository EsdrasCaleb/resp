import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import time


class Scholar(object):

    def __init__(self,start_year=2018,end_year=2022,year_dept=2):
        self.start_year = start_year
        self.end_year = end_year
        self.year_dept = year_dept
        self.api_wait=2

    def payload(self, keyword, st_page=0, pasize=10):

        params = (
            ("q", keyword),
            ("as_ylo", str(self.start_year)),
            ("as_yhi", str(self.end_year)),
            ("start", str(st_page*pasize)),
        )

        response = requests.get(
            "https://scholar.google.com/scholar",
            params=params,
            headers={"accept": "application/json"},
        )
        
        soup = BeautifulSoup(response.text, "html.parser")

        return soup

    def citations(self,citeurl,paper_year):
        time.sleep(self.api_wait)
        response = requests.get(
            "https://scholar.google.com"+citeurl+"&as_ylo="+str(paper_year)+"&as_yhi="+str(paper_year+self.year_dept),
            headers={"accept": "application/json"},
        )
        citesoup = BeautifulSoup(response.text, "html.parser")
        
        search = citesoup.find(
            "div", {"id": "gs_ab_md"}
        )
        part = search.find("div",{"class":"gs_ab_mdw"})
      
        paper_count = [int(i) for i in part.contents[0].split(" ") if i.isdigit()][0]
        
        return paper_count

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
                
                paper_year_string = paper.find("div",{"class":"gs_a"}).contents[-1].split(",")
                paper_year = [int(i) for i in paper_year_string[-1].split(" ") if i.isdigit()][0]
                citations = self.citations(paper.find("div",{"class":"gs_fl gs_flb"}).contents[4]["href"],paper_year)
                
                title = content_.text
                
                temp_data["title"] = title
                temp_data["link"] = paper_url
                temp_data["year"] = paper_year
                temp_data["citations"] = citations
                all_papers.append(temp_data)
            except Exception as e:
                print("error")
                print(e)

        df = pd.DataFrame(all_papers)
        return df

    def query(
        self,
        keyword,
        max_pages=5,
    ):
        all_pages = []

        for page in tqdm(range(max_pages)):
            scholar_soup = self.payload(
                keyword, st_page=page, pasize=10
            )
            time.sleep(self.api_wait)
            scholar_result = self.soup_html(scholar_soup)
            all_pages.append(scholar_result)


        df = pd.concat(all_pages)
        return df