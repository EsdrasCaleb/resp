from resp.apis.serp_api import Serp
from resp.apis.cnnp import connected_papers
from resp.apis.semantic_s import Semantic_Scholar
from resp.apis.acm_api import ACM
from resp.apis.ieee_api import IEEE
from resp.apis.scholar_api import Scholar
from resp.apis.arxiv_api import Arxiv
from resp.apis.trends_api import Trends
from resp.resp import Resp
import random

#datas de 2004 a 2023

topics = ["Computer Engineering","Machine Learning","Integer Programing","Serius Games","Tensor Flow","Artificial inteligence"]
#sc = Scholar()
#result = sc.query(topics[ random.randint(0, len(topics)-1)],1)
headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0",
                            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                            "Accept-Language": "pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3",
                            "Accept-Encoding": "gzip, deflate, br",
                            "Connection": "keep-alive",
                            "Cookie": "__utma=10102256.266499014.1711329929.1711371121.1711386579.4; __utmz=10102256.1711329935.1.1.utmcsr=trends.google.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmc=10102256; __utmb=10102256.4.10.1711386579; __utmt=1; NID=512=X04NQ6UIKdD8M17tHLr1azvTu3tR2wg0x5jZ9GiNSFgReNhcvOaSYYOv3YGdB3sTHTfEwvtuSnWZIl0s0hc36uPKTsblHNGVoZtPIE_9OPSDScietsfQUz_PzztmucbD6VLe_FX4nIIPOD9ajvY7majVWQA9HoTrGrOD8NPDQzN-Mdlsww79S9Bdu5BdBa4KEFTbnyJ6UrZtt6m6S83QZRxoUxokIIscynutQ-i7-0qsyHpnR1Jff3eNRemV4YMvhvgQFFmqm8rGIbtwHQU0oqgjBiJU9vByQyyX2QVvc_QrB5ndHWhb4jT1mDzuAC4Xh6BXRR9_hnGgWBRQ7-st5tEpJruEQK2tcI4WjQXbsznMs_vSiW5HIIP2toRnLtXceAvyePPhKuw2hd1Jqi10Z7z4Kr0xjmmEM0i-KgEFmqttZznggnvMTsJ_GB5YvlH7b-YdHMvo8V3-Aab5ey32wrce_e_Hs4MUK_aAIBJGw7lE6Y82p9hjmzLURRBz84SDvMyD_WjeSRxTBpzmIbYsH3Qw3VWCSNniyXFqCedeRYjNxeQ3eTieiDCDfuTCCcmIok3MFwWNGhFtcpTbS2ad7IInZadJ3M57ahosM2kCrykIGqIGQi4vhKHsPeHv9RSP23U_bjo8DF3qXT6wLvjI6M2Vd7CSAVvbJuH3nEVRmYlgILEM7RBgwuff3tUKviEDIhtVkWErBldR8LeXGdaeZHO_MYXon0I-5VWBKS2n2tHHr9IrEfvLgFDfEx9E0kfN6fybAMubsgMyS9sWAoEpbiMu28F5hEwdhDJUzMb0UliGDmlQHIBFQkPdQfEgdMTCgshjuFRyo8UQ6439Xv3x_dfZtQFPwowE4v8rdzbULWIQxJvmfv46rX0K3i7Pap2Z1V9k7bHbMI31IYh_ZoaWZrzjuE91hDvQuW3sZkTd5DhKHvzXi83QgXB7vXnNHT38wTJ6QTQ4qybd5l3J_-yd-cnhroXsxNb5IxInafESh_w0-jeN1hqU1lK4Rpd7vSAOA9Vpip4RY_GaXuv2-8IyS78hpKdtdIYFZ1mhhtcBG7ECskuxCb_nMBwfTFjGgVUwmmBQOql53Nt2ILBjq6XDD66xvceQlmWH0LnHCZvlg8drQl3jU0q1ZeIwGc0QhGhyktSz_sDDvR3nYk4xry4P_HKoAZYNjjw; 1P_JAR=2024-03-25-16; SEARCH_SAMESITE=CgQI3ZoB; ANID=AHWqTUnMWdRx55Av9ABLl2GWIrI2RiR9RuoZKFufPgj97zX_cV5y63jVHDjwhQmy; AEC=Ae3NU9MPT8gahF1kgOwRZPQa1LkxMgOf_Hd4IX8JzSHj6b0MvQnlqPnn6g; SID=g.a000hwiw8mWaWz-JJQ7EkAAt3BqQ6_JarxYOiKw0HwYHVRnMbAze2ZhGJSsw3u96egHS8l_DnwACgYKARYSAQASFQHGX2MixOcpeIUvLCWscMbZ4BB3nRoVAUF8yKo4HBlWqp5Zqmsw1hwAzPpl0076; __Secure-1PSID=g.a000hwiw8mWaWz-JJQ7EkAAt3BqQ6_JarxYOiKw0HwYHVRnMbAzeycmqFnv3r3LaZHWgBr6H0AACgYKAZQSAQASFQHGX2MiMl4q32hh4G7BGfW00OhDkxoVAUF8yKr0vBT4pRACqqQusxGNwE2A0076; __Secure-3PSID=g.a000hwiw8mWaWz-JJQ7EkAAt3BqQ6_JarxYOiKw0HwYHVRnMbAzemSe-szt5jAMlFkrwBrPpHQACgYKAfkSAQASFQHGX2MiCAL6gHshElWP185oEkMZShoVAUF8yKrLdpM7PWxmEiN8EQRqFjbT0076; HSID=AvQssgkv8bTi_MJN7; SSID=A_PRG9X6FhoPiRmLL; APISID=1FQQAOetMu2Z_nqC/AB7a9Qt-I2eJzvrcu; SAPISID=OtI8AuS7T1j8PckO/AlrnvEvuaWMfkDjk4; __Secure-1PAPISID=OtI8AuS7T1j8PckO/AlrnvEvuaWMfkDjk4; __Secure-3PAPISID=OtI8AuS7T1j8PckO/AlrnvEvuaWMfkDjk4; SIDCC=AKEyXzW2CoPc2iYF3Kw2MnxHaIQ-9ENTbw6-yOAxmISj9OqCa0_-zfa7ossCp4f1dQvE4GOzF9w; __Secure-1PSIDCC=AKEyXzWSPU3_Umnw7-P6uJKCW2QiGrgc010CPaStWNcGmf0Nm9UGGwLMGqgqG-zV3FuCHb3a4g0; __Secure-3PSIDCC=AKEyXzWIQdb2MHLHCPbHQ1tza7mavlGqit65BWmpm5q_cHQvO7vYxj2bCY4tg6Uy-hDVfNdLBOg; __Secure-1PSIDTS=sidts-CjEB7F1E_NV2I5LoduK4RCrPTabEOkNELxfO_KhCnxF1wEQ2AJwA49YkVpAT_8lr5beQEAA; __Secure-3PSIDTS=sidts-CjEB7F1E_NV2I5LoduK4RCrPTabEOkNELxfO_KhCnxF1wEQ2AJwA49YkVpAT_8lr5beQEAA; _ga_VWZPXDNJJB=GS1.1.1711386579.4.1.1711387548.0.0.0; _ga=GA1.3.266499014.1711329929; _gid=GA1.3.2049783146.1711329935; S=billing-ui-v3=dEKp_gZojR01F2gmg5YhKLRgMW4LEkqo:billing-ui-v3-efe=dEKp_gZojR01F2gmg5YhKLRgMW4LEkqo; _gat_gtag_UA_4401283=1",
                            "Upgrade-Insecure-Requests": "1",
                            "Sec-Fetch-Dest": "document",
                            "Sec-Fetch-Mode": "navigate",
                            "Sec-Fetch-Site": "none",
                            "Sec-Fetch-User": "?1",
                            }
query = topics[random.randint(0, len(topics)-1)]
print(query)
td = Trends(5,headers)
result = td.query(query)
dic = result.to_dict()

for rr in dic[query]:
    print(rr.year,rr.month)
    print(dic[query][rr])

#acm = ACM()
#print(acm.all_paper(0,1,10))
#acm.query(topics[ random.randint(0, len(topics)-1)],1)