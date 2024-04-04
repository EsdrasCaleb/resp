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
from fp.fp import FreeProxy

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
proxiOpen = ['http://pommetvh:o73b5ipcaqia@2.56.119.93:5074',
                'http://pommetvh:o73b5ipcaqia@185.199.229.156:7492',
                'http://pommetvh:o73b5ipcaqia@185.199.228.220:7300',
                'http://pommetvh:o73b5ipcaqia@185.199.231.45:8382',
                'https://7b0c03df015c987fdb49e1300c94c8f3:YLyqHCDkTaUor5S2@credibility-ru.tlsext.com:10799',
                'https://7b0c03df015c987fdb49e1300c94c8f3:YLyqHCDkTaUor5S2@union-us.tlsext.com:10799',
                 'https://7b0c03df015c987fdb49e1300c94c8f3:YLyqHCDkTaUor5S2@hide-fr.tlsext.com:10799',
                 'https://7b0c03df015c987fdb49e1300c94c8f3:YLyqHCDkTaUor5S2@octothorp-uk.tlsext.com:10799',
                 'https://7b0c03df015c987fdb49e1300c94c8f3:YLyqHCDkTaUor5S2@sympathy-us.tlsext.com:10799',
                 'https://7b0c03df015c987fdb49e1300c94c8f3:YLyqHCDkTaUor5S2@retirement-nl.tlsext.com:10799',
                 'https://7b0c03df015c987fdb49e1300c94c8f3:YLyqHCDkTaUor5S2@greet-sg.tlsext.com:10799',
                 'https://7b0c03df015c987fdb49e1300c94c8f3:YLyqHCDkTaUor5S2@consequently-sg.tlsext.com:10799',
                 'https://UVPNv3-td6gqggyx0zvxpvzdobws6hzugfb60cd2mdelutg9lm91uv3pckev80h2wfb6322&12359007:yopiu4b87qctvj1gqui53eml04wrt35uott2qvodkar5g3e3du3b7w35qyrfg23f@de103.uvpn.me:433',
                 'https://UVPNv3-td6gqggyx0zvxpvzdobws6hzugfb60cd2mdelutg9lm91uv3pckev80h2wfb6322&12359007:yopiu4b87qctvj1gqui53eml04wrt35uott2qvodkar5g3e3du3b7w35qyrfg23f@de105.uvpn.me:433',
                 'https://UVPNv3-td6gqggyx0zvxpvzdobws6hzugfb60cd2mdelutg9lm91uv3pckev80h2wfb6322&12359007:yopiu4b87qctvj1gqui53eml04wrt35uott2qvodkar5g3e3du3b7w35qyrfg23f@it107.uvpn.me:433',
                 'https://UVPNv3-td6gqggyx0zvxpvzdobws6hzugfb60cd2mdelutg9lm91uv3pckev80h2wfb6322&12359007:yopiu4b87qctvj1gqui53eml04wrt35uott2qvodkar5g3e3du3b7w35qyrfg23f@sp181.uvpn.me:433',
                 'https://UVPNv3-td6gqggyx0zvxpvzdobws6hzugfb60cd2mdelutg9lm91uv3pckev80h2wfb6322&12359007:yopiu4b87qctvj1gqui53eml04wrt35uott2qvodkar5g3e3du3b7w35qyrfg23f@ua133.uvpn.me:433',
                 'https://access_token:CAESKAoIdG91Y2h2cG4QmKOZswYYmZW01QYiEGUyNzE4MGZlNWMyODE3MTUaIG613BLMX8XISgGTGE7uv4AGqrJF2wjoLEeSqfNI83Zj@ext-ms-ex-fr-par-pr-p-7.northghost.com:433',
                 'https://access_token:yopiu4b87qctvj1gqui53eml04wrt35uott2qvodkar5g3e3du3b7w35qyrfg23f@ext-ms-ex-gb-lon-pr-p-1.northghost.com:433']
proxies = [
                "socks5://ubhvovau:2ujo9w8p47l1@38.154.227.167:5868",
                "socks5://ubhvovau:2ujo9w8p47l1@185.199.229.156:7492",
                "socks5://ubhvovau:2ujo9w8p47l1@185.199.228.220:7300",
                "socks5://ubhvovau:2ujo9w8p47l1@185.199.231.45:8382",
                "socks5://ubhvovau:2ujo9w8p47l1@188.74.210.207:6286",
                "socks5://ubhvovau:2ujo9w8p47l1@188.74.183.10:8279",
                "socks5://ubhvovau:2ujo9w8p47l1@188.74.210.21:6100",
                "socks5://ubhvovau:2ujo9w8p47l1@45.155.68.129:8133",
                "socks5://ubhvovau:2ujo9w8p47l1@154.95.36.199:6893",
                "socks5://ubhvovau:2ujo9w8p47l1@45.94.47.66:8110",
                ''
            ]

end = False
index = 0

blacklist = []

proxy = None
while not end:
    term = dataG[index]
    try:
        while not proxy:
            proxy = FreeProxy(https=True, rand=True).get()
            if proxy in blacklist:
                proxy = None
            else:
                pytrends = TrendReq(hl='pt-Br', tz=360, timeout=(10, 25), retries=0, backoff_factor=0,
                                    proxies=[proxy])

        termob = dict(zip(colums, term))
        pytrends.build_payload(kw_list=[termob["name"]], timeframe=['2004-01-01 2022-01-01'])
        result =json.loads(pytrends.interest_over_time().to_json())

        keys = list(result.keys())

        for data in result[keys[0]].keys():
            dt_object = datetime.fromtimestamp(int(data)/1000)
            print(termob["name"],termob["id"],dt_object.year, dt_object.month, result[keys[0]][data])
            db.insert_update_trends(termob["id"], dt_object.year, dt_object.month, result[keys[0]][data])
        index += 1
        time.sleep(5+random.random())
    except Exception as e:
        print("error",e)
        if(proxy):
            blacklist.append(proxy)
        print(blacklist)
        proxy = None

    if(index == len(dataG)):
        end = True
db.close()
print("Done")
print(blacklist)
