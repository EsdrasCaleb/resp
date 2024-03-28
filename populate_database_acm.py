from resp.apis.acm_api import ACM
from resp.apis.scholar_api import Scholar
from db_paper import db_paper,update_citations



db = db_paper(host="db",user="root",password="example",db="papersplease")
db.connect()
acm = ACM()
sc = Scholar()
order = ["EpubDate_asc","EpubDate_desc","downloaded","cited","relevancy"]
for ano in range(2007,2022):
    for mes in range(1,13):
        for i in order:
            papers = acm.all_paper(start_page=0, max_pages=10, pagesize=200,min_year=ano,max_year=ano,
                                   min_mouth=mes,max_mouth=mes,order=i) #max 1000
            print("Ano "+str(ano)+" mes "+str(mes)+ " order "+i)
            for paper_url in papers:
                paper_ob =db.get_paper("/".join(paper_url.split("/")[2:]))
                if not paper_ob:
                    paper = acm.get_paperdata(paper_url)
                    if(paper):
                        source_data = db.insert_source(paper["origin"].strip())
                        paper["source_id"] = source_data["id"]
                        paper_ob = db.insert_paper(paper)
                        for term in paper["terms"]:
                            term_ob = db.insert_keyword(term.strip())
                            db.insert_keyword_paper(term_ob["id"], paper_ob["id"])
                    else:
                        continue
                update_citations(paper_ob,sc,db)

db.close()