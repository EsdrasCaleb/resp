import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn import datasets
from sklearn import svm


query = ("SELECT paper_references,"
            "count(distinct kp.keyword_id) as keywords,"
            "coalesce(max(dt.delta),0) as max_delta,"
            "coalesce(sum(dt.delta),0)/count(distinct kp.keyword_id) avg_delta,"
            "coalesce(min(dt.delta),0) as min_delta,"
            "sum(kt.value)/count(distinct kp.keyword_id) avg_trend,"
            "coalesce(max(kt.value),0) as max_trend,"
            "coalesce(min(kt.value),0) as min_trend,"
            "max(q.value) as peso_fonte, "
            "Case "
            "when c.citations <2  then "
                "'irrelevant' "
            "else "
                "'relevant' "
            "END"
            "as class "
        "FROM paper p "
        "left JOIN keyword_paper kp on p.id = kp.paper_id "
        "LEFT JOIN keyword_trend kt on kt.keyword_id = kp.keyword_id "
        "and kt.trend_year= p.paper_year and kt.trend_mounth = p.mounth "
        "LEFT JOIN delta_trend dt on p.id = dt.paper_id and dt.keyword_id = kp.keyword_id "
        "JOIN citations c on c.paper_id = p.id  and c.final_year=(p.paper_year+2) "
        "JOIN source s on s.id = p.source_id "
        "JOIN qualis q on q.id = s.qualis_id "
        "GROUP BY p.id,paper_references,c.citations "
)
db = db_paper(host="db", user="root", password="example", db="papersplease")
fig, ax = plt.subplots()
boxplot = df.boxplot(ax=ax,column=['peso_fonte'])  
plt.show()
