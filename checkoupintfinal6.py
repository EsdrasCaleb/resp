import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import davies_bouldin_score, adjusted_rand_score, rand_score
from sklearn.cluster import KMeans, AgglomerativeClustering
import scikit_posthocs as sp
from sklearn.preprocessing import LabelEncoder

# Load data from CSV
label_encoder = LabelEncoder()
databases = [pd.read_csv('checkpoint/data.csv'), pd.read_csv('checkpoint/redusida2.csv')]
basesname = ["Original Dataset", "Reduced Dataset 2"]
results_db = [[], []]
results_ari = [[], []]

for idx, database in enumerate(databases):
    X = database.iloc[:, :-1]  # assuming the last column is the true labels or it's not needed
    y_true = label_encoder.fit_transform(database.iloc[:, -1])

    # Settings
    n_clusters_range = range(2, 21)
    results_db_temp = []
    results_ari_temp = []

    for n_clusters in n_clusters_range:
        # KMeans
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        y_pred_kmeans = kmeans.fit_predict(X)
        db_score_kmeans = davies_bouldin_score(X, y_pred_kmeans)
        ari_kmeans = adjusted_rand_score(y_true, y_pred_kmeans)
        results_db[idx].append(db_score_kmeans)
        results_db_temp.append(('KMeans', n_clusters, db_score_kmeans))
        results_ari[idx].append(ari_kmeans)
        results_ari_temp.append(('KMeans', n_clusters, ari_kmeans))

        # AgglomerativeClustering
        agg_clust = AgglomerativeClustering(n_clusters=n_clusters)
        y_pred_agg = agg_clust.fit_predict(X)
        db_score_agg = davies_bouldin_score(X, y_pred_agg)
        ari_agg = adjusted_rand_score(y_true, y_pred_agg)
        results_db[idx].append(db_score_agg)
        results_db_temp.append(('AgglomerativeClustering', n_clusters, db_score_agg))
        results_ari[idx].append(ari_agg)
        results_ari_temp.append(('AgglomerativeClustering', n_clusters, ari_agg))

    # Convert results to DataFrames for post-hoc analysis
    results_db_df = pd.DataFrame(results_db_temp, columns=['Algorithm', 'n_clusters', 'davies_bouldin_score'])
    results_ari_df = pd.DataFrame(results_ari_temp, columns=['Algorithm', 'n_clusters', 'adjusted_rand_score'])

    # Perform post-hoc Wilcoxon signed-rank test
    p_values_db = sp.posthoc_wilcoxon(results_db_df, group_col='Algorithm', val_col='davies_bouldin_score')
    print("\nPost-hoc Wilcoxon test results Davies-Bouldin " + basesname[idx])
    print(p_values_db)

    p_values_ari = sp.posthoc_wilcoxon(results_ari_df, group_col='Algorithm', val_col='adjusted_rand_score')
    print("\nPost-hoc Wilcoxon test results Adjusted Rand " + basesname[idx])
    print(p_values_ari)

array_aux = ["KMeans Original Dataset", "Agglomerative Original Dataset",
             "KMeans Reduced Dataset 2", "Agglomerative Reduced Dataset 2"]
color = ["red", "blue", "green", "yellow"]
markers = ['o', 's', '^', 'D']

plt.figure(figsize=(10, 6))
plt.title('Davies-Bouldin Index per cluster')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('Davies-Bouldin Index')
plt.xticks(n_clusters_range)
plt.grid(True)

for i in range(2):
    for j in range(2):
        plt.plot(n_clusters_range, results_db[i][j::2], marker=markers[j], color=color[2 * i + j], label=array_aux[2 * i + j])

plt.legend()
plt.savefig("checkpoint/dbindexcomplete.png")
plt.show()

plt.figure(figsize=(10, 6))
plt.title('Adjusted Rand Index per cluster')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('Adjusted Rand Index')
plt.xticks(n_clusters_range)
plt.grid(True)

for i in range(2):
    for j in range(2):
        plt.plot(n_clusters_range, results_ari[i][j::2], marker=markers[j], color=color[2 * i + j], label=array_aux[2 * i + j])

plt.legend()
plt.savefig("checkpoint/randindexcomplete.png")
plt.show()
