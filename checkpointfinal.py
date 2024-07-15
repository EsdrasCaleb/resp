import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score,KFold, cross_val_predict
from sklearn.metrics import accuracy_score, mean_squared_error, classification_report, roc_curve, auc
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
import scikit_posthocs as sp
from scipy.stats import friedmanchisquare, chi2
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
models = {
    'Random Forest':1,
    'Logistic Regression': 2,
    'SVM': 3
}



def tenfold(classifier,attributes,classe):
    kft = KFold(n_splits=10, shuffle=True, random_state=42)
    y_pred = cross_val_predict(classifier, attributes, classe, cv=kft)
    return [str(1-mean_squared_error(classe,y_pred)),y_pred]


def splited(classifier,attributes,classe,split):
    X_train, X_test, y_train, y_test = train_test_split(attributes, classe, test_size=split,
                                                        random_state=42)
    classifier.fit(X_train, y_train)
    y_pred = classifier.predict(X_test)

    # Evaluate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    return [str(accuracy), y_pred]

df = pd.read_csv('checkpoint/data.csv')
df_cleaned = pd.read_csv('checkpoint/redusida1.csv')
df_reduced = pd.read_csv('checkpoint/redusida2.csv')
data_pca = pd.read_csv('checkpoint/redusida3.csv')
databases = [df,df_cleaned,df_reduced,data_pca]
klen = [3,5,7]
classifiers = ["KNN","Decision tree","Naive Bayes","MPL (Plot)","MPL (GrindSearch)"]
databasesName = ["Original","No outliners r1","Menos atributos r2","PCA R3"]
i = 0
resultsdata = [[{},{},{},{}],[{},{},{},{}],[{},{},{},{}],[{},{},{},{}]]
label_encoder = LabelEncoder()
print('Classifier,Trainer,3,5,7')
for classifiername in classifiers:
    finalresult = []
    j = 0
    for database in databases:
        result = [[classifiername+databasesName[j],'10fold'],
                  [classifiername+databasesName[j],'10/90'],
                  [classifiername+databasesName[j],'20/80'],
                  [classifiername+databasesName[j],'30/70']]
        atribute = database.iloc[:, :-1]
        y = database.iloc[:, -1]
        classe = label_encoder.fit_transform(y)
        if(i < 2):
            for k in klen:
                trainer = None
                if(i ==0):
                    trainer = KNeighborsClassifier(n_neighbors=k)
                else:
                    trainer = DecisionTreeClassifier(random_state=42,max_depth=k)
                datascore = tenfold(trainer, atribute, classe)
                result[0].append(datascore[0])
                resultsdata[j][0][classifiername+"k"+str(k)+"kfold"] =datascore[1]
                datascore = splited(trainer, atribute, classe, 0.1)
                result[1].append(datascore[0])
                resultsdata[j][1][classifiername + "k" + str(k) + "split10/90"] = datascore[1]
                datascore = splited(trainer, atribute, classe, 0.2)
                result[2].append(datascore[0])
                resultsdata[j][2][classifiername + "k" + str(k) + "split20/80"] = datascore[1]
                datascore = splited(trainer, atribute, classe, 0.3)
                resultsdata[j][3][classifiername + "k" + str(k) + "split30/70"] = datascore[1]
                result[3].append(datascore[0])
        elif(i==2):
            trainer = GaussianNB(priors=None, var_smoothing=1e-9)
            datascore = tenfold(trainer, atribute, classe)
            result[0].append(datascore[0])
            resultsdata[j][0][classifiername + "kfold"] = datascore[1]
            datascore = splited(trainer, atribute, classe, 0.1)
            result[1].append(datascore[0])
            resultsdata[j][1][classifiername + "split10/90"] = datascore[1]
            datascore = splited(trainer, atribute, classe, 0.2)
            result[2].append(datascore[0])
            resultsdata[j][2][classifiername + "split20/80"] = datascore[1]
            datascore = splited(trainer, atribute, classe, 0.3)
            resultsdata[j][3][classifiername + "split30/70"] = datascore[1]
            result[3].append(datascore[0])
        else:
            if(i==3):
                trainerTen = MLPClassifier(hidden_layer_sizes=7, max_iter=1000, learning_rate_init=0.01, random_state=42)
                trainerSplited = MLPClassifier(hidden_layer_sizes=6, max_iter=1000, learning_rate_init=0.001,
                                            random_state=42)
            else:
                trainerTen = MLPClassifier(hidden_layer_sizes=111, max_iter=500,
                                            learning_rate_init=0.001, random_state=9)
                trainerSplited = MLPClassifier(hidden_layer_sizes=95, max_iter=200,
                                                learning_rate_init=0.01, random_state=3)
            trainer = trainerTen
            datascore = tenfold(trainer, atribute, classe)
            result[0].append(datascore[0])
            resultsdata[j][0][classifiername + "kfold"] = datascore[1]

            trainer = trainerSplited
            datascore = splited(trainer, atribute, classe, 0.1)
            result[1].append(datascore[0])
            resultsdata[j][1][classifiername + "split10/90"] = datascore[1]
            datascore = splited(trainer, atribute, classe, 0.2)
            result[2].append(datascore[0])
            resultsdata[j][2][classifiername + "split20/80"] = datascore[1]
            datascore = splited(trainer, atribute, classe, 0.3)
            resultsdata[j][3][classifiername + "split30/70"] = datascore[1]
            result[3].append(datascore[0])

        finalresult += result
        j += 1
    for line in finalresult:
        print(','.join(line))
    i += 1


