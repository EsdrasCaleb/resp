from resp.apis.acm_api import ACM
from resp.apis.scholar_api import Scholar
from resp.apis.trends_api import Trends


headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0",
                            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                            "Accept-Language": "pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3",
                            "Accept-Encoding": "gzip, deflate, br",
                            "Connection": "keep-alive",
                            "Cookie": "__utma=10102256.266499014.1711329929.1711329935.1711329935.1; __utmb=10102256.2.10.1711329935; __utmc=10102256; __utmz=10102256.1711329935.1.1.utmcsr=trends.google.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmt=1; NID=512=SoHqkgDlcerKHS_czYHFoQSeheOk3y_HlKFxbwiw3Hq2TJXUJwVyJue1hCcwmG3bjlTe-AmucWdLC_T9sBbyKsmvHxVuUg0CYa85KiV_EJvd2NpiCg975h-gFh64SnvZb_egdsI33zmr_Ys_kXXpiQXhpuXjIO8AX7OUYXFN9pOJui-euZMqtG0ZXhE0-G2QQkWAUafJDiBCVFx0POzzlYYleR7f5TOep9rCoso-AZhrcy_qi8p4dQUmC3DzrUfR-H9jOhyr6UnwkmUVtwC4xBUHsK0-8taZn_lkkn8Q7DDI2iu_1oIYc7I0on-D4dOrDVtBwEvXeBXwGoNRtZ6Q_s8hxdfQp62Ru6-IRyCDzNRANlqVusGOSYJeGY5KMgEEfUyFbC-EeygbMLnrpvWvYSxKD8LNihuGuktnar4fSwalIqqK0fFaoQdAVEZueIuSTQy4V6s0C5p6X6O_4NkAO0yZoSimDjfDtzTdkVYRF6kIoBotlruaFErDM6ZaKM9Kern5e8jAqfzKucJdxg9BHqeiKs1a3YF8LR1jMa9-jK9JOjhKrY53ev62OBVLk_SFHr-yL-xSdZVmtpWxX-oq5XuTjXGkcSTJV5Qm8feTzIOmUV1QpReCLci50MQMlToo67YgLD-WQTRTfp5cHURxsNGbG6lIQXzrXNnO9mjRUoDIcbkawaYd7FqfRUaLNIQFS_Kn2M841Wz2vC9SvvC7u97m2Fii5qfb6C_vJLly38g1QSUyz-2Uf-Gws8L8sRXwTb9iKXuhy4a2ofDP9A3-AP6pePPMDpKkVGRNTY7i6Dln0-VvJvy2yaiLl-Tm-sROYF442Bn9urOsaQA4YsRPD9_zqvClhD4szW8bbJAfXp8UhKcyCuWXdNp4iG0mAuxxgVKkGMiCMNfmJRnUL4oY1PZtwkyXwrTRyKn6qytsX0PEbDZkKjkDKCA2nRNIibpdvSzgNXbpeid5b6HbEHfJR_M3nEWxtpLKwNwtZ2ewb6LAS_G_pzXUogbr9mrISpklWmfqIiSBpIPG9QGa6CF1AaYPygIX_JqpJ_E5uN_d47JiEGklLTfjPBPj8uujNZB2EjP6QS1lZGkT6d9oxyuHnXkMiYTaCqyoFvTyd5QGYvd9ASoU46amEMuU8o-JhN3toR8tw3YGX3xMz2BZ-0BCmCH9RHpgLzE; 1P_JAR=2024-03-25-01; SEARCH_SAMESITE=CgQI3ZoB; ANID=AHWqTUnMWdRx55Av9ABLl2GWIrI2RiR9RuoZKFufPgj97zX_cV5y63jVHDjwhQmy; AEC=Ae3NU9MPT8gahF1kgOwRZPQa1LkxMgOf_Hd4IX8JzSHj6b0MvQnlqPnn6g; SID=g.a000hwiw8mWaWz-JJQ7EkAAt3BqQ6_JarxYOiKw0HwYHVRnMbAze2ZhGJSsw3u96egHS8l_DnwACgYKARYSAQASFQHGX2MixOcpeIUvLCWscMbZ4BB3nRoVAUF8yKo4HBlWqp5Zqmsw1hwAzPpl0076; __Secure-1PSID=g.a000hwiw8mWaWz-JJQ7EkAAt3BqQ6_JarxYOiKw0HwYHVRnMbAzeycmqFnv3r3LaZHWgBr6H0AACgYKAZQSAQASFQHGX2MiMl4q32hh4G7BGfW00OhDkxoVAUF8yKr0vBT4pRACqqQusxGNwE2A0076; __Secure-3PSID=g.a000hwiw8mWaWz-JJQ7EkAAt3BqQ6_JarxYOiKw0HwYHVRnMbAzemSe-szt5jAMlFkrwBrPpHQACgYKAfkSAQASFQHGX2MiCAL6gHshElWP185oEkMZShoVAUF8yKrLdpM7PWxmEiN8EQRqFjbT0076; HSID=AvQssgkv8bTi_MJN7; SSID=A_PRG9X6FhoPiRmLL; APISID=1FQQAOetMu2Z_nqC/AB7a9Qt-I2eJzvrcu; SAPISID=OtI8AuS7T1j8PckO/AlrnvEvuaWMfkDjk4; __Secure-1PAPISID=OtI8AuS7T1j8PckO/AlrnvEvuaWMfkDjk4; __Secure-3PAPISID=OtI8AuS7T1j8PckO/AlrnvEvuaWMfkDjk4; SIDCC=AKEyXzXrpcY5-LuLCtB463NsQ-gsvwRRu7wlwvamtaPA5szTZ5I8RKSX4D1zJ-L8fQab-H-l4t4; __Secure-1PSIDCC=AKEyXzUZU-PcUwJSnPCZTNABV5ftpTMQi6cwVfYPLpnmEJl1KO8_P0hSa0NZxAekvV-nGO45sHI; __Secure-3PSIDCC=AKEyXzUuYcEk_OI4hLeekEkY7Kyogh1dDmQBn7Ila3Q5oPtLQ3nS0a-UvD21wKCl2ZjxZaN2cVY; __Secure-1PSIDTS=sidts-CjEB7F1E_G-dtTKmZM5TIuOwIESfN7dbELcpl3L-FUvqy3J-nmhIZ_FIecUhyiswk1miEAA; __Secure-3PSIDTS=sidts-CjEB7F1E_G-dtTKmZM5TIuOwIESfN7dbELcpl3L-FUvqy3J-nmhIZ_FIecUhyiswk1miEAA; S=billing-ui-v3=dEKp_gZojR01F2gmg5YhKLRgMW4LEkqo:billing-ui-v3-efe=dEKp_gZojR01F2gmg5YhKLRgMW4LEkqo; _ga_VWZPXDNJJB=GS1.1.1711329929.1.1.1711329942.0.0.0; _ga=GA1.3.266499014.1711329929; _gid=GA1.3.2049783146.1711329935; _gat_gtag_UA_4401283=1",
                            "Upgrade-Insecure-Requests": "1",
                            "Sec-Fetch-Dest": "document",
                            "Sec-Fetch-Mode": "navigate",
                            "Sec-Fetch-Site": "none",
                            "Sec-Fetch-User": "?1"
                            }

acm = ACM()
sc = Scholar()
td = Trends(3,headers)
papers = acm.all_paper(0,1,1)
print(papers)
for paper_url in papers:
    paper = acm.get_paperdata(paper_url)
    result = sc.paper_citations(paper["title"],paper["year"])
    paper["f_citations"] =result
    for term in paper["terms"]:
        #check database is term exists id don't populate
        result = td.query(term)
        dic = result.to_dict()
        for rr in dic[term]:
            print(rr.year, rr.month) #mes e ano
            print(dic[term][rr]) #valor
    break
