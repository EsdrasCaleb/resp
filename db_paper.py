import mysql.connector





def update_citations(paper_ob,sc,db):
    db.connect()
    final_year = str(int(paper_ob["paper_year"]) + 2)
    citations_ob = db.get_citations(paper_ob["id"], final_year)
    if not citations_ob or not citations_ob["citations"]:
        result = sc.paper_citations(paper_ob["name"], paper_ob["paper_year"])
        print(result)
        if not citations_ob or citations_ob["citations"] != result:
            citations_ob = {"paper_id": paper_ob["id"], "citations": result, "final_year": final_year}
            citations_ob = db.insert_citations(citations_ob)
    db.close()
    return citations_ob
class db_paper(object):
    def __init__(self,host,db,password,user):
        self.config = {"host":host,"user":user,"password":password,"database":db}

    def get_qualis(self,qualisname):
        if (not self.ctx.is_connected()):
            self.connect()
        cursor = self.ctx.cursor()
        query = "SELECT * from qualis where label = %s"
        querydata = [qualisname]
        cursor.execute(query, querydata)
        result = cursor.fetchall()
        if (len(result) == 0):
            return None
        else:
            return dict(zip(cursor.column_names, result[0]))

    def update_source_qualis(self,source_string,qualis,force=False):
        if (not self.ctx.is_connected()):
            self.connect()
        cursor = self.ctx.cursor()
        update_trend = ("UPDATE source SET qualis_id = %(qualisid)s  "
                        "WHERE name like %(sourcestring)s "
                        "and  %(qualisvalue)s> (SELECT q2.value from qualis q2 where q2.id= source.qualis_id)")
        if(force):
            update_trend = ("UPDATE source SET qualis_id = %(qualisid)s  "
                            "WHERE name like %(sourcestring)s ")
        querydata = {"qualisid":qualis["id"],"qualisvalue":qualis["value"], "sourcestring":source_string}

        cursor.execute(update_trend, querydata)

        self.ctx.commit()
        cursor.close()
    def connect(self):
        self.ctx = mysql.connector.connect(**self.config)

    def insert_update_trends(self,keyword_id, year, mounth, value, onlyinsert = False):
        if (not self.ctx.is_connected()):
            self.connect()
        cursor = self.ctx.cursor()
        atual_trend = self.get_trend(keyword_id, year, mounth)
        if(atual_trend):
            if not onlyinsert:
                update_trend = "UPDATE keyword_trend SET value = %s  WHERE id = %s"
                querydata = (value,atual_trend["id"])

                cursor.execute(update_trend, querydata)
                self.ctx.commit()
                cursor.close()
        else:
            add_paper = ("INSERT INTO keyword_trend "
                         "(keyword_id, trend_year, trend_mounth, value) "
                         "VALUES (%s, %s, %s, %s)")
            querydata = (keyword_id, year, mounth,
                         value)
            cursor.execute(add_paper, querydata)
            self.ctx.commit()
            atual_trend = {"id":cursor.lastrowid, "trend_year":year, "trend_mounth":mounth, "value":value}
            cursor.close()
        return atual_trend

    def get_trend(self,keyword_id, year, mounth):
        if (not self.ctx.is_connected()):
            self.connect()
        cursor = self.ctx.cursor()
        query = ("SELECT * FROM keyword_trend "
                 "WHERE keyword_id = %s and trend_year = %s and trend_mounth =%s")

        cursor.execute(query, (keyword_id, year, mounth))
        data = cursor.fetchall()
        cursor.close()
        if (len(data) == 0):
            return None
        else:
            return dict(zip(cursor.column_names, data[0]))
    def get_paper(self,paper_doi):
        if (not self.ctx.is_connected()):
            self.connect()
        cursor = self.ctx.cursor()
        query = ("SELECT * FROM paper "
                 "WHERE doi = %s")

        cursor.execute(query, (paper_doi,))
        data = cursor.fetchall()
        cursor.close()
        if(len(data) == 0):
            return None
        else:
            return dict(zip(cursor.column_names, data[0]))
    def insert_paper(self,paper_data):
        if(not self.ctx.is_connected()):
            self.connect()
        cursor = self.ctx.cursor()
        paper_ob = self.get_paper(paper_data['doi'])
        if(paper_ob):
            return paper_ob
        else:
            add_paper = ("INSERT INTO paper "
                            "(name, paper_year, mounth, source_id, doi,paper_references,total_citations) "
                            "VALUES (%s, %s, %s, %s, %s, %s,%s)")
            querydata = (paper_data["title"],paper_data["year"],paper_data["mounth"],
                                       paper_data["source_id"],paper_data["doi"],paper_data["references"],
                                        paper_data["total_citations"])
            cursor.execute(add_paper, querydata)
            self.ctx.commit()
            paper_data["id"] = cursor.lastrowid
            paper_data["paper_year"] = paper_data["year"]
            paper_data["name"] = paper_data["title"]
            cursor.close()
            return paper_data
    def update_paper(self, paper_data):
        if(not self.ctx.is_connected()):
            self.connect()
        cursor = self.ctx.cursor()
        paper_ob = self.get_paper(paper_data['doi'])
        if(paper_ob):
            update_paper = "UPDATE paper SET paper_references = %s , total_citations = %s WHERE id = %s"
            querydata = (paper_data["paper_references"],paper_data["total_citations"],paper_data["id"])

            cursor.execute(update_paper, querydata)
            self.ctx.commit()
            cursor.close()
    def get_source(self,name):
        if (not self.ctx.is_connected()):
            self.connect()
        cursor = self.ctx.cursor()
        query = ("SELECT * FROM source "
                 "WHERE name = %s")

        cursor.execute(query, (name,))
        data = cursor.fetchall()
        cursor.close()
        if (len(data) == 0):
            return None
        else:
            return dict(zip(cursor.column_names, data[0]))

    def insert_source(self,source_name):
        if (not self.ctx.is_connected()):
            self.connect()
        cursor = self.ctx.cursor()
        source_ob = self.get_source(source_name)
        if (source_ob):
            return source_ob
        else:
            add_paper = ("INSERT INTO source "
                         "(name, qualis_id) "
                         "VALUES (%s, 1)")
            cursor.execute(add_paper, (source_name,))
            source_data = {"name":source_name, "qualis_id":1}
            self.ctx.commit()
            source_data["id"] = cursor.lastrowid
            cursor.close()
            return source_data

    def get_citations(self,paper_id,year):
        if (not self.ctx.is_connected()):
            self.connect()
        cursor = self.ctx.cursor()
        query = ("SELECT * FROM citations "
                 "WHERE paper_id = %s and final_year = %s")

        cursor.execute(query, (paper_id,year))
        data = cursor.fetchall()
        cursor.close()
        if (len(data) == 0):
            return None
        else:
            return dict(zip(cursor.column_names, data[0]))
    def insert_citations(self,citations_ob):
        if (not self.ctx.is_connected()):
            self.connect()
        cursor = self.ctx.cursor()
        cit_ob = self.get_citations(paper_id=citations_ob["paper_id"],year=citations_ob["final_year"])
        if(not cit_ob):
            add_citations = ("INSERT INTO citations "
                         "(paper_id, final_year, citations) "
                         "VALUES (%s, %s, %s)")

            cursor.execute(add_citations, (citations_ob["paper_id"],citations_ob["final_year"],
                                           citations_ob["citations"]))
            self.ctx.commit()
            citations_ob["id"] = cursor.lastrowid

        elif(cit_ob["citations"] != citations_ob["citations"]):
            add_citations = ("UPDATE citations SET citations =%s where id=%s")
            cursor.execute(add_citations, (citations_ob["citations"],cit_ob["id"]))
            citations_ob["id"] = cit_ob["id"]
            self.ctx.commit()
        cursor.close()
        return citations_ob

    def get_keyword(self,keyname):
        if (not self.ctx.is_connected()):
            self.connect()
        cursor = self.ctx.cursor()
        query = ("SELECT * FROM keyword "
                 "WHERE UPPER(name) = %s ")

        cursor.execute(query, (keyname.upper(),))
        data = cursor.fetchall()
        cursor.close()
        if (len(data) == 0):
            return None
        else:
            return dict(zip(cursor.column_names, data[0]))
    def insert_keyword(self,keyname):
        if (not self.ctx.is_connected()):
            self.connect()
        cursor = self.ctx.cursor()
        key_ob = self.get_keyword(keyname=keyname)
        if(not key_ob):
            key_ob = {"name":keyname}
            add_key = ("INSERT INTO keyword "
                         "(name) "
                         "VALUES (%s)")
            cursor.execute(add_key, (keyname,))
            self.ctx.commit()
            key_ob["id"] = cursor.lastrowid
            cursor.close()

        return key_ob

    def get_keyword_paper(self, key_id,paper_id):
        if (not self.ctx.is_connected()):
            self.connect()
        cursor = self.ctx.cursor()
        query = ("SELECT * FROM keyword_paper "
                 "WHERE paper_id = %s and keyword_id = %s")

        cursor.execute(query, (paper_id,key_id))
        data = cursor.fetchall()
        cursor.close()
        if (len(data) == 0):
            return None
        else:
            return dict(zip(cursor.column_names, data[0]))

    def insert_keyword_paper(self, key_id,paper_id):
        if (not self.ctx.is_connected()):
            self.connect()
        cursor = self.ctx.cursor()
        ob = self.get_keyword_paper(key_id=key_id,paper_id=paper_id)
        if (not ob):
            ob = {"paper_id":paper_id,"keyword_id":key_id}
            add_key = ("INSERT INTO keyword_paper "
                       "(paper_id,keyword_id) "
                       "VALUES (%s,%s)")
            cursor.execute(add_key, (paper_id,key_id))
            self.ctx.commit()
            ob["id"] = cursor.lastrowid
            cursor.close()

        return ob

    def close(self):
        if(self.ctx):
            self.ctx.close()