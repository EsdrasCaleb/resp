from pytrends.request import TrendReq
import user_agent
import requests
import json
import random
import time

from pytrends import exceptions

class Trends(object):

    def __init__(self,api_wait=2,headers = []):
        if(headers == []):
            headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
                            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                            "Accept-Language": "pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3",
                            "Accept-Encoding": "gzip, deflate, br",
                            "Connection": "keep-alive",
                            "Cookie": "__utmz=84675036.1711659203.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=84675036.1424190668.1711659203.1711659203.1711717975.2; __utmc=84675036; __utmt=1; __utmb=84675036.5.10.1711717975; SID=g.a000fwjdPyiS_5fwzV6Cn9F6b1646EmLoDETMe_We1-KF3EUh_b-M3GeV2XkbjsK8ELcrln_MwACgYKAaESAQASFQHGX2Mi2ZVIjKL1Xg1go-jw4jUEsRoVAUF8yKrzV01LTSDw1eoRYjGSPIux0076; __Secure-1PSID=g.a000fwjdPyiS_5fwzV6Cn9F6b1646EmLoDETMe_We1-KF3EUh_b-xQLD6v9eUcKWJ9u-oKkwuAACgYKAe8SAQASFQHGX2MiEHwsOD5soOlwVDGZYcUynBoVAUF8yKq6CJNIleUccIYW7FQPHAcm0076; __Secure-3PSID=g.a000fwjdPyiS_5fwzV6Cn9F6b1646EmLoDETMe_We1-KF3EUh_b-FEuxGp-Bi7CnDdLafzROSgACgYKAdESAQASFQHGX2MiqUm-we3Bqvz4J19j1F5iJhoVAUF8yKpFGhg9Ua24m0-QaPcCS0bb0076; HSID=AWR9pmQL4A9yh7vCa; SSID=AuoPZtlJjEC1jB-BN; APISID=BVVCSeoJpRUo8UTf/AE-v7WqsnEnsdnv1F; SAPISID=9sgP3SUeuk9j7ZlH/Amzk0n87cJU5fnVC2; __Secure-1PAPISID=9sgP3SUeuk9j7ZlH/Amzk0n87cJU5fnVC2; __Secure-3PAPISID=9sgP3SUeuk9j7ZlH/Amzk0n87cJU5fnVC2; NID=512=tXenHtT0UCkIAlsI9MoGYE0eNtU9BkH_spCpqS993VKiNAoym0q_v_11keSPcZ-EnqYXZ4wKDwowSVX9Yd5SEx33-nA8B761uNe2j2ShSmfGGzC7cXDVLk4Ag0W0kkg2_KjDr8rtA2tXfuP89EQ3eDCmRQ4F1yCNo5uPdjHtvvQ; _gid=GA1.4.574535451.1711659205; _ga=GA1.4.1138266163.1711659204; _ga_VWZPXDNJJB=GS1.1.1711717975.2.1.1711718272.0.0.0; _gat_gtag_UA_4401283=1",
                            "Upgrade-Insecure-Requests": "1",
                            "Sec-Fetch-Dest": "document",
                            "Sec-Fetch-Mode": "navigate",
                            "Sec-Fetch-Site": "none",
                            "Sec-Fetch-User": "?1"
                            }
        self.headers = headers
        self.token = "APP6_UEAAAAAZgcepkb7CY0HX7URNljrpb2SCIwIvkgV"
        self.api_wait = api_wait

    def serach5(self,keyword,token,useragent):
        standardurl = "https://trends.google.com.br/trends/api/widgetdata/multiline"
        array_keyword = []
        for key in keyword:
            array_keyword.append(
                  {
                     "geo":{

                     },
                     "complexKeywordsRestriction":{
                        "keyword":[
                           {
                              "type":"BROAD",
                              "value":key
                           }
                        ]
                     }
                  })

        params = {
            "hl" : "pt-BR",
            "tz" : [180,180],
            "req" : {
               "time":"2004-01-01 2023-12-31",
               "resolution":"MONTH",
               "locale":"pt-BR",
               "comparisonItem":array_keyword,
               "requestOptions":{
                  "property":"",
                  "backend":"IZG",
                  "category":0
               },
               "userConfig":{
                  "userType": "USER_TYPE_LEGIT_USER"
               }
            },
            "token" : self.token,
        }

        header = {
            "accept": "application/json",
            "User-Agent": useragent
        }

        time.sleep(self.api_wait + random.random())
        response = requests.get(
            standardurl,
            params=params,
            headers=self.headers
        )
        print(response.text)
        return response.json()


    def payload(self, keyword):
        trends_header = self.headers
        waittimer = self.api_wait

        class TrendReqA(TrendReq):

            def _get_data(self, url, trim_chars=0, **kwargs):
                GET_METHOD = 'get'
                return super()._get_data(url, trim_chars=trim_chars, headers=trends_header, **kwargs)
        pytrends = TrendReqA(hl='pt-Br', tz=360, timeout=(10, 25), retries=0, backoff_factor=0)
        pytrends.build_payload(kw_list=[keyword], timeframe=['2004-01-01 2021-12-31'])
        return pytrends.interest_over_time()



    def query(
        self,
        keyword
    ):
        trend_soup = self.payload(
            keyword
        )

        return trend_soup