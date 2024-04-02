from resp.apis.scholar_api import Scholar
from db_paper import db_paper,update_citations
from db_paper import db_paper,update_citations

lastid = "1889"
sc = Scholar()
db = db_paper(host="db", user="root", password="example", db="papersplease")
db.connect()
cursor = db.ctx.cursor()
query = ("SELECT * FROM paper "
         "WHERE paper_references>0 and id not in (SELECT paper_id FROM citations where citations<>0)"
         "ORDER BY id DESC")
          #"and id >"+lastid)

cursor.execute(query)
data = cursor.fetchall()
colums = cursor.column_names
cursor.close()
for paper in data:
    sc.renew_proxy()
    paper_ob = dict(zip(colums, paper))
    print(paper_ob)
    print(update_citations(paper_ob, sc, db))
db.close()