import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score, KFold
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB

from db_paper import db_paper
import csv
import os.path
import time


def remove_outliers(df, column, threshold=3):
    # Calculate z-scores
    z_scores = (df[column] - df[column].mean()) / df[column].std()

    # Identify outliers
    outlier_indices = z_scores.abs() > threshold

    # Remove outliers
    df_cleaned = df[~outlier_indices]

    return df_cleaned

def test_naive(attributes,classes):
    nb_classifier = GaussianNB()
    kf = KFold(n_splits=10, shuffle=True, random_state=int(time.time() % 100))
    scores = cross_val_score(nb_classifier, attributes, classes, cv=kf)
    print("Mean Accuracy:", scores.mean())

def splited_naive(atributes,classes,split):
    X_train, X_test, y_train, y_test = train_test_split(atributes, classes, test_size=split,
                                                        random_state=int(time.time() % 100))
    nb_classifier = GaussianNB()
    nb_classifier.fit(X_train, y_train)
    y_pred = nb_classifier.predict(X_test)

    # Evaluate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print("Split " + str(split * 100) + "% Accuracy:", accuracy)

def test_tree(atributes,classes):
    dt_classifier = DecisionTreeClassifier(random_state=int(time.time() % 100))

    # Define 10-fold cross-validation
    kf = KFold(n_splits=10, shuffle=True, random_state=int(time.time() % 100))

    # Perform 10-fold cross-validation
    scores = cross_val_score(dt_classifier, atributes, classes, cv=kf)

    # Print accuracy scores for each fold
    #for i, score in enumerate(scores, 1):
    #    print(f"Fold {i}: {score}")

    # Calculate and print mean accuracy
    print("Mean Accuracy:", scores.mean())

def splited_tree(atributes,classes,split):
    X_train, X_test, y_train, y_test = train_test_split(atributes, classes, test_size=split,
                                                        random_state=int(time.time() % 100))

    # Create KNN classifier with k=5
    dt_classifier = DecisionTreeClassifier(random_state=int(time.time() % 100))

    # Train the classifier
    dt_classifier.fit(X_train, y_train)

    # Make predictions on the testing set
    y_pred = dt_classifier.predict(X_test)

    # Evaluate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print("Split " + str(split * 100) + "% Accuracy:", accuracy)

def test_knm(atributes,classes):
    knn = KNeighborsClassifier()
    knn.fit(atributes, classes)
    kf = KFold(n_splits=10, shuffle=True, random_state=int(time.time()%100))
    scores = cross_val_score(knn, atributes, classes, cv=kf)
    #for i, score in enumerate(scores, 1):
        #print(f"Fold {i}: {score}")

    # Calculate and print mean accuracy
    print("10 Fold Accuracy:", scores.mean())

def splitedt_knm(atributes,classes,porcent):
    X_train, X_test, y_train, y_test = train_test_split(atributes, classes, test_size=porcent,
                                                        random_state=int(time.time()%100))

    # Create KNN classifier with k=5
    knn = KNeighborsClassifier(n_neighbors=5)

    # Train the classifier
    knn.fit(X_train, y_train)

    # Make predictions on the testing set
    y_pred = knn.predict(X_test)

    # Evaluate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print("Split "+str(porcent*100)+"% Accuracy:", accuracy)

if(not os.path.isfile("checkpoint/data.csv")):
    query = ("SELECT paper_references,"
                "count(distinct kp.keyword_id) as keywords,"
                "coalesce(max(dt.delta),0) as max_delta,"
                "coalesce(sum(dt.delta)/count(distinct kp.keyword_id),0) avg_delta,"
                "coalesce(min(dt.delta),0) as min_delta,"
                "coalesce(sum(kt.value)/count(distinct kp.keyword_id),0) avg_trend,"
                "coalesce(max(kt.value),0) as max_trend,"
                "coalesce(min(kt.value),0) as min_trend,"
                "max(q.value) as peso_fonte, "
                "Case "
                "when c.citations <2  then "
                    "'irrelevant' "
                "else "
                    "'relevant' "
                "END "
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
    db.connect()
    data = db.query(query)
    header = data[0].keys()
    with open("checkpoint/data.csv", 'w', newline='') as csvfile:
        # Create a CSV writer object
        writer = csv.DictWriter(csvfile, fieldnames=header)

        # Write header
        writer.writeheader()

        # Write each dictionary as a row
        for row in data:
            writer.writerow(row)
print("Checkpoint 2")
df = pd.read_csv('checkpoint/data.csv')
print("Testando dados")
test_knm(df.iloc[:, :-1],df.iloc[:, -1] )
print("Removendo da base outliners usando treshhold 3 e o pandas")

df_cleaned = df
for colum in df.columns:
    if(colum != "class"):
        df_cleaned = remove_outliers(df_cleaned, colum)
df_cleaned.to_csv('checkpoint/redusida1.csv', index=False)
print("Testando dados")
test_knm(df_cleaned.iloc[:, :-1],df_cleaned.iloc[:, -1])

print("Removendo os artibutos delta trends")
columns_to_remove = ['max_delta', 'avg_delta',"min_delta"]
df_reduced = df.drop(columns=columns_to_remove)
df_reduced.to_csv('checkpoint/redusida2.csv', index=False)
print("Testando dados")
test_knm(df_reduced.iloc[:, :-1],df_reduced.iloc[:, -1])

print("Checkpoint 3")
print("Testando dados completos")
splitedt_knm(df.iloc[:, :-1],df.iloc[:, -1],0.1)
splitedt_knm(df.iloc[:, :-1],df.iloc[:, -1],0.2)
splitedt_knm(df.iloc[:, :-1],df.iloc[:, -1],0.3)
print("Testando dados reduzido 1")
splitedt_knm(df_cleaned.iloc[:, :-1],df_cleaned.iloc[:, -1],0.1)
splitedt_knm(df_cleaned.iloc[:, :-1],df_cleaned.iloc[:, -1],0.2)
splitedt_knm(df_cleaned.iloc[:, :-1],df_cleaned.iloc[:, -1],0.3)
print("Testando dados reduzido 2")
splitedt_knm(df_reduced.iloc[:, :-1],df_reduced.iloc[:, -1],0.1)
splitedt_knm(df_reduced.iloc[:, :-1],df_reduced.iloc[:, -1],0.2)
splitedt_knm(df_reduced.iloc[:, :-1],df_reduced.iloc[:, -1],0.3)
#fig, ax = plt.subplots()
#boxplot = df.boxplot(ax=ax,column=['peso_fonte'])
#plt.show()
