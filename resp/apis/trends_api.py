from pytrends.request import TrendReq
import time


class Trends(object):

    def __init__(self,api_wait=5,headers = []):
        if(headers == []):
            headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0",
                            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                            "Accept-Language": "pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3",
                            "Accept-Encoding": "gzip, deflate, br",
                            "Connection": "keep-alive",
                            "Cookie": "__utma=84675036.1642905141.1711122214.1711193083.1711197850.4; __utmz=84675036.1711193083.3.2.utmcsr=trends.google.com.br|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmc=84675036; __utmb=84675036.1.10.1711197850; NID=512=RHpMQWfUD08XjRZq8uvjdET2i_EX4V4jhDpiqF3Grk5Keo9dxT6iWyljhfnw1myMqjLvPLo4uE12vTickMvWj2TOFuYslt1nCqrHqbDjk_JtvBET8xvDXRizomXif21vwrZSjiky2AVpsA5RRySGx2TQG1joHn6aqs3Fmo3x1R2F7hEHeqjGC5lbNgahsBhkNT2vUv4OVoQjKUiNuubU3Hu1wKtm8DqrNgKuCkSUtTYmuCkfGMoMRh0BjOSc6FWFlmpoMpgGoYhYq1VOcmg5zzPFTFhjS25IPyM5FQozIwYr1Y2SHqas0LLGjGsMIrbsjsHVXMUt0C2A82rgqule5z6p-s89zoM4M2O0zRNjnTFgfW5Bo_3slcVPr-C3OfvojNRQ0f4W5VJQf3KEmWFC3yf0wXXaJdGp4rPqWP37hGN_8g7igCloipOsWdNj_Hh0OBYJnxUqMb07F6uBJBwys84tf-CDf0vIPs-a6ykVO9PB-_T0E-EpYMzBpnoY73ZUZUHn8-N9Wh-t74rHtqreHUHsAbsct_OR1QyfjpFQa8-0gYPWaVytcA; SID=g.a000hwiw8mWaWz-JJQ7EkAAt3BqQ6_JarxYOiKw0HwYHVRnMbAze2ZhGJSsw3u96egHS8l_DnwACgYKARYSAQASFQHGX2MixOcpeIUvLCWscMbZ4BB3nRoVAUF8yKo4HBlWqp5Zqmsw1hwAzPpl0076; __Secure-1PSID=g.a000hwiw8mWaWz-JJQ7EkAAt3BqQ6_JarxYOiKw0HwYHVRnMbAzeycmqFnv3r3LaZHWgBr6H0AACgYKAZQSAQASFQHGX2MiMl4q32hh4G7BGfW00OhDkxoVAUF8yKr0vBT4pRACqqQusxGNwE2A0076; __Secure-3PSID=g.a000hwiw8mWaWz-JJQ7EkAAt3BqQ6_JarxYOiKw0HwYHVRnMbAzemSe-szt5jAMlFkrwBrPpHQACgYKAfkSAQASFQHGX2MiCAL6gHshElWP185oEkMZShoVAUF8yKrLdpM7PWxmEiN8EQRqFjbT0076; HSID=A9HuG1IG2K1njZ6NL; SSID=AktvJ49egrFkAsB9Q; APISID=1FQQAOetMu2Z_nqC/AB7a9Qt-I2eJzvrcu; SAPISID=OtI8AuS7T1j8PckO/AlrnvEvuaWMfkDjk4; __Secure-1PAPISID=OtI8AuS7T1j8PckO/AlrnvEvuaWMfkDjk4; __Secure-3PAPISID=OtI8AuS7T1j8PckO/AlrnvEvuaWMfkDjk4; AEC=Ae3NU9OF_OYwf9eU5OwtFrq8szMqnQm2YdJN-5AGTWqegSlJ4u01QLbHuA; ANID=AHWqTUnkUYW01cBBJ4QQxTVKYISfSur_kRVVJWuIVmBdA5RRa9JeT5Uk_-GBqur0; 1P_JAR=2024-03-20-23; SEARCH_SAMESITE=CgQI2poB; _ga_VWZPXDNJJB=GS1.1.1711197849.5.1.1711197851.0.0.0; _ga=GA1.4.1642905141.1711122214; _gid=GA1.4.1804341020.1711122214; OTZ=7480304_68_68__68_",
                            "Upgrade-Insecure-Requests": "1",
                            "Sec-Fetch-Dest": "document",
                            "Sec-Fetch-Mode": "navigate",
                            "Sec-Fetch-Site": "none",
                            "Sec-Fetch-User": "?1"
                            }
        self.headers = headers
        self.api_wait = api_wait

    def payload(self, keyword):
        trends_header = self.headers
        class TrendReqA(TrendReq):

            def _get_data(self, url, trim_chars=0, **kwargs):
                GET_METHOD = 'get'
                return super()._get_data(url, trim_chars=trim_chars, headers=trends_header, **kwargs)
        pytrends = TrendReqA()
        pytrends.build_payload(kw_list=[keyword], timeframe=['2004-01-01 2021-12-31'])
        return pytrends.interest_over_time()



    def query(
        self,
        keyword
    ):
        time.sleep(self.api_wait)
        trend_soup = self.payload(
            keyword
        )

        return trend_soup