import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import davies_bouldin_score
from sklearn.cluster import AgglomerativeClustering
import matplotlib.pyplot as plt
import numpy as np


from db_paper import db_paper
import csv
import os.path
import time

original_database = pd.read_csv('checkpoint/data.csv')
df_lessattr = pd.read_csv('checkpoint/redusida2.csv')
basesname = ["Orignal Dataset","Reduced Dataset 2"]
databases = [original_database.iloc[:, :-1],df_lessattr.iloc[:, :-1]]
indice = 0
for db in databases:
    # Define range for k
    k_range = range(2, 21)

    # Store the Davies-Bouldin index for each k
    db_indices = []
    db_hi_indeces = []

    # Perform clustering for each k
    for k in k_range:
        db_index_k = []
        dbh_index_k = []
        for i in [5,20,30,42,7]:  # 5 tests with different initial states
            kmeans = KMeans(n_clusters=k, n_init=1, random_state=i)
            kmeans.fit(db)
            hc = AgglomerativeClustering(n_clusters=k)
            labels = kmeans.labels_
            db_index = davies_bouldin_score(db, labels)
            db_index_k.append(db_index)
            labels = hc.fit_predict(db)
            dbh_index = davies_bouldin_score(db,labels)
            dbh_index_k.append(dbh_index)

        # Average Davies-Bouldin index for the current k
        db_indices.append(np.mean(db_index_k))
        db_hi_indeces.append(np.mean(dbh_index_k))

    # Plot the Davies-Bouldin index for each k
    plt.figure(figsize=(10, 6))
    plt.plot(k_range, db_indices, marker='o', color='blue', label='DB for KMeans')
    plt.title('Davies-Bouldin Index per cluster')
    plt.xlabel('Number of Cluster(k)')
    plt.ylabel('Davies-Bouldin Index')
    plt.plot(k_range, db_hi_indeces, marker='x', color='red', label='DB for Hierarchical Clustering')
    plt.xticks(k_range)
    plt.grid(True)
    plt.savefig("checkpoint/db"+str(indice)+".png")
    indice+=1