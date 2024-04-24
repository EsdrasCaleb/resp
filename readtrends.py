import time

from resp.apis.acm_api import ACM
from resp.apis.ieee_api import IEEE
from resp.apis.scholar_api import Scholar
import requests
from pytrends.request import TrendReq
import random
import time
import csv
import json
from datetime import datetime
from db_paper import db_paper
from fp.fp import FreeProxy

db = db_paper(host="db", user="root", password="example", db="papersplease")
db.connect()
cursor = db.ctx.cursor()
query = ("SELECT keyword.name as name,keyword.id as id,count(distinct keyword_paper.paper_id) as counter FROM keyword "
         " join keyword_paper on keyword.id = keyword_paper.keyword_id "
         " join citations on citations.paper_id=keyword_paper.paper_id "
         " WHERE keyword.id not in (SELECT keyword_id from keyword_trend) and name<>'' "
         " GROUP BY keyword.id,keyword.name"
         #" HAVING counter >100"
         " ORDER BY counter DESC")

blacklist = []

cursor.execute(query)
dataG = cursor.fetchall()
colums = cursor.column_names
cursor.close()
db.close()

end = False
index = 0



proxy = ["http://104.207.50.188:3128", "http://104.207.43.133:3128", "http://104.207.43.184:3128", "http://104.207.60.157:3128", "http://104.207.33.213:3128", "http://104.207.46.38:3128", "http://104.207.60.55:3128", "http://104.207.56.179:3128", "http://104.207.34.84:3128", "http://104.167.29.124:3128", "http://104.207.55.200:3128", "http://104.207.38.23:3128", "http://104.207.40.0:3128", "http://104.207.36.187:3128", "http://104.207.43.208:3128", "http://104.207.41.171:3128", "http://104.207.52.105:3128", "http://104.207.39.225:3128", "http://104.167.30.107:3128", "http://104.207.57.68:3128", "http://104.167.31.107:3128", "http://104.207.62.182:3128", "http://104.207.45.99:3128", "http://104.207.53.0:3128", "http://104.207.50.22:3128", "http://104.207.45.73:3128", "http://104.207.51.51:3128", "http://104.167.30.166:3128", "http://104.207.56.107:3128", "http://104.207.45.217:3128", "http://104.167.25.234:3128", "http://104.167.25.167:3128", "http://104.207.57.240:3128", "http://104.207.51.244:3128", "http://104.207.34.61:3128", "http://104.207.53.53:3128", "http://104.207.33.238:3128", "http://104.207.37.23:3128", "http://104.207.49.69:3128", "http://104.207.55.230:3128", "http://104.167.27.28:3128", "http://104.207.39.43:3128", "http://104.207.35.137:3128", "http://104.167.28.187:3128", "http://104.167.29.2:3128", "http://104.167.28.182:3128", "http://104.167.28.210:3128", "http://104.207.51.179:3128", "http://104.207.42.197:3128", "http://104.207.33.73:3128", "http://104.207.49.209:3128", "http://104.167.30.175:3128", "http://104.167.25.157:3128", "http://104.207.37.29:3128", "http://104.207.38.172:3128", "http://104.207.55.13:3128", "http://104.207.38.120:3128", "http://104.207.44.156:3128", "http://104.207.43.199:3128", "http://104.207.32.132:3128", "http://104.207.46.229:3128", "http://104.207.57.212:3128", "http://104.207.61.86:3128", "http://104.207.40.165:3128", "http://104.167.28.219:3128", "http://104.207.62.252:3128", "http://104.207.58.233:3128", "http://104.207.41.166:3128", "http://104.207.44.114:3128", "http://104.167.28.174:3128", "http://104.207.49.178:3128", "http://104.207.54.150:3128", "http://104.207.57.193:3128", "http://104.207.58.128:3128", "http://104.167.28.123:3128", "http://104.207.51.94:3128", "http://104.207.48.57:3128", "http://104.207.57.121:3128", "http://104.167.28.8:3128", "http://104.167.28.199:3128", "http://104.207.32.95:3128", "http://104.207.36.232:3128", "http://104.207.38.189:3128", "http://104.167.30.125:3128", "http://104.207.54.209:3128", "http://104.207.57.4:3128", "http://104.167.27.102:3128", "http://104.207.51.200:3128", "http://104.167.28.186:3128", "http://104.207.41.206:3128", "http://104.207.63.139:3128", "http://104.207.56.89:3128", "http://104.207.32.167:3128", "http://104.207.52.109:3128", "http://104.207.40.100:3128", "http://104.207.56.134:3128", "http://104.207.55.196:3128", "http://104.207.51.90:3128", "http://104.207.41.149:3128", "http://104.207.63.70:3128"]
proxyindex = 0
maxProxies = 1000
print(len(dataG))
while not end:
    term = dataG[index]

    try:

        pytrends = TrendReq(hl='pt-Br', tz=360, timeout=(60, 120), retries=0, backoff_factor=0.1,
                                proxies=proxy, requests_args={'verify':False})
        termob = dict(zip(colums, term))
        pytrends.build_payload(kw_list=[termob["name"]], timeframe=['2004-01-01 2022-01-01'])
        result =json.loads(pytrends.interest_over_time().to_json())

        keys = list(result.keys())
        db.connect()
        for data in result[keys[0]].keys():
            dt_object = datetime.fromtimestamp(int(data)/1000)
            db.insert_update_trends(termob["id"], dt_object.year, dt_object.month, result[keys[0]][data])
        print(termob["name"], termob["id"], "inserido")
        db.close()
    except Exception as e:
        print("error",e,index,term)
        for ano in range(2004,2023):
            for mes in range(1,13):
                db.insert_update_trends(termob["id"], ano, mes, 0,True)
    index += 1
    if (index >= len(dataG)):
        end = True

print("Done")
