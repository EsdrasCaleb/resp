from resp.apis.acm_api import ACM
from resp.apis.scholar_api import Scholar
from db_paper import db_paper,update_citations




acm = ACM()
#sc = Scholar()
order = ["EpubDate_asc","EpubDate_desc","batch1","cited","relevancy"]
for ano in range(2021,2022): #alguns faltando em 2004 e 2007
    for mes in range(1,13):
        for i in order:
            papers = acm.all_paper(start_page=0, max_pages=10, pagesize=200,min_year=ano,max_year=ano,
                                   min_mouth=mes,max_mouth=mes,order=i) #max 1000
            print("Ano "+str(ano)+" mes "+str(mes)+ " order "+i)
            for paper_url in papers:
                db = db_paper(host="db", user="root", password="example", db="papersplease")
                db.connect()
                paper_ob =db.get_paper("/".join(paper_url["url"].split("/")[2:]))
                if paper_ob and False:
                    print("novo paper "+paper_url["url"])
                    paper = acm.get_paperdata(paper_url["url"])
                    if(paper) :
                        paper["total_citations"] = paper_url['citation']
                        print(paper)
                        source_data = db.insert_source(paper["origin"].strip())
                        paper["source_id"] = source_data["id"]
                        paper_ob = db.insert_paper(paper)
                        for term in paper["terms"]:
                            term_ob = db.insert_keyword(term.strip())
                            db.insert_keyword_paper(term_ob["id"], paper_ob["id"])
                elif paper_ob:
                    print(paper_url)
                    if not paper_ob["total_citations"] or int(paper_ob["total_citations"]) <= int(paper_url['citation']):
                        paper_ob["total_citations"] = paper_url['citation']
                        db.update_paper(paper_ob)
                        print("update citations "+paper_url['citation']+" in paper "+paper_url["url"])
                    continue
                db.close()
                #update_citations(paper_ob,sc,db)

