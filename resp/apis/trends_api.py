from pytrends.request import TrendReq
import time
import json
import pandas as pd
import requests

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from requests import status_codes

from pytrends import exceptions

class Trends(object):

    def __init__(self,api_wait=5,headers = []):
        if(headers == []):
            headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0",
                            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                            "Accept-Language": "pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3",
                            "Accept-Encoding": "gzip, deflate, br",
                            "Connection": "keep-alive",
                            "Cookie": "__utma=10102256.266499014.1711329929.1711329935.1711364173.2; __utmz=10102256.1711329935.1.1.utmcsr=trends.google.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmc=10102256; NID=512=Fkm2jAGb35UbcfDpoSUK8Xq8qYvMouqi4NEEtdi2WE6-2_DuNY17psb2En8uSIFXDywWV2qWOYIWc4qZW7y6zvjfo-cbJxB3rHsGD2RcPFxShiY4H_a1LqT6a8z0qECPtpR_DavP7ayGf_vKCi8nU34X6JHIjVUqjekv5ePTb6bQp6BDyKEd0eKMU2A5NuvsxF0EPorUYj2Nh3imwViLjG4vA-mD671kl771EztsJnWrS4okFzA5Pjd96W10G83Yq_4np6NmTJCTbwpuNiqNE90WwJJa4BPA5jyvOEF4URFo8xCQHWsBdBAxJbUXd2EQvJ_Q1i0wpHCmOHYYGMstSgBdrxRSOLBkZ9emJoo38DLE9Qrr5YFe83mc_ixz7FR2SLBZqRsSlddla9ZGaT5ULPAiLSFqdc0Qg6OXw6Y0xnBwMlwJO3QAvCnkXgFjOr2ofT4v2TmuU7r2QWo3sgV_OD7AVqVeenq12sHEK2fszoTx3j1Zr5sINgCmNhxny4rj66EaAV5CUKXK8yG_LlymGUwwnNz8Vnog3dcfbWfekPwVilKioXCVPLmwW8tKWw2dyVJ_psPz13lpmJemR76zlCUBRT8CpSBaRHBO5DBfcHQw7rbJPbAGkSC4cXGZOfwsrls5GClj7WXWeSZ9rL_8raDevGPbz8OV18XT0OcqPKBWT_UfFXN7WHNhsjflgVhBUXITVYNHkSRtVsvgTdyX1Na28JIul9aMHqI5xRsHdkGpGdCuZLVEdd3ubS5stQq-nMEW8wWMRPCsrNilwSheHRQtTDHD48e98zKRa2QOFDm1zkWYrR3sVEFfNZ63MwtYNA9GQAWaj3whcWXcs9-mgSeGgwdXe0zGXZMJd8XtzChgptP3FaxKSu2dVFg9iGd9EbBut-N04NamZwQsSdKQ3L0ap2K1dWu_e3lrcIg2neIOIUmyEKdsK5bTSamGfoB-bS4CRI7xT2LyvsijVcRLogHstVS7oaS6xzmVZbvy52QZ7HXrsGD9aJw7L_wsen9u4PTa4crRBCSOabtEROGBScd2IKc4msAkpSMQs1Kd3PW5HIN2sw17gjsiAvo-kiLYyhdP85MnM0VOX27Y3FxE7uHXW5fPTglcubvVZlCWBB3jS-yXDVifqzZnxIqDUcRm6yEIXkH63IkgVvYVGjwBKiJpDKpfkpc; 1P_JAR=2024-03-25-12; SEARCH_SAMESITE=CgQI3ZoB; ANID=AHWqTUnMWdRx55Av9ABLl2GWIrI2RiR9RuoZKFufPgj97zX_cV5y63jVHDjwhQmy; AEC=Ae3NU9MPT8gahF1kgOwRZPQa1LkxMgOf_Hd4IX8JzSHj6b0MvQnlqPnn6g; SID=g.a000hwiw8mWaWz-JJQ7EkAAt3BqQ6_JarxYOiKw0HwYHVRnMbAze2ZhGJSsw3u96egHS8l_DnwACgYKARYSAQASFQHGX2MixOcpeIUvLCWscMbZ4BB3nRoVAUF8yKo4HBlWqp5Zqmsw1hwAzPpl0076; __Secure-1PSID=g.a000hwiw8mWaWz-JJQ7EkAAt3BqQ6_JarxYOiKw0HwYHVRnMbAzeycmqFnv3r3LaZHWgBr6H0AACgYKAZQSAQASFQHGX2MiMl4q32hh4G7BGfW00OhDkxoVAUF8yKr0vBT4pRACqqQusxGNwE2A0076; __Secure-3PSID=g.a000hwiw8mWaWz-JJQ7EkAAt3BqQ6_JarxYOiKw0HwYHVRnMbAzemSe-szt5jAMlFkrwBrPpHQACgYKAfkSAQASFQHGX2MiCAL6gHshElWP185oEkMZShoVAUF8yKrLdpM7PWxmEiN8EQRqFjbT0076; HSID=AvQssgkv8bTi_MJN7; SSID=A_PRG9X6FhoPiRmLL; APISID=1FQQAOetMu2Z_nqC/AB7a9Qt-I2eJzvrcu; SAPISID=OtI8AuS7T1j8PckO/AlrnvEvuaWMfkDjk4; __Secure-1PAPISID=OtI8AuS7T1j8PckO/AlrnvEvuaWMfkDjk4; __Secure-3PAPISID=OtI8AuS7T1j8PckO/AlrnvEvuaWMfkDjk4; SIDCC=AKEyXzW4bJqTUkGp5rVn4dCLpkOSBTTGvx9ZcSwENOar6BXq3aLM1SfiCdrwqrGkau06DS3VLms; __Secure-1PSIDCC=AKEyXzU8Ui48aV8JPrH26Mdcj1XOmo1IY8X0bt1Lbu3qjyh_ATEhZ1VamvuhNMVeqc46ItnqvDo; __Secure-3PSIDCC=AKEyXzVVvIm4IGejyp0zxCys0ticZx704f0grEFO5Oj-zOxY47gwkPJNDhwhIYHsepseBsv_4Qo; __Secure-1PSIDTS=sidts-CjEB7F1E_KwE2LrChyROweSd9Wvo_6gFNtI2N8GS35QeWqo5MhFvkLhGdAr9bWUBgsg6EAA; __Secure-3PSIDTS=sidts-CjEB7F1E_KwE2LrChyROweSd9Wvo_6gFNtI2N8GS35QeWqo5MhFvkLhGdAr9bWUBgsg6EAA; _ga_VWZPXDNJJB=GS1.1.1711364172.2.1.1711366407.0.0.0; _ga=GA1.3.266499014.1711329929; _gid=GA1.3.2049783146.1711329935; S=billing-ui-v3=dEKp_gZojR01F2gmg5YhKLRgMW4LEkqo:billing-ui-v3-efe=dEKp_gZojR01F2gmg5YhKLRgMW4LEkqo",
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