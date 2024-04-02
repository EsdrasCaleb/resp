from resp.apis.ieee_api import IEEE
import time
from db_paper import db_paper
from os import walk,rename
import csv

mounths = {
    "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12,
    "January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6, "July": 7, "August": 8,
    "September": 9, "October": 10, "November": 11, "December": 12
}
initialyear = 2011
def get_mouth(string):
    array_ob = string.split(" ")
    if len(array_ob) ==3:
        return mounths[array_ob[1].strip()]
    else:
        print(string)
        return 0
def cache_pile(pile, ieee, db):
    csvstring = None
    while not csvstring:
        try:
            csvstring = ieee.download_csv(pile)
        except Exception as e:
            time.sleep(5)
    f = open("ieeecsv/"+str(initialyear)+".csv", "w")
    f.write(csvstring)
    print("writtern")
    f.close()
    try:
        with open("ieeecsv/"+str(initialyear)+".csv", newline='') as csvfile:
            print("enter")
            reader = csv.DictReader(csvfile)
            for row in reader:
                if not "DOI" in row.keys() :
                        print(row)
                        continue
                paper_ob = db.get_paper(row["DOI"].strip())
                citations = 0
                if row["Article Citation Count"]:
                    citations += int(row["Article Citation Count"].strip())
                if row["Patent Citation Count"]:
                    citations += int(row["Patent Citation Count"].strip())
                if not paper_ob:
                    print("new paprer"+ row["Document Title"] )
                    if (not row["Reference Count"]):
                        row["Reference Count"] = '0'
                    paper = {"title": row["Document Title"].strip(), "origin": row["Publication Title"],
                             "year": row["Publication Year"].strip(), "mounth": get_mouth(row["Date Added To Xplore"].strip()),
                             "doi": row["DOI"].strip(), "references": row["Reference Count"].strip(),
                             "total_citations": citations
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
                    if (not row["IEEE Terms"] and not row["Author Keywords"] and row["Mesh_Terms"]):
                        for term in row["Mesh_Terms"].split(";"):
                            term_ob = db.insert_keyword(term.strip())
                            db.insert_keyword_paper(term_ob["id"], paper_ob["id"])
                else:
                    if paper_ob["total_citations"] != citations:
                        paper_ob["total_citations"] = citations
                        db.update_paper(paper_ob)
                    print("already imported " + str(paper_ob["id"]))
    except Exception as e:
        filenames = next(walk("ieeecsv/downloaded"), (None, None, []))[2]  # [] if no file
        rename("ieeecsv/"+str(initialyear)+".csv", "ieeecsv/downloaded/error" + str(len(filenames))+".csv")
    return []

db = db_paper(host="db", user="root", password="example", db="papersplease")
pile = []

db.connect()
ieee = IEEE()
source = ["ContentType:Conferences", "ContentType:Journals", "ContentType:Magazines"]
short = ["", "newest", "oldest","paper-citations","patent-citations","most-popular","pub-title-asc","pub-title-desc"]
for ano in range(initialyear, 2021):
    print("Ano "+str(ano) )
    for cont in source:
        print("Importing "+cont)
        for searc in short:
            print("Order " + cont)
            response = None
            for page in range(1, 101):
                while not response:
                    try:
                        response = ieee.serach_articles(page=page, year=ano, content=[cont],order=searc)
                    except Exception as e:
                        time.sleep(5)
                        response = None
                if (page > response["totalPages"]):
                    break
                print("Page " + str(page))
                for paperob in response["records"]:
                    if "doi" in paperob.keys() :
                        paper = db.get_paper(paperob["doi"].strip())
                        if not paper:
                            pile.append(paperob["articleNumber"])
                            print("Paper Add " + str(paperob["articleNumber"]+" doi "+paperob["doi"]))
                        else:
                            citations = 0
                            if paperob["citationCount"]:
                                citations += paperob["citationCount"]
                            if paperob["patentCitationCount"]:
                                citations += paperob["patentCitationCount"]
                            if paper["total_citations"] != citations:
                                print("Atualizando citacoes " + paperob["doi"])
                                paper["total_citations"] = citations
                                db.update_paper(paper)
                if len(pile) >= 2000:
                    pile = cache_pile(pile, ieee, db)
                response = None

db.close()
