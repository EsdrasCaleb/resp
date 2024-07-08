import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import rand_score
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.metrics import davies_bouldin_score, adjusted_rand_score
import scikit_posthocs as sp
from sklearn.preprocessing import LabelEncoder

# Load data from CSV
label_encoder = LabelEncoder()
data = pd.read_csv('checkpoint/redusida2.csv')
X = data.iloc[:, :-1]  # assuming the last column is the true labels or it's not needed
y_true =label_encoder.fit_transform(data.iloc[:, -1])

# Settings
n_clusters_range = range(2, 21)
initial_states = [5, 20, 30, 42, 7]

# Store results
results_db = []
results_ari = []

# Evaluate models
for n_clusters in n_clusters_range:
    for init_state in initial_states:
        # KMeans
        kmeans = KMeans(n_clusters=n_clusters, random_state=init_state)
        y_pred_kmeans = kmeans.fit_predict(X)
        db_score_kmeans = davies_bouldin_score(X, y_pred_kmeans)
        ari_kmeans = rand_score(y_true, y_pred_kmeans)
        results_db.append(('KMeans', n_clusters, init_state, db_score_kmeans))
        results_ari.append(('KMeans', n_clusters, init_state, ari_kmeans))

        # AgglomerativeClustering
        agg_clust = AgglomerativeClustering(n_clusters=n_clusters)
        y_pred_agg = agg_clust.fit_predict(X)
        db_score_agg = davies_bouldin_score(X, y_pred_agg)
        ari_agg =  rand_score(y_true, y_pred_agg)
        results_db.append(('AgglomerativeClustering', n_clusters, init_state, db_score_agg))
        results_ari.append(('AgglomerativeClustering', n_clusters, init_state, ari_agg))

# Convert results to DataFrames for post-hoc analysis
results_db_df = pd.DataFrame(results_db, columns=['Algorithm', 'n_clusters', 'init_state', 'davies_bouldin_score'])
results_ari_df = pd.DataFrame(results_ari, columns=['Algorithm', 'n_clusters', 'init_state', 'adjusted_rand_score'])

# Perform post-hoc Wilcoxon signed-rank test
pd.set_option('display.max_rows', None)  # Show all rows
pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.width', None)  # Auto-adjust width to display data fully

p_values_db = sp.posthoc_wilcoxon(results_db_df, group_col='Algorithm', val_col='davies_bouldin_score')
print("\nPost-hoc Wilcoxon test results David Boes:")
print(p_values_db)

p_values_ari = sp.posthoc_wilcoxon(results_ari_df, group_col='Algorithm', val_col='adjusted_rand_score')
print("\nPost-hoc Wilcoxon test results Rand:")
print(p_values_ari)



# Plot results
def plot_results(results, metric_name):
    fig, ax = plt.subplots(figsize=(12, 8))
    for model in results:
        df = pd.DataFrame(results[model], columns=['n_clusters', 'init_state', metric_name])
        for init_state in initial_states:
            subset = df[df['init_state'] == init_state]
            ax.plot(subset['n_clusters'], subset[metric_name], label=f'{model} (init_state={init_state})')

    ax.set_title(f'{metric_name} for KMeans and AgglomerativeClustering')
    ax.set_xlabel('Number of Clusters')
    ax.set_ylabel(metric_name)
    ax.legend()
    plt.savefig(f'{metric_name}_comparison.png')


# Plot Davies-Bouldin Score
plot_results(results_db, 'davies_bouldin_score')

# Plot Adjusted Rand Index
plot_results(results_ari, 'adjusted_rand_score')
