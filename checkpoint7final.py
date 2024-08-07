import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_predict, StratifiedKFold
from sklearn.metrics import accuracy_score, mean_squared_error
from sklearn.ensemble import AdaBoostClassifier, BaggingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import StackingClassifier
from sklearn.preprocessing import LabelEncoder
from weigthknm import WeightedKNeighborsClassifier
from weigtedmpl import WeightedMLPClassifier
import scikit_posthocs as sp
from scipy.stats import friedmanchisquare, chi2



base_mlp = MLPClassifier(random_state=42)
base_knn = KNeighborsClassifier()
# Define base classifiers
base_classifiers = {
    "AD":DecisionTreeClassifier(random_state=42),
    'k-NN': base_knn,
    'NB': GaussianNB(),
    'MLP': base_mlp
}

# Define parameter values
n_estimators_list = [10, 20]
max_features_list = [1,0.3, 0.5, 0.8]
splits = [(10, '10-fold'), (0.1, '90/10'), (0.2, '80/20'), (0.3, '70/30')]

# Function to perform evaluation
def evaluate_classifier(model, X, y, split):
    if split[1] == '10-fold':
        cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)
        y_pred = cross_val_predict(model, X, y, cv=cv)
        return [str(1-mean_squared_error(y,y_pred)), y_pred]
    else:
        test_size = split[0]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        return [accuracy_score(y_test, y_pred), y_pred]


kumites = [
    'Ada',
    'Bagging',
]



for datastring in ['checkpoint/data.csv','checkpoint/redusida2.csv']:
    resultsdata = [{},{},{},{}]
    # Train and evaluate classifiers with different configurations
    # Load data from CSV file
    # Update the path to your CSV file
    df = pd.read_csv(datastring)
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]
    # Encode the string labels into numerical values
    label_encoder = LabelEncoder()
    kumites = ["Ada Boosting",
                "Bagging"]

    print("base "+datastring)
    y = label_encoder.fit_transform(y)
    for kumite in kumites:
        for max_features in max_features_list:
            if kumite != kumites[1] and max_features != 1:
                continue
            print(f'Tabela {kumite} com features {max_features}')
            i = 0
            for split in splits:
                print("estrategia de selecao,estrategia estimador, 10,20")
                for name, clf in base_classifiers.items():
                    result = [split[1],name]
                    for n_estimators in n_estimators_list:
                        # AdaBoostClassifier
                        if(kumite == kumites[1]):
                            bagging_model = BaggingClassifier(estimator=clf, n_estimators=n_estimators, max_features=max_features, random_state=42)
                            bagging_accuracy = evaluate_classifier(bagging_model, X, y, split)
                            resultsdata[i]["begging "+split[1]+name+" est"+str(n_estimators)] = bagging_accuracy[1]
                            result.append(str(bagging_accuracy[0]))
                        else:
                            if(clf==base_knn):
                                clf = WeightedKNeighborsClassifier()
                            if(clf==base_mlp):
                                clf = WeightedMLPClassifier()
                            ada_model = AdaBoostClassifier(estimator=clf, n_estimators=n_estimators, random_state=42,algorithm='SAMME')
                            ada_accuracy = evaluate_classifier(ada_model, X, y, split)
                            resultsdata[i]["ada "+split[1] + name + " est" + str(n_estimators)] = ada_accuracy[1]
                            result.append(str(ada_accuracy[0]))
                        #print(f'AdaBoost with {name}, n_estimators={n_estimators}, max_features={max_features}, split={split[1]}')
                        #print(f'Accuracy: {ada_accuracy:.4f}')
                    
                    print(",".join(result), flush=True)
                i += 1
    
    print("Tabela Randon Florest", flush=True)
    n_estimators_list = [10, 100]
    criteria = ['gini', 'entropy', 'log_loss']
    print("estrategia de selecao,criterio, 10,20")

    for criterion in criteria:
        i = 0
        for split in splits:
            result = [split[1],criterion]
            for n_estimators in n_estimators_list:
                model = RandomForestClassifier(n_estimators=n_estimators, criterion=criterion, random_state=42)
                accuracy = evaluate_classifier(model, X, y, split)
                resultsdata[i]["RandomForest " +split[1]+" "+criterion + " est" + str(n_estimators)] = accuracy[1]
                result.append(str(accuracy[0]))
            print(",".join(result), flush=True)
            i += 1
    print("Tabela Staking")
    print("estrategia de selecao,Classificdores, Acuracia")
    n_classifiers_list = [10, 20]
    for n_classifiers in n_classifiers_list:
        base_estimators = [(f'knn_{i}', base_knn) for i in range(n_classifiers // 2)] + \
                        [(f'mlp_{i}', base_mlp) for i in range(n_classifiers // 2, n_classifiers)]
        i = 0
        for split in splits:
            # Define the StackingClassifier
            stacking_model = StackingClassifier(estimators=base_estimators, final_estimator=MLPClassifier(max_iter=1000), cv=5)
            
            # Evaluate the model
            accuracy = evaluate_classifier(stacking_model, X, y, split)
            resultsdata[i]["Stacking KNN MPL" + split[1] +" est d"] = accuracy[1]
            print(f'{split[1]}, {n_classifiers}, {accuracy[0]}', flush=True)
            i += 1
    base_estimators = [(f'ad_{i}', DecisionTreeClassifier(random_state=42,max_depth=5)) for i in range(2)]+ \
                        [(f'RF_{i}', RandomForestClassifier(n_estimators=20, criterion='entropy', random_state=42)) for i in range(1)] + \
                      [(f'RD_{i}', base_knn) for i
                       in range(2)] + \
                      [ ( f'mlp_{i}', MLPClassifier(hidden_layer_sizes=7, max_iter=1000, learning_rate_init=0.01, random_state=42)) for i in range(1) ]
    stacking_model = StackingClassifier(estimators=base_estimators, final_estimator=base_mlp, cv=10)
            
    # Evaluate the model
    accuracy = evaluate_classifier(stacking_model, X, y, (0.3, '70/30'))
    resultsdata[3]["Stacking MPL KNN NB RandFlorest 70/30" ] = accuracy[1]
    print(f'Stacking com decision tree e random forest {accuracy[0]}')
    i = 0
    aux = ["Ten Fold", '90/10', '80/20', '70/30']
    for results in resultsdata:
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

        posthoc_results = sp.posthoc_wilcoxon(results_df_cv_long, group_col='Model', val_col='Prediction', p_adjust='holm')
        print("\nPost-hoc Wilcoxon test results :")
        output_data = []
        for inex, row in posthoc_results.iterrows():
            for col in posthoc_results.columns:
                if inex != col:
                    output_data.append({
                        'Classifier1': inex,
                        'Classifier2': col,
                        'Pvalue': row[col]
                    })
        output_df = pd.DataFrame(output_data)


        def format_float(x):
            if abs(x) < 0.0001:
                return f"{x:.2e}"  # Scientific notation for values less than 0.0001
            else:
                return f"{x:.4f}"  # Default formatting for other values


        print(output_df.to_latex(index=False, float_format=lambda x: format_float(x)))
