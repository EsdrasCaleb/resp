import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import time
import random

#modificar https://github.com/starshineee/crawl-IEEE-article/blob/master/crawl.py
#only retrns 10000 per query
class IEEE(object):
    def __init__(self):
        self.wait = 0

    def download_csv(self, documentids=[], cokie=""):
        url = "https://ieeexplore.ieee.org/rest/search/export-csv"
        data = {
            "documentIds": documentids,
            "returnFacets": ["ALL"],
            "returnType": "SEARCH",
        }
        header= {
            "Accept": "application/json,text/plain, */*",
            "Accept-Language": "pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip,deflate,br",
            "Referer": "https://ieeexplore.ieee.org/search/searchresult.jsp",
            "Origin": "https://ieeexplore.ieee.org",
            "Connection": "keep-alive",
            "Cookie": cokie,
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "no-cors",
            "Sec-Fetch-Site": "same-origin",
            "X-Security-Request": "required",
            "Content-Type": "application/json",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "TE": "trailers",
            "Sec-GPC":"1",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0",
        }
        time.sleep(self.wait + random.random())
        response = requests.post(
            url, headers=header, json=data
        )

        return response.text


    def serach_all_articles(self,start_year="2004",end_year="2021",page=1,
                            content=["ContentType:Conferences","ContentType:Journals","ContentType:Magazines"],
                            order=None,cokie=""):
        url = "https://ieeexplore.ieee.org/rest/search"
        data = {
            "sortType": order,
            "returnFacets": ["ALL"],
            "refinements":content,
            "ranges": [start_year+"_"+end_year+"_Year"],
            "returnType": "SEARCH",
            "rowsPerPage":100,
            "pageNumber":page,
        }
        header = {
            "Accept": "application/json,text/plain, */*",
            "Accept-Language": "pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip,deflate,br",
            "Referer": "https://ieeexplore.ieee.org/search/searchresult.jsp",
            "Origin": "https://ieeexplore.ieee.org",
            "Connection": "keep-alive",
            "Cookie": cokie,
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "no-cors",
            "Sec-Fetch-Site": "same-origin",
            "X-Security-Request": "required",
            "Content-Type": "application/json",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "TE": "trailers",
            "Sec-GPC": "1",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0",
        }

        response = requests.post(
            url, headers=header, json=data
        )

        return response.json()
    def serach_articles(self,year,page=1,content=None,order=None,cokie=""):
        url = "https://ieeexplore.ieee.org/rest/search"
        data = {
            "sortType": order,
            "returnFacets": ["ALL"],
            "refinements":content,
            "ranges": [str(year)+"_"+str(year)+"_Year"],
            "returnType": "SEARCH",
            "rowsPerPage":100,
            "pageNumber":page,
        }
        header = {
            "Accept": "application/json,text/plain, */*",
            "Accept-Language": "pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip,deflate,br",
            "Referer": "https://ieeexplore.ieee.org/search/searchresult.jsp",
            "Origin": "https://ieeexplore.ieee.org",
            "Connection": "keep-alive",
            "Cookie": cokie,
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "no-cors",
            "Sec-Fetch-Site": "same-origin",
            "X-Security-Request": "required",
            "Content-Type": "application/json",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "TE": "trailers",
            "Sec-GPC": "1",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0",
        }
        time.sleep(self.wait + random.random())
        response = requests.post(
            url, headers=header, json=data
        )

        return response.json()

    def payload(self, keyword, st_page=0, start_year=2018, end_year=2022):

        params = (
            ("queryText", keyword),
            ("refinements", "ContentType:Early Access Articles"),
            ("refinements", "ContentType:Conferences"),
            ("refinements", "ContentType:Journals"),
            ("refinements", "ContentType:Magazines"),
            ("ranges", str(start_year)+"_"+str(end_year)+"_Year"),
            ("queryID", "45/3852851837"),
            ("pageNumber", str(st_page))
        )

        headers=(
            "Accept: application/json"
        )
        response = requests.get(
            "https://ieeexplore.ieee.org/search/searchresult.jsp",
            params=params,
            headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0"},
        )
        soup = BeautifulSoup(response.text, "html.parser")
        return soup
    def article_data(self,articleurl):
        response = requests.get(
            articleurl,
            headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0"},
        )
        soup = BeautifulSoup(response.text, "html.parser")
    def soup_html(self, soup):

        all_papers = []
        main_class = soup.find(
            "xpl-results-list"
        )

        main_c = main_class.find_all("div", {"class": "List-results-items"})

        for paper in main_c:
            temp_data = {}

            print(paper)
            return
            try:
                content_ = paper.find("h5", {"class": "issue-item__title"})
                paper_url = content_.find("a", href=True)["href"].split("/")

                doi_url.extend(paper_url[2:])
                title = content_.text
                temp_data["title"] = title
                temp_data["link"] = "/".join(doi_url)
                all_papers.append(temp_data)
            except Exception as e:
                pass

        df = pd.DataFrame(all_papers)
        return df

    def query(
        self,
        keyword,
        max_pages=5,
        min_year=2008,
        max_year=2021,
        api_wait=5,
    ):
        "iee final call"
        all_pages = []

        for page in tqdm(range(max_pages)):
            ieee_soup = self.payload(
                keyword, st_page=page, start_year=min_year, end_year=max_year
            )

            acm_result = self.soup_html(ieee_soup)
            all_pages.append(acm_result)
            time.sleep(api_wait)

        df = pd.concat(all_pages)
        return df