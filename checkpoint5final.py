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



def tenfold(classifier,attributes,classe_y):
    kft = KFold(n_splits=10, shuffle=True, random_state=42)
    y_pred = cross_val_predict(classifier, attributes, classe_y, cv=kft)
    return [str(1-mean_squared_error(classe_y,y_pred)),y_pred,classe_y]


def splited(classifier,attributes,classe_y,split):
    X_train, X_test, y_train, y_test = train_test_split(attributes, classe_y, test_size=split,
                                                        random_state=42)
    classifier.fit(X_train, y_train)
    y_pred = classifier.predict(X_test)

    # Evaluate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    return [str(accuracy), y_pred,y_test]

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
frideman = {}
label_encoder = LabelEncoder()
print('Classifier,Trainer,3,5,7')
for classifiername in classifiers:
    finalresult = []
    j = 0
    for database in databases:
        if(not databasesName[j] in frideman):
            frideman[databasesName[j]] = {}
        result = [[classifiername+databasesName[j],'10fold'],
                  [classifiername+databasesName[j],'10/90'],
                  [classifiername+databasesName[j],'20/80'],
                  [classifiername+databasesName[j],'30/70']]
        atribute = database.iloc[:, :-1]
        y = database.iloc[:, -1]
        classe = label_encoder.fit_transform(y)
        fresult = []
        if(i < 2):
            for k in klen:
                fresult = []
                trainer = None
                if(i ==0):
                    trainer = KNeighborsClassifier(n_neighbors=k)
                else:
                    trainer = DecisionTreeClassifier(random_state=42,max_depth=k)
                datascore = tenfold(trainer, atribute, classe)
                result[0].append(datascore[0])
                fresult.append(float(datascore[0]))

                resultsdata[j][0][classifiername+"k"+str(k)+"kfold"] = [datascore[1],datascore[2]]
                datascore = splited(trainer, atribute, classe, 0.1)
                result[1].append(datascore[0])
                fresult.append(float(datascore[0]))

                resultsdata[j][1][classifiername + "k" + str(k) + "split10/90"] = [datascore[1],datascore[2]]
                datascore = splited(trainer, atribute, classe, 0.2)
                result[2].append(datascore[0])
                fresult.append(float(datascore[0]))

                resultsdata[j][2][classifiername + "k" + str(k) + "split20/80"] = [datascore[1],datascore[2]]
                datascore = splited(trainer, atribute, classe, 0.3)
                resultsdata[j][3][classifiername + "k" + str(k) + "split30/70"] = [datascore[1],datascore[2]]
                result[3].append(datascore[0])
                fresult.append(float(datascore[0]))
                frideman[databasesName[j]][classifiername+"k" + str(k)] = fresult
        elif(i==2):
            trainer = GaussianNB(priors=None, var_smoothing=1e-9)
            datascore = tenfold(trainer, atribute, classe)
            result[0].append(datascore[0])
            fresult.append(float(datascore[0]))
            resultsdata[j][0][classifiername + "kfold"] = [datascore[1],datascore[2]]

            datascore = splited(trainer, atribute, classe, 0.1)
            result[1].append(datascore[0])
            fresult.append(float(datascore[0]))
            resultsdata[j][1][classifiername + "split10/90"] = [datascore[1],datascore[2]]

            datascore = splited(trainer, atribute, classe, 0.2)
            result[2].append(datascore[0])
            fresult.append(float(datascore[0]))
            resultsdata[j][2][classifiername + "split20/80"] = [datascore[1],datascore[2]]

            datascore = splited(trainer, atribute, classe, 0.3)
            resultsdata[j][3][classifiername + "split30/70"] = [datascore[1],datascore[2]]
            result[3].append(datascore[0])
            fresult.append(float(datascore[0]))
            frideman[databasesName[j]][classifiername] = fresult

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
            resultsdata[j][0][classifiername + "kfold"] = [datascore[1],datascore[2]]
            fresult.append(float(datascore[0]))

            trainer = trainerSplited
            datascore = splited(trainer, atribute, classe, 0.1)
            result[1].append(datascore[0])
            resultsdata[j][1][classifiername + "split10/90"] = [datascore[1],datascore[2]]
            fresult.append(float(datascore[0]))

            datascore = splited(trainer, atribute, classe, 0.2)
            result[2].append(datascore[0])
            resultsdata[j][2][classifiername + "split20/80"] = [datascore[1],datascore[2]]
            fresult.append(float(datascore[0]))

            datascore = splited(trainer, atribute, classe, 0.3)
            resultsdata[j][3][classifiername + "split30/70"] = [datascore[1],datascore[2]]
            result[3].append(datascore[0])
            fresult.append(float(datascore[0]))
            frideman[databasesName[j]][classifiername] = fresult

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
print("=================")
print("Clasification report")
print("Dataset,Classifier,trategy,Class,precision,recall,f1-score,support")
for resultsdb in resultsdata:
    # print("=================")
    # print(databasesName[j])
    i = 0
    #
    # results_df = pd.DataFrame(frideman[databasesName[j]])
    # # Perform the Friedman test
    #
    # stat, p_value = friedmanchisquare(*[results_df[col] for col in results_df])
    # print("\nFriedman test results :")
    # print(f'Statistic: {stat}, p-value: {p_value}')
    # # Determine the critical value
    # k = results_df.shape[1]
    # df = k - 1
    # alpha = 0.05
    # critical_value = chi2.ppf(1 - alpha, df)
    # print(f'Critical value: {critical_value}')
    #
    # # Decision rule
    # if stat > critical_value:
    #     print("Reject the null hypothesis (H0). There are significant differences between the models.")
    # else:
    #     print("Fail to reject the null hypothesis (H0). There are no significant differences between the models.")

    for results in resultsdb:



        fig = plt.figure(figsize=(12, 6))
        ax = plt.subplot(111)
        for model_name, y_array in results.items():
            # print("Classification Report " + model_name+aux[i]+databasesName[j] )
            cr = classification_report(y_array[1], y_array[0],digits=4, output_dict=True)
            print(','.join([databasesName[j],model_name,aux[i],'irrelevant',str(round(cr['0']['precision']*100,2))+'%',
                            str(round(cr['0']['recall']*100,2))+'%',str(round(cr['0']['f1-score']*100,2))+'%',
                            str(cr['0']['support'])]))
            print(','.join([databasesName[j], model_name, aux[i], 'relevant', str(round(cr['1']['precision'] * 100,2)) + '%',
                            str(round(cr['1']['recall'] * 100,2)) + '%', str(round(cr['1']['f1-score'] * 100,2)) + '%',
                            str(cr['1']['support']) ]))
            fpr, tpr, _ = roc_curve(y_array[1], y_array[0])  #
            roc_auc = auc(fpr, tpr)
            ax.plot(fpr, tpr, label=f'{model_name} (AUC = {roc_auc:.2f})')

        ax.plot([0, 1], [0, 1], color='gray', linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver Operating Characteristic (ROC) Curve')
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
                  fancybox=True, shadow=True, ncol=5)
        plt.grid(True)
        plt.savefig("checkpoint/rocfinal" + databasesName[j] + aux[i].replace('/', '_') + ".png")
        i += 1
    j += 1

