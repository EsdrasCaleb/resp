from resp.apis.ieee_api import IEEE


def cache_pile(pile,ieee,index):
    csv = ieee.download_csv(pile)
    f = open("ieeecsv/downloaded/file"+str(index)+".csv", "w")
    f.write(csv)
    f.close()
    print("file"+str(index)+".csv")
index = 219
path = "ieeecsv/downloaded"
pile = []
ieee = IEEE()
source =["ContentType:Conferences","ContentType:Journals","ContentType:Magazines"]
for ano in range(2008,2022): #talvez tenham algumas faltando em 2007
    print("Ano "+str(ano))
    for cont in source:
        print(cont)
        response = ieee.serach_articles(page=1, year=ano,content=[cont])
        for page in range(2,response["totalPages"]+2):
            print("Page "+str(page))
            for paperob in response["records"]:
                pile.append(paperob["articleNumber"])
            reponse = []
            if len(pile)>=2000:
                cache_pile(pile,ieee,index)
                pile = []
                index += 1
            if page<=response["totalPages"]:
                response = ieee.serach_articles(page=page, year=ano, content=[cont])