aux = ["Ten Fold",'90/10','80/20','70/30']
# Convert to DataFrame for easier manipulation
# Adjust Pandas display options to show full matrix
pd.set_option('display.max_rows', None)  # Show all rows
pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.width', None)  # Auto-adjust width to display data fully
j=0
for resultsdb in resultsdata:
    print("=================")
    print(databasesName[j])
    i = 0
    atribute = databases[j].iloc[:, :-1]

    y = label_encoder.fit_transform( databases[j].iloc[:, -1])
    for results in resultsdb:
        results_df = pd.DataFrame(results)
        # Perform the Friedman test
        stat, p_value = friedmanchisquare(*[results_df[col] for col in results_df])
        print("\nFriedman test results "+aux[i]+" :")
        print(f'Statistic: {stat}, p-value: {p_value}')
        # Determine the critical value
        k = results_df.shape[1]
        df = k - 1
        alpha = 0.05
        critical_value = chi2.ppf(1 - alpha, df)
        print(f'Critical value: {critical_value}')

        # Decision rule
        if stat > critical_value:
            print("Reject the null hypothesis (H0). There are significant differences between the models.")
        else:
            print("Fail to reject the null hypothesis (H0). There are no significant differences between the models.")

        results_df_cv_long = results_df.melt(var_name='Model', value_name='Prediction')
        # Perform the Wilcoxon signed-rank test
        posthoc_results = sp.posthoc_wilcoxon(results_df_cv_long,group_col='Model', val_col='Prediction',  p_adjust='holm')
        print("\nPost-hoc Wilcoxon test results "+aux[i]+":")
        # Fill the new DataFrame
        output_data = []
        #for inex, row in posthoc_results.iterrows():
        #    for col in posthoc_results.columns:
        #        if inex != col:
        #            output_data.append({
        #                'Classifier1': inex,
        #                'Classifier2': col,
        #                'Pvalue': row[col]
        #            })
        #output_df = pd.DataFrame(output_data)

        if i == 0:
            continue
            kft = KFold(n_splits=10, shuffle=True, random_state=42)
            y_test = np.empty_like(y)
            for train_index, test_index in kft.split(atribute, y):
                y_test[test_index] = y[test_index]
        else:
            X_train, X_test, y_train, y_test = train_test_split(atribute, y, test_size=i * 0.1, random_state=42)

        print("Classification Report " + str(i))

        plt.figure(figsize=(8, 6))

        for model_name, y_pred in results.items():
            y_pred_i = results.values()
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

        #def format_float(x):
        #    if abs(x) < 0.0001:
        #        return f"{x:.2e}"  # Scientific notation for values less than 0.0001
        #    else:
        #        return f"{x:.4f}"  # Default formatting for other values

        #print(output_df.to_latex(index=False,float_format=lambda x: format_float(x)))
        i += 1
    j += 1

