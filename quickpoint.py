import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score, KFold
from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np


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


def tenfold(classifier,attributes,classe):
    kf = KFold(n_splits=10, shuffle=True, random_state=42)
    scores = cross_val_score(classifier, attributes, classe, cv=kf)
    return str(scores.mean())


def splited(classifier,attributes,classe,split):
    X_train, X_test, y_train, y_test = train_test_split(attributes, classe, test_size=split,
                                                        random_state=42)
    classifier.fit(X_train, y_train)
    y_pred = classifier.predict(X_test)

    # Evaluate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    return str(accuracy)
def test_naive(attributes,classes):
    nb_classifier = GaussianNB()
    accurace = tenfold(nb_classifier, attributes, classes)
    print("Mean Accuracy:", accurace)

def splited_naive(atributes,classes,split):
    nb_classifier = GaussianNB()
    acuracy = splited(nb_classifier, atributes, classes, split)
    print("Split " + str(split * 100) + "% Accuracy:", acuracy)

def test_tree(atributes,classes):
    dt_classifier = DecisionTreeClassifier(random_state=42)
    accurace = tenfold(dt_classifier, atributes, classes)
    print("Mean Accuracy:", accurace)

def splited_tree(atributes,classes,split):
    dt_classifier = DecisionTreeClassifier(random_state=42)
    acuracy =splited(dt_classifier, atributes, classes, split)
    print("Split " + str(split * 100) + "% Accuracy:", acuracy)

def test_knm(atributes,classes,neighbors=1):
    knn = KNeighborsClassifier(n_neighbors=neighbors)
    knn.fit(atributes, classes)
    kf = KFold(n_splits=10, shuffle=True, random_state=int(time.time()%100))
    scores = cross_val_score(knn, atributes, classes, cv=kf)
    #for i, score in enumerate(scores, 1):
        #print(f"Fold {i}: {score}")

    # Calculate and print mean accuracy
    print("KNN acuraci:", round(scores.mean()*100,2))

def splitedt_knm(atributes,classes,porcent,neighbors=1):
    X_train, X_test, y_train, y_test = train_test_split(atributes, classes, test_size=porcent,
                                                        random_state=int(time.time()%100))

    # Create KNN classifier with k=5
    knn = KNeighborsClassifier(n_neighbors=neighbors)

    # Train the classifier
    knn.fit(X_train, y_train)

    # Make predictions on the testing set
    y_pred = knn.predict(X_test)

    # Evaluate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print("Split "+str(porcent*100)+"% Accuracy:", round(accuracy*100,2),"%")

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

print("Removendo da base outliners usando treshhold 3 e o pandas")
if(not os.path.isfile("checkpoint/redusida1.csv")):
    print("Testando dados")
    atribute = df.iloc[:, :-1]
    classe = df.iloc[:, -1]
    test_knm(atribute, classe)
    test_tree(atribute, classe)
    df_cleaned = df
    for colum in df.columns:
        if(colum != "class"):
            plt.figure(figsize=(8, 6))
            plt.boxplot(df[colum])
            plt.title(f'Box plot of {colum}')
            plt.xlabel('Feature')
            plt.ylabel('Value')
            plt.savefig(f'checkpoint/boxplot_{colum}.png')
            df_cleaned = remove_outliers(df_cleaned, colum)
    df_cleaned.to_csv('checkpoint/redusida1.csv', index=False)
    print("Testando dados")
    atribute = df_cleaned.iloc[:, :-1]
    classe = df_cleaned.iloc[:, -1]
    test_knm(atribute,classe)
    test_tree(atribute,classe)
else:
    df_cleaned = pd.read_csv('checkpoint/redusida1.csv')
