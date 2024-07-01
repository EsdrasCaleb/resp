import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score,KFold, cross_val_predict
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error
import scikit_posthocs as sp
from scipy.stats import friedmanchisquare


def kpredic(classifier, X, y):
    kf = KFold(n_splits=10, shuffle=True, random_state=42)
    return cross_val_predict(classifier, X, y, cv=kf)

def splitedpredict(classifier, X, y,split):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=split,
                                                        random_state=42)
    classifier.fit(X_train, y_train)
    return classifier.predict(X_test)

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

databases = [df,df_cleaned,df_reduced,data_pca]
k = [3,5,7]
classifiers = []

# Load data from CSV
df = pd.read_csv('your_data.csv')

# Assume the last column is the target
X = df.iloc[:, :-1].values
y = df.iloc[:, -1].values

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train three models
rf = RandomForestRegressor(random_state=42)
lr = LinearRegression()
svr = SVR()

rf.fit(X_train, y_train)
lr.fit(X_train, y_train)
svr.fit(X_train, y_train)

# Predict on the test set
y_pred_rf = rf.predict(X_test)
y_pred_lr = lr.predict(X_test)
y_pred_svr = svr.predict(X_test)

# Evaluate the models
mse_rf = mean_squared_error(y_test, y_pred_rf)
mse_lr = mean_squared_error(y_test, y_pred_lr)
mse_svr = mean_squared_error(y_test, y_pred_svr)

print(f'Mean Squared Error (RF): {mse_rf}')
print(f'Mean Squared Error (LR): {mse_lr}')
print(f'Mean Squared Error (SVR): {mse_svr}')

# Prepare data for statistical analysis
results = {
    'Random Forest': y_pred_rf,
    'Linear Regression': y_pred_lr,
    'SVR': y_pred_svr
}

# Convert to DataFrame for easier manipulation
results_df = pd.DataFrame(results)

# Perform the Wilcoxon signed-rank test
posthoc_results = sp.posthoc_wilcoxon(results_df, p_adjust='holm')
print("Post-hoc Wilcoxon test results:")
print(posthoc_results)

# Perform the Friedman test
stat, p_value = friedmanchisquare(y_pred_rf, y_pred_lr, y_pred_svr)
print("\nFriedman test results:")
print(f'Statistic: {stat}, p-value: {p_value}')

# Define models
models = {
    'Random Forest': RandomForestRegressor(random_state=42),
    'Linear Regression': LinearRegression(),
    'SVR': SVR()
}

# Initialize KFold
kf = KFold(n_splits=10, shuffle=True, random_state=42)

# Perform 10-fold cross-validation
predictions = {name: cross_val_predict(model, X, y, cv=kf) for name, model in models.items()}

# Evaluate the models using MSE
mse_scores = {name: mean_squared_error(y, pred) for name, pred in predictions.items()}
for name, mse in mse_scores.items():
    print(f'Mean Squared Error ({name}): {mse}')

# Convert predictions to DataFrame
results_df = pd.DataFrame(predictions)

# Perform the Wilcoxon signed-rank test
posthoc_results = sp.posthoc_wilcoxon(results_df, p_adjust='holm')
print("\nPost-hoc Wilcoxon test results:")
print(posthoc_results)

# Perform the Friedman test
stat, p_value = friedmanchisquare(*[results_df[col] for col in results_df])
print("\nFriedman test results:")
print(f'Statistic: {stat}, p-value: {p_value}')