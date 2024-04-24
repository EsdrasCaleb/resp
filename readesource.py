from db_paper import db_paper
import csv

file = open('qualis8.csv', 'r')

db = db_paper(host="db", user="root", password="example", db="papersplease")
spamreader = csv.reader(file)

for row in spamreader:

    test = row[1].split(" ")
    string_test = "%"
    force = False
    if(len(test) < 1):
        continue
    if len(test) == 1:
        string_test = test[0]
        force = True
    else:
        for j in test:
            string_test = string_test + j+"%"
    db.connect()
    qualis = db.get_qualis(row[2].upper())
    if(qualis):
        db.update_source_qualis(string_test,qualis,force)
    else:
        print(row)
        print("np")
    db.close()
print("end")