if(not os.path.isfile("checkpoint/redusida2.csv")):
    print("Removendo os artibutos delta trends")
    columns_to_remove = ['max_delta', 'avg_delta',"min_delta"]
    df_reduced = df.drop(columns=columns_to_remove)
    df_reduced.to_csv('checkpoint/redusida2.csv', index=False)
    print("Testando dados")
    atribute = df_reduced.iloc[:, :-1]
    classe = df_reduced.iloc[:, -1]
    test_knm(atribute,classe)
    test_tree(atribute,classe)
else:
    df_reduced = pd.read_csv('checkpoint/redusida2.csv')
if(not os.path.isfile("checkpoint/redusida3.csv")):
    print("Aplicando PCA")
    atribute = df.iloc[:, :-1]
    classe = df.iloc[:, -1]
    pca = PCA(n_components=0.95)
    reducedatributes = pca.fit_transform(atribute)
    test_knm(reducedatributes,classe)
    test_tree(reducedatributes,classe)
    data_pca = pd.concat([pd.DataFrame(reducedatributes), classe], axis=1)
    data_pca.to_csv('checkpoint/redusida3.csv', index=False)
else:
    data_pca = pd.read_csv('checkpoint/redusida3.csv')
print("===================")
print("===================")
print("Checkpoint 3")
if not os.path.isfile("checkpoint/redusida3.csv"):
    databases = [df,df_cleaned,df_reduced,data_pca]
    print("KNN")

    print("Testando dados completos")
    i = 0
    nb_classifier = GaussianNB()
    dt_classifier = DecisionTreeClassifier(random_state=42)
    trainers = ["Decision tree","Naive Bayes"]
    j=0

    for trainer in trainers:
        print("Trainer "+trainer)
        finalresult = []

        for database in databases:
            result = [[], [], [], []]
            i += 1
            atribute = database.iloc[:, :-1]
            classe = database.iloc[:, -1]
            if (j == 0):
                for k in [1,2,3,5,7,9,11]:
                    trainer = DecisionTreeClassifier(random_state=42,max_depth=k)
                    result[0].append(tenfold(trainer,atribute,classe))
                    result[1].append(splited(trainer,atribute,classe,0.1))
                    result[2].append(splited(trainer,atribute,classe,0.2))
                    result[3].append(splited(trainer,atribute,classe,0.3))
            else:
                trainer = GaussianNB(priors=None, var_smoothing=1e-9)
                result[0].append(tenfold(trainer, atribute, classe))
                result[1].append(splited(trainer, atribute, classe, 0.1))
                result[2].append(splited(trainer, atribute, classe, 0.2))
                result[3].append(splited(trainer, atribute, classe, 0.3))
            finalresult += result
        j+=1
        for line in finalresult:
            print(','.join(line))
selectors = ["10Fold","70/30"]
plt.figure(figsize=(8, 6))
plt.title('Melhor numero de neuronios')
plt.xlabel('Neuronios')
plt.ylabel('Acuracia')
bestNeurons = {"10Fold":6,"70/30":6}
atribute = df.iloc[:, :-1]
classe = df.iloc[:, -1]
for selector in selectors:
    hiddenlayers = {}
    testhidden = 6
    bestguess = 6
    downmax = False
    downmin = False
    marker = 'o'
    while not(downmax and downmin):
        mlp_classifier = MLPClassifier(hidden_layer_sizes=testhidden,random_state=42)
        if(selector == "10Fold"):
            marker = 's'
            result = tenfold(mlp_classifier, atribute, classe)
        else:
            result = splited(mlp_classifier, atribute, classe,0.3)

        hiddenlayers[testhidden] = result
        if(hiddenlayers[testhidden]>hiddenlayers[bestguess]):
            bestguess = testhidden
        elif(bestguess>testhidden):
            downmin = True
        elif(bestguess<testhidden):
            downmax = True
        if(downmin):
            testhidden += 1
            while testhidden in hiddenlayers.keys():
                testhidden += 1
        else:
            testhidden -= 1
            while testhidden in hiddenlayers.keys():
                testhidden -= 1
    bestNeurons[selector] = bestguess
    plt.scatter( [float(x) for x in hiddenlayers.keys()], [float(x) for x in hiddenlayers.values()],
              marker='o', label=selector)
