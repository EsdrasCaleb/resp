import time

from resp.apis.acm_api import ACM
from resp.apis.ieee_api import IEEE
from resp.apis.scholar_api import Scholar
from resp.apis.trends_api import Trends
from pytrends.request import TrendReq
import random
import time
import csv
import json
from datetime import datetime
from db_paper import db_paper
from proxy_helper import proxy_helper

helper = proxy_helper([
    {"url": "https://advanced.name/freeproxy/662b6ca41c1ae?type=https","protocol":"https","json":False},
    {"url": "https://advanced.name/freeproxy/662b6ca41c1ae?type=socks4","json":False,"protocol":"socks4"},
    {"url": "https://advanced.name/freeproxy/662b6ca41c1ae?type=socks5","json":False,"protocol":"socks5"},
    {"url": "https://advanced.name/freeproxy/662b6ca41c1ae?type=http","protocol":"http","json":False},
])

db = db_paper(host="db", user="root", password="example", db="papersplease")
db.connect()
cursor = db.ctx.cursor()
query = ("SELECT keyword.name as name,keyword.id as id,"
         "count(distinct keyword_paper.paper_id) as counter "
         #"sum(keyword_trend.value) as error_metric "
         "FROM keyword "
         " join keyword_paper on keyword.id = keyword_paper.keyword_id "
         " join citations on citations.paper_id=keyword_paper.paper_id "
         #" join keyword_trend on keyword_trend.keyword_id=keyword.id "
         " WHERE keyword.id not in (SELECT keyword_id from keyword_trend) and name<>''"
         #" where name<>'' and keyword.id>37504 "
         " GROUP BY keyword.id,keyword.name"
         #" HAVING error_metric =0"
         " ORDER BY counter DESC"
         )


cursor.execute(query)
dataG = cursor.fetchall()
colums = cursor.column_names
cursor.close()
db.close()


end = False
index = 0

proxy = helper.get_proxy()
print(len(dataG))
while not end:
    term = dataG[index]
    termob = dict(zip(colums, term))
    try:
        pytrends = TrendReq(hl='pt-Br', tz=360, timeout=(30,60), retries=0, backoff_factor=0,
                                    proxies=[proxy], requests_args={'verify':False})


        pytrends.build_payload(kw_list=[termob["name"]], timeframe=['2004-01-01 2022-01-01'])
        result =json.loads(pytrends.interest_over_time().to_json())

        keys = list(result.keys())
        db.connect()
        if (len(keys) > 0):
            for data in result[keys[0]].keys():
                dt_object = datetime.fromtimestamp(int(data) / 1000)
                db.insert_update_trends(termob["id"], dt_object.year, dt_object.month, result[keys[0]][data])
            print(termob["name"], termob["id"], "inserido")
        else:
            for ano in range(2004, 2023):
                for mes in range(1, 13):
                    db.insert_update_trends(termob["id"], ano, mes, 0, True)
        index += 1
        db.close()
    except Exception as e:
        print("error",e)
        print(index, termob["name"], termob["id"])
        helper.black_list_proxy(proxy)
        proxy = helper.get_proxy()

    if(index == len(dataG)):
        end = True

print("Done")

