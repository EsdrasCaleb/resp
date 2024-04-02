from resp.apis.acm_api import ACM
from resp.apis.scholar_api import Scholar
from db_paper import db_paper,update_citations



db = db_paper(host="db",user="root",password="example",db="papersplease")
db.connect()
acm = ACM()
#sc = Scholar()
order = ["EpubDate_asc","EpubDate_desc","batch1","cited","relevancy"]
for ano in range(2004,2022): #alguns faltando em 2004 e 2007
    for mes in range(1,13):
        for i in order:
            if(ano==2004 and mes<11):
                continue
            papers = acm.all_paper(start_page=0, max_pages=10, pagesize=200,min_year=ano,max_year=ano,
                                   min_mouth=mes,max_mouth=mes,order=i) #max 1000
            print("Ano "+str(ano)+" mes "+str(mes)+ " order "+i)
            for paper_url in papers:
                paper_ob =db.get_paper("/".join(paper_url["url"].split("/")[2:]))
                if not paper_ob:
                    print("novo paper "+paper_url["url"])
                    paper = acm.get_paperdata(paper_url["url"])
                    if(paper):
                        paper["total_citations"] = paper_url['citation']
                        print(paper)
                        source_data = db.insert_source(paper["origin"].strip())
                        paper["source_id"] = source_data["id"]
                        paper_ob = db.insert_paper(paper)
                        for term in paper["terms"]:
                            term_ob = db.insert_keyword(term.strip())
                            db.insert_keyword_paper(term_ob["id"], paper_ob["id"])
                    else:
                        print(paper_url)
                        if paper_ob["total_citations"] != paper_url['citation']:
                            paper_ob["total_citations"] = paper_url['citation']
                            db.update_paper(paper_ob)
                            print("update citations "+paper_url['citation']+" in paper "+paper_url["url"])
                        continue
                #update_citations(paper_ob,sc,db)

db.close()