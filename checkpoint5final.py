import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, KFold, cross_val_predict, StratifiedKFold
from sklearn.metrics import accuracy_score, mean_squared_error, classification_report, roc_curve, auc
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
import scikit_posthocs as sp
from scipy.stats import friedmanchisquare, chi2
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier

# Load the data
df = pd.read_csv('checkpoint/data.csv')
df_cleaned = pd.read_csv('checkpoint/redusida1.csv')
df_reduced = pd.read_csv('checkpoint/redusida2.csv')
data_pca = pd.read_csv('checkpoint/redusida3.csv')
databases = [df, df_cleaned, df_reduced, data_pca]

# Define classifiers and their parameters
klen = [3, 5, 7]
classifiers = ["KNN", "Decision tree", "Naive Bayes", "MPL (Plot)", "MPL (GrindSearch)"]
databasesName = ["Original", "No outliners r1", "Menos atributos r2", "PCA R3"]

label_encoder = LabelEncoder()
print('Classifier,Trainer,3,5,7')

resultsdata = [[{}, {}, {}, {}], [{}, {}, {}, {}], [{}, {}, {}, {}], [{}, {}, {}, {}]]
i = 0
for classifiername in classifiers:
    finalresult = []
    j = 0
    for database in databases:
        result = [[classifiername + databasesName[j], '10fold'],
                  [classifiername + databasesName[j], '10/90'],
                  [classifiername + databasesName[j], '20/80'],
                  [classifiername + databasesName[j], '30/70']]
        atribute = database.iloc[:, :-1]
        y = database.iloc[:, -1]
        classe = label_encoder.fit_transform(y)

        if i < 2:
            for k in klen:
                if i == 0:
                    trainer = KNeighborsClassifier(n_neighbors=k)
                else:
                    trainer = DecisionTreeClassifier(random_state=42, max_depth=k)

                datascore = cross_val_predict(trainer, atribute, classe, cv=10)
                resultsdata[j][0][classifiername + "k" + str(k) + "kfold"] = datascore

                X_train, X_test, y_train, y_test = train_test_split(atribute, classe, test_size=0.1, random_state=42)
                trainer.fit(X_train, y_train)
                datascore = trainer.predict(X_test)
                resultsdata[j][1][classifiername + "k" + str(k) + "split10/90"] = datascore

                X_train, X_test, y_train, y_test = train_test_split(atribute, classe, test_size=0.2, random_state=42)
                trainer.fit(X_train, y_train)
                datascore = trainer.predict(X_test)
                resultsdata[j][2][classifiername + "k" + str(k) + "split20/80"] = datascore

                X_train, X_test, y_train, y_test = train_test_split(atribute, classe, test_size=0.3, random_state=42)
                trainer.fit(X_train, y_train)
                datascore = trainer.predict(X_test)
                resultsdata[j][3][classifiername + "k" + str(k) + "split30/70"] = datascore

        elif i == 2:
            trainer = GaussianNB()
            datascore = cross_val_predict(trainer, atribute, classe, cv=10)
            resultsdata[j][0][classifiername + "kfold"] = datascore

            X_train, X_test, y_train, y_test = train_test_split(atribute, classe, test_size=0.1, random_state=42)
            trainer.fit(X_train, y_train)
            datascore = trainer.predict(X_test)
            resultsdata[j][1][classifiername + "split10/90"] = datascore

            X_train, X_test, y_train, y_test = train_test_split(atribute, classe, test_size=0.2, random_state=42)
            trainer.fit(X_train, y_train)
            datascore = trainer.predict(X_test)
            resultsdata[j][2][classifiername + "split20/80"] = datascore

            X_train, X_test, y_train, y_test = train_test_split(atribute, classe, test_size=0.3, random_state=42)
            trainer.fit(X_train, y_train)
            datascore = trainer.predict(X_test)
            resultsdata[j][3][classifiername + "split30/70"] = datascore

        else:
            if i == 3:
                trainerTen = MLPClassifier(hidden_layer_sizes=7, max_iter=1000, learning_rate_init=0.01,
                                           random_state=42)
                trainerSplited = MLPClassifier(hidden_layer_sizes=6, max_iter=1000, learning_rate_init=0.001,
                                               random_state=42)
            else:
                trainerTen = MLPClassifier(hidden_layer_sizes=111, max_iter=500, learning_rate_init=0.001,
                                           random_state=9)
                trainerSplited = MLPClassifier(hidden_layer_sizes=95, max_iter=200, learning_rate_init=0.01,
                                               random_state=3)

            datascore = cross_val_predict(trainerTen, atribute, classe, cv=10)
            resultsdata[j][0][classifiername + "kfold"] = datascore

            X_train, X_test, y_train, y_test = train_test_split(atribute, classe, test_size=0.1, random_state=42)
            trainerSplited.fit(X_train, y_train)
            datascore = trainerSplited.predict(X_test)
            resultsdata[j][1][classifiername + "split10/90"] = datascore

            X_train, X_test, y_train, y_test = train_test_split(atribute, classe, test_size=0.2, random_state=42)
            trainerSplited.fit(X_train, y_train)
            datascore = trainerSplited.predict(X_test)
            resultsdata[j][2][classifiername + "split20/80"] = datascore

            X_train, X_test, y_train, y_test = train_test_split(atribute, classe, test_size=0.3, random_state=42)
            trainerSplited.fit(X_train, y_train)
            datascore = trainerSplited.predict(X_test)
            resultsdata[j][3][classifiername + "split30/70"] = datascore

        j += 1
    i += 1

