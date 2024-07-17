import numpy as np
import pandas as pd
from scipy.stats import friedmanchisquare, wilcoxon
from matplotlib import pyplot as plt
from Orange.evaluation import compute_CD, graph_ranks

# Example data
data = {
    'KNN': [0.75, 0.80, 0.78, 0.76, 0.79, 0.74, 0.81, 0.77, 0.80, 0.78],
    'MLP': [0.82, 0.85, 0.84, 0.83, 0.86, 0.81, 0.87, 0.84, 0.85, 0.83],
    'NB': [0.65, 0.67, 0.66, 0.68, 0.69, 0.65, 0.70, 0.67, 0.68, 0.66]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Perform the Friedman test
friedman_stat, friedman_p = friedmanchisquare(df['KNN'], df['MLP'], df['NB'])
print(f"Friedman test statistic: {friedman_stat}, p-value: {friedman_p}")

# Perform Wilcoxon signed-rank test for pairwise comparisons
def wilcoxon_test(df):
    classifiers = df.columns
    p_values = {}
    for i, clf1 in enumerate(classifiers):
        for j, clf2 in enumerate(classifiers):
            if i < j:
                stat, p = wilcoxon(df[clf1], df[clf2])
                p_values[(clf1, clf2)] = p
    return p_values

wilcoxon_p_values = wilcoxon_test(df)
print("Wilcoxon signed-rank test p-values:")
for pair, p in wilcoxon_p_values.items():
    print(f"{pair}: {p}")

# Create critical distance diagram
def plot_critical_distance(data):
    df = pd.DataFrame(data)
    avg_ranks = df.rank(axis=1, method='min', ascending=False).mean().values
    names = list(data.keys())
    cd = compute_CD(avg_ranks, len(df))  # Use appropriate N for the number of datasets
    graph_ranks(avg_ranks, names, cd=cd, width=6)
    plt.show()

plot_critical_distance(data)
