import mysql.connector

class db_paper(object):
    def __init__(self,host,db,password,user):
        self.config = {"host":host,"user":user,"password":password,"database":db}

    def connect(self):
        self.ctx = mysql.connector.connect(**self.config)

    def get_paper(self,paper_doi):
        if (not self.ctx.is_connected()):
            self.connect()
        cursor = self.cnx.cursor()
        query = ("SELECT * FROM paper "
                 "WHERE doi = %s")

        cursor.execute(query, (paper_doi))
        data = cursor.fetchall()
        cursor.close()
        if(len(data) == 0):
            return None
        else:
            return data[0]
    def insert_paper(self,paper_data):
        if(not self.ctx.is_connected()):
            self.connect()
        cursor = self.cnx.cursor()
        paper_ob = self.get_paper(paper_data['doi'])
        if(paper_ob):
            return paper_ob
        else:
            add_paper = ("INSERT INTO paper "
                            "(name, year, mounth, source_id, doi,references) "
                            "VALUES (%(title)s, %(year)s, %(mounth)s, %(origin_id)s, %(doi)s, %(references)s)")
            cursor.execute(add_paper, paper_data)
            paper_data["id"] = cursor.lastrowid
            cursor.close()
            return paper_data

    def get_source(self,name):
        if (not self.ctx.is_connected()):
            self.connect()
        cursor = self.cnx.cursor()
        query = ("SELECT * FROM source "
                 "WHERE name = %s")

        cursor.execute(query, (name))
        data = cursor.fetchall()
        cursor.close()
        if (len(data) == 0):
            return None
        else:
            return data[0]

    def insert_source(self,source_name):
        if (not self.ctx.is_connected()):
            self.connect()
        cursor = self.cnx.cursor()
        source_ob = self.get_source(source_name)
        if (source_ob):
            return source_ob
        else:
            add_paper = ("INSERT INTO source "
                         "(name, qualis_id) "
                         "VALUES (%s, 1)")
            cursor.execute(add_paper, (source_name))
            source_data = {"name":source_name, "qualis_id":1}
            source_data["id"] = cursor.lastrowid
            cursor.close()
            return source_data

    def get_citations(self,paper_id,year):
        if (not self.ctx.is_connected()):
            self.connect()
        cursor = self.cnx.cursor()
        query = ("SELECT * FROM citations "
                 "WHERE paper_id = %s and final_year = %s")

        cursor.execute(query, (paper_id,year))
        data = cursor.fetchall()
        cursor.close()
        if (len(data) == 0):
            return None
        else:
            return data[0]
    def insert_citations(self,citations_ob):
        if (not self.ctx.is_connected()):
            self.connect()
        cursor = self.cnx.cursor()
        cit_ob = self.get_citations(paper_id=citations_ob["paper_id"],year=citations_ob["final_year"])
        if(not cit_ob):
            add_citations = ("INSERT INTO citations "
                         "(paper_id, final_year, citations) "
                         "VALUES (%{paper_id}s, %{final_year}s, %{citations}s)")
            cursor.execute(add_citations, citations_ob)
            citations_ob["id"] = cursor.lastrowid

        elif(cit_ob["citations"] != citations_ob["citations"]):
            add_citations = ("UPDATE citations SET citations =%s where id=%s")
            cursor.execute(add_citations, (citations_ob["citations"],cit_ob["id"]))
            citations_ob["id"] = cit_ob["id"]
        cursor.close()
        return citations_ob

    def close(self):
        if(self.ctx):
            self.ctx.close()