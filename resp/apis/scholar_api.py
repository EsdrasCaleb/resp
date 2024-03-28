import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import time
import random


class Scholar(object):

    def __init__(self,start_year=2004,end_year=2021,year_dept=2):
        self.start_year = start_year
        self.end_year = end_year
        self.year_dept = year_dept
        self.api_wait=7

    def payload(self, keyword, st_page=0, pasize=10):

        params = (
            ("q", keyword),
            ("as_ylo", str(self.start_year)),
            ("as_yhi", str(self.end_year)),
            ("start", str(st_page*pasize)),
        )
        time.sleep(self.api_wait + random.random()*2)
        response = requests.get(
            "https://scholar.google.com/scholar",
            params=params,
            headers={
                "accept": "application/json",
                "Cookie":"GOOGLE_ABUSE_EXEMPTION=ID=f7786fc4867395fc:TM=1711593393:C=r:IP=89.39.107.172-:S=QHDfCTuFlUofZYsNgJ6p-Qc; NID=512=Cblf366wbr9ZKjtptxf8ceRYv-lGW1CmGA1M2b3vicbEtztUtysaWm5b69oiKEtCY5HnW3mKd5mMaj__M53cUuplqxEIvnACSMn1TFADuPhAqM8KH7_E3l6XB9k0qaeuA1AGZVX_zoYFtOpurCjqgE8CEI5fdCZjJK95dWOtu6c; GSP=A=tdd-wg:CPTS=1711593468:LM=1711593468:S=VwkQPpy_da2bQadB"
             },
        )
        
        soup = BeautifulSoup(response.text, "html.parser")
        return soup

    def citations(self,citeurl,paper_year):
        time.sleep(self.api_wait+random.random()*2)
        response = requests.get(
            "https://scholar.google.com"+citeurl+"&as_ylo="+str(paper_year)+"&as_yhi="+str(paper_year+self.year_dept),
            headers={"accept": "application/json",
                     "Cookie": "GOOGLE_ABUSE_EXEMPTION=ID=f7786fc4867395fc:TM=1711593393:C=r:IP=89.39.107.172-:S=QHDfCTuFlUofZYsNgJ6p-Qc; NID=512=Cblf366wbr9ZKjtptxf8ceRYv-lGW1CmGA1M2b3vicbEtztUtysaWm5b69oiKEtCY5HnW3mKd5mMaj__M53cUuplqxEIvnACSMn1TFADuPhAqM8KH7_E3l6XB9k0qaeuA1AGZVX_zoYFtOpurCjqgE8CEI5fdCZjJK95dWOtu6c; GSP=A=tdd-wg:CPTS=1711593468:LM=1711593468:S=VwkQPpy_da2bQadB"
                 },
        )
        citesoup = BeautifulSoup(response.text, "html.parser")
        
        search = citesoup.find(
            "div", {"id": "gs_ab_md"}
        )
        part = search.find("div",{"class":"gs_ab_mdw"})

        if(part.contents):
            paper_count = [int(i.translate({ord('.'): None})) for i in part.contents[0].split(" ") if i.translate({ord('.'): None}).isdigit()][0]
        else:
            paper_count = 0

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

        return all_papers

    def query(
        self,
        keyword,
        max_pages=5,
    ):
        all_pages = []

        for page in tqdm(range(max_pages)):
            time.sleep(self.api_wait)
            scholar_soup = self.payload(
                keyword, st_page=page, pasize=10
            )
            scholar_result = self.soup_html(scholar_soup)
            all_pages += scholar_result

        return all_pages

    def paper_citations(self,paper_name,paper_year):
        self.start_year = paper_year
        self.end_year = int(paper_year)+2
        scholar_soup = self.payload(
            paper_name, st_page=0, pasize=1
        )

        lowbar = scholar_soup.find("div", {"class": "gs_fl gs_flb gs_invis"})
        if(lowbar):
            return self.citations(lowbar.contents[4]["href"], int(paper_year))
        else:
            hibar = scholar_soup.findAll("div", {"class": "gs_fl gs_flb"})
            if(hibar):
                return self.citations(hibar[0].contents[4]["href"], int(paper_year))
            else:
                print("possivel erro no scholar")
                return 0