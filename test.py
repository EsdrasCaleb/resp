import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc

# Load dataset from CSV
df = pd.read_csv('checkpoint/data.csv')

# Assuming the last column is the target variable and others are features
X = df.iloc[:, :-1]  # Features
y = df.iloc[:, -1]   # Target

# Perform KMeans clustering
n_clusters = 6  # Example: using 5 clusters
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
cluster_labels = kmeans.fit_predict(X)

# Convert cluster labels to one-hot encoding
cluster_labels_onehot = np.eye(n_clusters)[cluster_labels]

# Concatenate cluster labels (or one-hot encoded) with original features
X_clustered = np.concatenate((X, cluster_labels_onehot), axis=1)

# Define classifiers
classifiers = {
    'KNN': KNeighborsClassifier(),
    'Naive Bayes': GaussianNB(),
    'Decision Tree': DecisionTreeClassifier(random_state=42,max_depth=5),
    'MPL':MLPClassifier(),
}

# Evaluate classifiers using cross-validation
for clf_name, clf in classifiers.items():
    scores = cross_val_score(clf, X, y, cv=10)
    print(f'{clf_name} Accuracy Normal: {scores.mean():.2f} (+/- {scores.std() * 2:.2f})')
    scores = cross_val_score(clf, X_clustered, y, cv=10)
    print(f'{clf_name} Accuracy Clustered: {scores.mean():.2f} (+/- {scores.std() * 2:.2f})')
