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
    {"url": "https://advanced.name/freeproxy/66286f5e16bac?type=https","protocol":"https","json":False},
    {"url": "https://advanced.name/freeproxy/66286f5e16bac?type=socks4","json":False,"protocol":"socks4"},
    {"url": "https://advanced.name/freeproxy/66286f5e16bac?type=socks5","json":False,"protocol":"socks5"}
])

db = db_paper(host="db", user="root", password="example", db="papersplease")
db.connect()
cursor = db.ctx.cursor()
query = ("SELECT keyword.name as name,keyword.id as id,count(distinct keyword_paper.paper_id) as counter FROM keyword "
         " join keyword_paper on keyword.id = keyword_paper.keyword_id "
         " join citations on citations.paper_id=keyword_paper.paper_id "
         " WHERE keyword.id not in (SELECT keyword_id from keyword_trend) and name<>'' "
         " GROUP BY keyword.id,keyword.name"
         " ORDER BY counter DESC")

cursor.execute(query)
dataG = cursor.fetchall()
colums = cursor.column_names
cursor.close()
db.close()


end = False
index = 0

proxy = helper.get_proxy()
while not end:
    term = dataG[index]
    try:
        pytrends = TrendReq(hl='pt-Br', tz=360, timeout=(45,100), retries=0, backoff_factor=0,
                                    proxies=[proxy], requests_args={'verify':False})

        termob = dict(zip(colums, term))
        pytrends.build_payload(kw_list=[termob["name"]], timeframe=['2004-01-01 2022-01-01'])
        result =json.loads(pytrends.interest_over_time().to_json())

        keys = list(result.keys())
        db.connect()
        for data in result[keys[0]].keys():
            dt_object = datetime.fromtimestamp(int(data)/1000)
            print(termob["name"],termob["id"],dt_object.year, dt_object.month, result[keys[0]][data])
            db.insert_update_trends(termob["id"], dt_object.year, dt_object.month, result[keys[0]][data])
        index += 1
        db.close()
        time.sleep(5+random.random())
    except Exception as e:
        print("error",e)
        helper.black_list_proxy(proxy)
        proxy = helper.get_proxy()

    if(index == len(dataG)):
        end = True

print("Done")

