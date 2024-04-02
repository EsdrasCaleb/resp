from resp.apis.ieee_api import IEEE
import time

def cache_pile(pile,ieee,index):
    csv = ieee.download_csv(pile)
    f = open("ieeecsv/downloaded/file"+str(index)+".csv", "w")
    f.write(csv)
    f.close()
    print("file"+str(index)+".csv")
    return []
index = 0
path = "ieeecsv/downloaded"
pile = []
ieee = IEEE()
lastpile = []
source =["ContentType:Conferences","ContentType:Journals","ContentType:Magazines"]
for ano in range(2012,2022): #talvez tenham algumas faltando em 2007 (tudo) e em 2009 (conferencias) e parece faltar 2004 tb
    print("Ano "+str(ano))
    for cont in source:
        print(cont)
        if(ano==2012):
            if cont == "ContentType:Conferences":
                continue
        for page in range(1,101):
            print("Page "+str(page))
            response = ieee.serach_articles(page=page, year=ano, content=[cont])
            for paperob in response["records"]:
                if not paperob["articleNumber"] in lastpile:
                    pile.append(paperob["articleNumber"])
            reponse = []
            if len(pile)>=2000:
                lastpile = pile
                pile = cache_pile(pile,ieee,index)
                index += 1


