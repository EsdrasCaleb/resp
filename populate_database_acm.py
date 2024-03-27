from resp.apis.acm_api import ACM
from resp.apis.scholar_api import Scholar
import db_paper



db = db_paper(host="db",user="root",password="example",database="papersplease")
db.conect()
acm = ACM()
sc = Scholar()

for i in range(1): #757
    papers = acm.all_paper(0, 1, 1) #max 1000
    print(papers)
    for paper_url in papers:
        paper = acm.get_paperdata(paper_url)
        source_data = db.insert_source(paper["origin"].strip())
        paper["origin_id"] = source_data["id"]
        paper_ob = db.insert_paper(paper)
        result = sc.paper_citations(paper["title"],paper["year"])
        final_year = paper["year"]+2
        citations_ob = {"paper_id":paper_ob["id"], "citations":result,"final_year":final_year}
        citations_ob = db.insert_citations(citations_ob)
db.close()