print("melhor neuronio",bestNeurons)
plt.legend()
plt.savefig('checkpoint/hiddenlayers.png')
plt.figure(figsize=(8, 6))
plt.title('Melhor numero de interações')
plt.xlabel('Interações')
plt.ylabel('Acuracia')
bestIntractions = {"10Fold":False,"70/30":False}
for selector in selectors:
    interactions = {"100":0,"1000":0,"5000":0}
    marker = 'o'
    for interaction in interactions.keys():
        mlp_classifier = MLPClassifier(hidden_layer_sizes=int(bestNeurons[selector])
                                                              ,max_iter=int(interaction),random_state=42)

        if (selector == "10Fold"):
            marker = 's'
            result = tenfold(mlp_classifier, atribute, classe)
        else:
            result = splited(mlp_classifier, atribute, classe,0.3)
        interactions[interaction] = result
        if not bestIntractions[selector]:
            bestIntractions[selector] = interaction
        elif(interactions[bestIntractions[selector]]<interactions[interaction]):
            bestIntractions[selector] = interaction

    plt.plot( [float(x) for x in interactions.keys()], [float(x) for x in interactions.values()],
              marker='o', label=selector)
print("melhor interacoes",bestIntractions)
plt.legend()
plt.savefig('checkpoint/interactions.png')
plt.figure(figsize=(8, 6))
plt.title('Melhor taxa de aprendizado')
plt.xlabel('Interações')
plt.ylabel('Acuracia')
bestLR = {"10Fold":False,"70/30":False}
for selector in selectors:
    lrs = {"0.001": 0, "0.01": 0, "0.1": 0}
    marker = 'o'
    for lr in lrs.keys():
        mlp_classifier = MLPClassifier(hidden_layer_sizes=int(bestNeurons[selector]),
                                       max_iter=int(bestIntractions[selector]),
                                       learning_rate_init=float(lr),
                                       random_state=42)

        if (selector == "10Fold"):
            marker = 's'
            result = tenfold(mlp_classifier, atribute, classe)
        else:
            result = splited(mlp_classifier, atribute, classe, 0.3)
        lrs[lr] = result
        if not bestLR[selector]:
            bestLR[selector] = lr
        elif (lrs[bestLR[selector]] < lrs[lr]):
            bestLR[selector] = lr

    plt.plot([float(x) for x in lrs.keys()], [float(x) for x in lrs.values()],
             marker=marker, label=selector)
print("melhor taxa de aprendizado",bestLR)
plt.legend()
plt.savefig('checkpoint/learningrate.png')

bestParameters = {"10Fold":False,"70/30":False}
parameters = {'max_iter': [100,500,1000,2000 ], 'learning_rate_init': [0.001,0.01,0.1] ,
'hidden_layer_sizes':np.arange(10, 100), 'random_state':[0,1,2,3,4,5,6,7,8,9]}
for selector in selectors:
    mlp = MLPClassifier()
    if (selector == "10Fold"):
        kt = KFold(n_splits=10, shuffle=True, random_state=42)
        clf = GridSearchCV(mlp, parameters, n_jobs=-1,cv=kt)
        clf.fit(atribute, classe)
        print("Best Parameters 10Fold:", clf.best_params_)
    else:
        X_train, X_test, y_train, y_test = train_test_split(atribute, classe, test_size=0.3, random_state=42)
        grid_search = GridSearchCV(mlp, parameters, cv=5, n_jobs=-1, verbose=1)
        grid_search.fit(X_train, y_train)
        print("Best Parameters 70/30:", grid_search.best_params_)
print("******")

#fig, ax = plt.subplots()
#boxplot = df.boxplot(ax=ax,column=['peso_fonte'])
#plt.show()
