import numpy as np
import pandas as pd
from scipy.stats import friedmanchisquare, wilcoxon
from matplotlib import pyplot as plt
import scikit_posthocs as sp
import csv


def format_float(x):
    if abs(x) < 0.0001:
        return f"{x:.2e}"  # Scientific notation for values less than 0.0001
    else:
        return f"{x:.4f}"  # Default formatting for other values

def plot_critical_distance(data_in,filename,x=18,y=24):
    data = (
        pd.DataFrame(data_in)
        .rename_axis('cv_fold')
        .melt(
            var_name='estimator',
            value_name='score',
            ignore_index=False,
        )
        .reset_index()
    )
    avg_rank = data.groupby('cv_fold').score.rank(pct=True).groupby(data.estimator).mean()
    test_results = sp.posthoc_conover_friedman(
        data,
        melted=True,
        block_col='cv_fold',
        group_col='estimator',
        y_col='score',
    )

    plt.figure(figsize=(x, y), dpi=100)
    plt.title('Critical difference diagram of average score ranks')
    print()
    sp.critical_difference_diagram(avg_rank, test_results)
    plt.savefig(filename+'cd.png')
    plt.close()
    plt.figure(figsize=(y, y), dpi=100)
    plt.title('Significance diagram of average score ranks')
    sp.sign_plot(test_results,data_in.keys(),labels=True)
    plt.savefig(filename + 'sg.png')


data = {
    'KNN': [0.75, 0.80, 0.78, 0.76, 0.79, 0.74, 0.81, 0.77, 0.80, 0.78],
    'MLP': [0.82, 0.85, 0.84, 0.83, 0.86, 0.81, 0.87, 0.84, 0.85, 0.83],
    'NB': [0.65, 0.67, 0.66, 0.68, 0.69, 0.65, 0.70, 0.67, 0.68, 0.66]
}


data = {}

with open('tofrideman.csv', newline='') as csvfile:

    reader = csv.DictReader(csvfile)

    for row in reader:
        if(not row['Method'] in data):
            data[row['Method']] = []

        data[row['Method']].append(float(row['accvar1']))
        if(row['accvar2']):
            methodname = row['Method']+'k5'
            if (not methodname in data):
                data[methodname] = []
            data[methodname].append(float(row['accvar2']))
        if (row['accvar3']):
            methodname = row['Method'] + 'k7'
            if (not methodname in data):
                data[methodname] = []
            data[methodname].append(float(row['accvar3']))
df = pd.DataFrame(data)
plot_critical_distance(data,'classifiers',20,8)
with open('tofridemanclassif.csv', newline='') as csvfile:

    reader = csv.DictReader(csvfile)

    for row in reader:
        namae = row['Methodo']+"_"+row['estimator']
        if(not namae in data):
            data[namae] = []

        data[namae].append(float(row['accvar10']))
        if(row['accvar20']):
            methodname = namae+'_20'
            if (not methodname in data):
                data[methodname] = []
            data[methodname].append(float(row['accvar20']))




# Perform the Friedman test
friedman_stat, friedman_p = friedmanchisquare(*[data[col] for col in data])
print(f"Friedman test statistic: {friedman_stat}, p-value: {friedman_p}")

# Perform Wilcoxon signed-rank test for pairwise comparisons
def wilcoxon_test(df):
    classifiers = df.columns
    p_values = {}
    output_data = []
    for i, clf1 in enumerate(classifiers):
        for j, clf2 in enumerate(classifiers):
            if i < j:
                stat, p = wilcoxon(df[clf1], df[clf2])
                p_values[(clf1, clf2)] = p
                output_data.append({
                    'Classifier1': clf1,
                    'Classifier2': clf2,
                    'Pvalue': p
                })
    output_df = pd.DataFrame(output_data)
    print(output_df.to_latex(index=False, float_format=lambda x: format_float(x)))
    return p_values

wilcoxon_p_values = wilcoxon_test(df)
print("Wilcoxon signed-rank test p-values:")
for pair, p in wilcoxon_p_values.items():
    print(f"{pair}: {p}")

# Create critical distance diagram


plot_critical_distance(data,'gerneral',20,18)
