import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import rand_score
from sklearn.cluster import AgglomerativeClustering
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
import numpy as np


from db_paper import db_paper
import csv
import os.path
import time

original_database = pd.read_csv('checkpoint/data.csv')
df_lessattr = pd.read_csv('checkpoint/redusida2.csv')
basesname = ["Orignal Dataset", "Reduced Dataset 2"]
databases = [original_database,df_lessattr]
indice = 0
label_encoder = LabelEncoder()
for db in databases:
    X = db.iloc[:, :-1]
    y_true = label_encoder.fit_transform(db.iloc[:, -1])
    # Define range for k
    k_range = range(2, 21)

    # Store the Davies-Bouldin index for each k
    db_indices = []
    db_hi_indeces = []

    # Perform clustering for each k
    for k in k_range:
        kmeans_optimal = KMeans(n_clusters=k, n_init=10, random_state=42)
        y_pred = kmeans_optimal.fit_predict(X)
        rikmeans = rand_score(y_true, y_pred)
        hc = AgglomerativeClustering(n_clusters=k)
        y_pred = hc.fit_predict(X)
        riho = rand_score(y_true, y_pred)

        db_indices.append(rikmeans)
        db_hi_indeces.append(riho)

    # Plot the Davies-Bouldin index for each k
    plt.figure(figsize=(10, 6))
    plt.plot(k_range, db_indices, marker='o',color='blue')
    plt.title('CR for k (k-means) with '+basesname[indice])
    plt.xlabel('Number of Cluster(k)')
    plt.ylabel('Corrected Rand Index')
    plt.plot(k_range, db_hi_indeces, marker='x', color='red')
    plt.xticks(k_range)
    plt.grid(True)
    plt.savefig("checkpoint/cr_"+str(indice)+".png")
    indice+=1