aux = ["Ten Fold", '90/10', '80/20', '70/30']

pd.set_option('display.max_rows', None)  # Show all rows
pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.width', None)  # Auto-adjust width to display data fully

j = 0
for resultsdb in resultsdata:
    print("=================")
    print(databasesName[j])
    i = 0
    atribute = databases[j].iloc[:, :-1]
    y = label_encoder.fit_transform(databases[j].iloc[:, -1])

    for results in resultsdb:
        results_df = pd.DataFrame(results)
        stat, p_value = friedmanchisquare(*[results_df[col] for col in results_df])
        print("\nFriedman test results " + aux[i] + " :")
        print(f'Statistic: {stat}, p-value: {p_value}')
        k = results_df.shape[1]
        df = k - 1
        alpha = 0.05
        critical_value = chi2.ppf(1 - alpha, df)
        print(f'Critical value: {critical_value}')

        if stat > critical_value:
            print("Reject the null hypothesis (H0). There are significant differences between the models.")
        else:
            print("Fail to reject the null hypothesis (H0). There are no significant differences between the models.")

        if i == 0:
            kft = StratifiedKFold(n_splits=10, shuffle=False)
            y_test = np.empty_like(y)
            for train_index, test_index in kft.split(atribute, y):
                y_test[test_index] = y[test_index]
        else:
            X_train, X_test, y_train, y_test = train_test_split(atribute, y, test_size=i * 0.1, random_state=42)

        print("Classification Report " + str(i))

        plt.figure(figsize=(8, 6))

        for model_name, y_pred in results.items():
            y_pred_i = np.array(results.values()).flatten()
            print(classification_report(y_test, y_pred_i))
            fpr, tpr, _ = roc_curve(y_test, y_pred_i)  #
            roc_auc = auc(fpr, tpr)
            plt.plot(fpr, tpr, label=f'{model_name} (AUC = {roc_auc:.2f})')

        plt.plot([0, 1], [0, 1], color='gray', linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver Operating Characteristic (ROC) Curve')
        plt.legend(loc="lower right")
        plt.grid(True)
        plt.savefig("checkpoint/roc" + databasesName[j] + aux[i] + ".png")

        i += 1
    j += 1
