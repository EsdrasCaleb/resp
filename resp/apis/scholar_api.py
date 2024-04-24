import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
import urllib.parse
from tqdm import tqdm
import time
import random
import user_agent
from fp.fp import FreeProxy
from proxy_helper import proxy_helper



class Scholar(object):

    def __init__(self,cookie="") :
        self.start_year = 2004
        self.end_year = 2021
        self.year_dept = 2
        self.api_wait=5
        self.cokie = ""
        self.backList = []
        self.proxyIndex = 0
        self.proxyArray = [
                 ]
        self.helper = proxy_helper([
            {"url": "https://advanced.name/freeproxy/66286f5e16bac?type=https", "protocol": "https", "json": False},
            {"url": "https://advanced.name/freeproxy/66286f5e16bac?type=socks4", "json": False, "protocol": "socks4"},
            {"url": "https://advanced.name/freeproxy/66286f5e16bac?type=socks5", "json": False, "protocol": "socks5"},
            {"url": "https://advanced.name/freeproxy/66286f5e16bac?type=http", "json": False, "protocol": "http"}
        ])
        if cookie:
            self.cokie = cookie
            self.user_agent = "Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0"
            self.proxy = None
        else:
            self.proxy = None
            self.renew_proxy()

    def renew_proxy(self):
        if (self.proxy):
            self.helper.black_list_proxy(self.proxy)
            #if(self.proxyArray and self.proxy in self.proxyArray):
                #self.proxyArray.remove(self.proxy)
        if (len(self.proxyArray) > 0):
            self.proxy = self.proxyArray[self.proxyIndex]
            self.proxyIndex += 1
            if self.proxyIndex >= len(self.proxyArray):
                self.proxyIndex = 0
        else:
            self.proxy = self.helper.get_proxy()

    def payload(self, keyword, st_page=0, pasize=10):

        params = (
            ("q", keyword),
            ("as_ylo", str(self.start_year)),
            ("as_yhi", str(self.end_year)),
            #("lookup",'0'),
            #("as_sdt",'0,5')
            #("start", str(st_page*pasize)),
        )
        payload_str = urllib.parse.urlencode(params, safe=':+')

        time.sleep(self.api_wait+random.random())
        if(self.cokie):
            time.sleep(self.api_wait + random.random())
            if(len(self.proxyArray)>0):
                self.proxy = self.proxyArray[self.proxyIndex]
            response = requests.get(
                "https://scholar.google.com/scholar",
                params=payload_str,
                headers={
                    "accept": "application/json",
                    "Cookie": self.cokie,
                    "User-Agent":self.user_agent,
                },
                timeout=30,
            )
            soup = BeautifulSoup(response.text, "html.parser")
            return soup
        soup = None
        while not soup:
            try:
                response = requests.get(
                    "https://scholar.google.com/scholar",
                    params=params,
                    headers={
                        "accept": "application/json",
                        "User-Agent": user_agent.generate_user_agent(),
                        # "Cookie": self.cokie
                    },
                    proxies={"https": self.proxy},
                    timeout=30
                )
                soup = BeautifulSoup(response.text, "html.parser")
                self.renew_proxy()
            except Exception as e:
                print(e)
                self.renew_proxy()
        return soup

    def citations(self,citeurl,paper_year):
        time.sleep(self.api_wait+random.random())
        search = None
        if (self.cokie):
            time.sleep(self.api_wait + random.random())
            response = requests.get(
                "https://scholar.google.com" + citeurl + "&as_ylo=" + str(paper_year) + "&as_yhi=" + str(
                    paper_year + self.year_dept),
                headers={
                    "accept": "application/json",
                    "User-Agent": user_agent.generate_user_agent(),
                    "Cookie": self.cokie
                },
                timeout=30
            )

            citesoup = BeautifulSoup(response.text, "html.parser")
            search = citesoup.find(
                "div", {"id": "gs_ab_md"}
            )
        while not search:
            try:
                response = requests.get(
                    "https://scholar.google.com" + citeurl + "&as_ylo=" + str(paper_year) + "&as_yhi=" + str(
                        paper_year + self.year_dept),
                    headers={
                        "accept": "application/json",
                        "User-Agent": user_agent.generate_user_agent()
                        # "Cookie": self.cokie
                    },
                    proxies={"https": self.proxy},
                    timeout=30
                )
                print("https://scholar.google.com" + citeurl + "&as_ylo=" + str(paper_year) + "&as_yhi=" + str(
                        paper_year + self.year_dept))
                citesoup = BeautifulSoup(response.text, "html.parser")
                search = citesoup.find(
                    "div", {"id": "gs_ab_md"}
                )
                self.renew_proxy()
            except Exception as e:
                print(e)
                self.renew_proxy()

        

        if not search :
            print(citesoup)
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
        self.start_year = paper_year-1
        self.end_year = int(paper_year)

        search = None
        while not search:
            scholar_soup = self.payload(
                paper_name, st_page=0, pasize=1
            )
            try:
                lowbar = scholar_soup.find("div", {"class": "gs_fl gs_flb gs_invis"})
                if(lowbar):
                    search = lowbar.contents[4]["href"]
                else:
                    hibar = scholar_soup.findAll("div", {"class": "gs_fl gs_flb"})
                    if(hibar):
                        search = hibar[0].contents[4]["href"]
                    else:
                        print("Switiching to proxy")
                        self.renew_proxy()
            except Exception as e:
                print(e)
                self.renew_proxy()

        retorno = self.citations(search, int(paper_year))

        return retorno

