from resp.apis.scholar_api import Scholar
import csv
from os import walk
from db_paper import db_paper,update_citations


filenames = next(walk("ieeecsv"), (None, None, []))[2]  # [] if no file

def get_mouth(string):
    array_ob = string.split(" ")
    mounths = {
        "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12,
        "January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6, "July": 7, "August": 8,
        "September": 9, "October": 10, "November": 11, "December": 12
    }
    return mounths[array_ob[1]]


if len(filenames) > 0:
    db = db_paper(host="db", user="root", password="example", db="papersplease")
    db.connect()
    sc = Scholar()
    for file in filenames:
        print(file)
        i = 0
        with open("ieeecsv/"+file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                print("importing "+row["Document Title"]+" n"+str(i))
                paper_ob = db.get_paper(row["DOI"].strip())
                if not paper_ob:
                    paper = {"title" : row["Document Title"].strip(),"origin" : row["Publication Title"],
                             "year" : row["Publication Year"].strip(),"mounth":get_mouth(row["Date Added To Xplore"].strip()),
                             "doi":row["DOI"].strip(),"references":row["Reference Count"].strip()
                             }
                    source_data = db.insert_source(paper["origin"].strip())
                    paper["source_id"] = source_data["id"]
                    paper_ob = db.insert_paper(paper)
                    for term in row["IEEE Terms"].split(";"):
                        term_ob = db.insert_keyword(term.strip())
                        db.insert_keyword_paper(term_ob["id"], paper_ob["id"])
                    for term in row["Author Keywords"].split(";"):
                        term_ob = db.insert_keyword(term.strip())
                        db.insert_keyword_paper(term_ob["id"], paper_ob["id"])
                update_citations(paper_ob,sc,db)
                i+=1
    db.close()
