import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import time
import random
from fp.fp import FreeProxy

class ACM(object):
    def __init__(self):
        self.api_wait_max = 5
        self.api_wait_min = 6
        self.mounths = {
            "Jan":1, "Feb":2, "Mar":3, "Apr":4, "Jun":6, "Jul":7,"Aug":8, "Sep":9, "Oct":10, "Nov":11, "Dec":12,
            "January":1,"February":2,"March":3,"April":4,"May":5,"June":6,"July":7,"August":8,
            "September":9, "October":10, "November":11, "December":12
        }
        self.proxies = ["socks5://ubhvovau:2ujo9w8p47l1@38.154.227.167:5868",
                "socks5://ubhvovau:2ujo9w8p47l1@185.199.229.156:7492",
                "socks5://ubhvovau:2ujo9w8p47l1@185.199.228.220:7300",
                "socks5://ubhvovau:2ujo9w8p47l1@185.199.231.45:8382",
                "socks5://ubhvovau:2ujo9w8p47l1@188.74.210.207:6286",
                "socks5://ubhvovau:2ujo9w8p47l1@188.74.183.10:8279",
                "socks5://ubhvovau:2ujo9w8p47l1@188.74.210.21:6100",
                "socks5://ubhvovau:2ujo9w8p47l1@45.155.68.129:8133",
                "socks5://ubhvovau:2ujo9w8p47l1@154.95.36.199:6893",
                "socks5://ubhvovau:2ujo9w8p47l1@45.94.47.66:8110",
                      ]
        self.proxy = ''
        self.proxy_index = 0
        self.renew_proxy()


    def renew_proxy(self):
        time.sleep(2000)
        if(len(self.proxies) <= self.proxy_index):
            self.proxy_index = 0
        self.proxy = self.proxies[self.proxy_index]
        self.proxy_index += 1

    def payload(self, keyword,st_page=0, pasize=50, start_year=2004, end_year=2023):

        params = (
            ("AllField", keyword),
            ("date", "all"),
            ("AfterYear", str(start_year)),
            ("BeforeYear", str(end_year)),
            ("queryID", "45/3852851837"),
            ("sortBy", "relevancy"),
            ("startPage", str(st_page)),
            ("pageSize", str(pasize)),
        )
        response = None
        while not response:
            try:
                response = requests.get(
                    "https://dl.acm.org/action/doSearch",
                    params=params,
                    headers={"accept": "application/json"},
                    verify=False,
                    #proxies={"https": self.proxy,"http": self.proxy},
                )
            except Exception as e:
                print("error")
                response = None
                self.renew_proxy()
                print(e)

        soup = BeautifulSoup(response.text, "html.parser")

        return soup

    def all_articles(self, st_page=0, pasize=50, start_year=2004, end_year=2021,min_mouth=0,
        max_mouth=12,order="relevancy"):

        params = (
            ("expand", "dl"), #dl all
            ("AfterMonth",str(min_mouth)),
            ("AfterYear", str(start_year)),
            ("BeforeMonth", str(max_mouth)),
            ("BeforeYear", str(end_year)),
            ("ContentItemType", "research-article"),
            ("startPage", str(st_page)),
            ("pageSize", str(pasize)),
            ("sortBy", order),
        )
        response = None

        while not response:
            try:
                response = requests.get(
                    "https://dl.acm.org/action/doSearch",
                    params=params,
                    headers={"accept": "application/json"},
                    verify=False,
                    #proxies={"https": self.proxy,"http": self.proxy},
                )
            except Exception as e:
                print("error")
                response = None
                self.renew_proxy()
                print(e)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup

    def soup_html(self, soup):
        all_papers = []
        main_class = soup.find(
            "div", {"class": "col-lg-9 col-md-9 col-sm-8 sticko__side-content"}
        )

        main_c = main_class.find_all("li", {"class": "search__item issue-item-container"})
        
        for paper_ob in main_c:
            doi_url = ["https://dl.acm.org", "doi", "pdf"]
            try:
                paper = paper_ob.find("div", {"class": "issue-item__content"})
                content_ = paper.find("h5", {"class": "issue-item__title"})
                citation = paper.find("span", {"class": "citation"})
                paper_url = content_.find("a", href=True)["href"]
                all_papers.append({"url":paper_url,"citation":citation.text.replace("Total Citations","").replace('.',"").replace(',',"")})
            except Exception as e:
                print("error")
                print(e)
        return all_papers

    def get_paperdata(self,paperurl):
        time.sleep(self.api_wait_min + random.random())
        response = None
        while not response:
            try:
                response = requests.get(
                     "https://dl.acm.org"+paperurl,
                    headers={"accept": "application/json"},
                    #proxies={"https": self.proxy[random.randint(0, len(self.proxy))]}
                )
            except Exception as e:
                print("error")
                response = None
                print(e)
        soup = BeautifulSoup(response.text, "html.parser")
        terms = soup.find("div", {"class": "citation article__section article__index-terms"})
        terms_array = []
        term_data = terms.find_all("a")
        for term in term_data:
            terms_array.append(term.text)
        paper_data = {"terms":terms_array}

        if(soup.find("h1", {"class": "citation__title"})):
            paper_data["title"] = soup.find("h1", {"class": "citation__title"}).text
            year_data = soup.find("span", {"class": "CitationCoverDate"}).text.split(" ")
            paper_data["year"] = year_data[2]
            paper_data["mounth"] = self.mounths[year_data[1]]
            paper_data["origin"] = soup.find("span", {"class": "epub-section__title"}).text
            paper_data["doi"] = "/".join(paperurl.split("/")[2:])
            paper_data["authors"] = len(soup.find_all("span", {"class": "loa__author-name"}))
            pagedata = soup.find("div", {"class": "pageRange"}).text.replace("Pages ","").split("-")
            paper_data["pages"] = int(pagedata[1])-int(pagedata[0])+1
            paper_data["references"] = len(soup.find_all("li", {"class": "references__item"}))
        else:
            print("https://dl.acm.org"+paperurl)
            return None

        return paper_data


    def all_paper(self,start_page=0,max_pages=5,pagesize=50,
        min_year=2004,
        max_year=2021,
        min_mouth=0,
        max_mouth=12,
        order="relevance"
        ):
        "all acm paper"
        all_pages = []

        for page in tqdm(range(max_pages)):
            #time.sleep(self.api_wait_min + random.random())
            acm_soup = self.all_articles(
                st_page=page+start_page, pasize=pagesize, start_year=min_year, end_year=max_year,
                min_mouth=min_mouth,max_mouth=max_mouth,order=order
            )
            if (acm_soup.find("li", {"class": "search__item issue-item-container"})):
                acm_result = self.soup_html(acm_soup)
                all_pages += acm_result
            else:
                break


        return all_pages
    def query(
        self,
        keyword,
        max_pages=5,
        min_year=2015,
        max_year=2021,
    ):
        "acm final call"
        all_pages = []

        for page in tqdm(range(max_pages)):
            acm_soup = self.payload(
                keyword, st_page=page, pasize=50, start_year=min_year, end_year=max_year
            )
            if(acm_soup.find("li", {"class": "search__item issue-item-container"})):
                acm_result = self.soup_html(acm_soup)
                all_pages += acm_result
                time.sleep(self.api_wait_min + random.random())
            else:
                break

        return all_pages