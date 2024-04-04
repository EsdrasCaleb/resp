from resp.apis.scholar_api import Scholar
from db_paper import db_paper,update_citations
from db_paper import db_paper,update_citations

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
lastid = "1889"
sc = Scholar()
db = db_paper(host="db", user="root", password="example", db="papersplease")
db.connect()
cursor = db.ctx.cursor()
query = ("SELECT * FROM paper "
         "WHERE paper_references>0 and id not in (SELECT paper_id FROM citations where citations<>0)"
         " and id in (SELECT paper_id FROM keyword_paper where keyword_id in (SELECT keyword_id FROM keyword_trend))"
         "ORDER BY id DESC")
          #"and id >"+lastid)

cursor.execute(query)
data = cursor.fetchall()
colums = cursor.column_names
cursor.close()
for paper in data:
    sc.renew_proxy(True)
    paper_ob = dict(zip(colums, paper))
    print(paper_ob)
    print(update_citations(paper_ob, sc, db))
db.close()