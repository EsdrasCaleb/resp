import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.metrics import classification_report, accuracy_score
from sklearn.ensemble import AdaBoostClassifier, BaggingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import StackingClassifier
from sklearn.preprocessing import LabelEncoder
from weigthknm import WeightedKNeighborsClassifier
from weigtedmpl import WeightedMLPClassifier



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
        scores = cross_val_score(model, X, y, cv=cv, scoring='accuracy')
        return scores.mean()
    else:
        test_size = split[0]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        return accuracy_score(y_test, y_pred)


kumites = [
    'Ada',
    'Bagging',
]

kumites = []

for datastring in ['checkpoint/data.csv','checkpoint/redusida2.csv']:
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
    kumites = []
    print("base "+datastring)
    y = label_encoder.fit_transform(y)
    for kumite in kumites:
        for max_features in max_features_list:
            if kumite != kumites[1] and max_features != 1:
                continue
            print(f'Tabela {kumite} com features {max_features}')
            for split in splits:
                print("estrategia de selecao,estrategia estimador, 10,20")
                for name, clf in base_classifiers.items():
                    result = [split[1],name]
                    for n_estimators in n_estimators_list:
                        # AdaBoostClassifier
                        if(kumite == kumites[1]):
                            bagging_model = BaggingClassifier(estimator=clf, n_estimators=n_estimators, max_features=max_features, random_state=42)
                            bagging_accuracy = evaluate_classifier(bagging_model, X, y, split)
                            result.append(str(bagging_accuracy))
                        else:
                            if(clf==base_knn):
                                clf = WeightedKNeighborsClassifier(random_state=42)
                            if(clf==base_mlp):
                                clf = WeightedMLPClassifier(random_state=42)
                            ada_model = AdaBoostClassifier(estimator=clf, n_estimators=n_estimators, random_state=42,algorithm='SAMME')
                            ada_accuracy = evaluate_classifier(ada_model, X, y, split)
                            result.append(str(ada_accuracy))
                        #print(f'AdaBoost with {name}, n_estimators={n_estimators}, max_features={max_features}, split={split[1]}')
                        #print(f'Accuracy: {ada_accuracy:.4f}')
                    
                    print(",".join(result), flush=True)
    
    print("Tabela Randon Florest", flush=True)
    n_estimators_list = [10, 100]
    criteria = ['gini', 'entropy', 'log_loss']
    print("estrategia de selecao,criterio, 10,20")
    criteria = []
    for criterion in criteria:
        for split in splits:
            result = [split[1],criterion]
            for n_estimators in n_estimators_list:
                model = RandomForestClassifier(n_estimators=n_estimators, criterion=criterion, random_state=42)
                accuracy = evaluate_classifier(model, X, y, split)
                result.append(str(accuracy))
            print(",".join(result), flush=True)
    print("Tabela Staking")
    print("estrategia de selecao,Classificdores, Acuracia")
    n_classifiers_list = [10, 20]
    n_classifiers_list = []
    for n_classifiers in n_classifiers_list:
        base_estimators = [(f'knn_{i}', base_knn) for i in range(n_classifiers // 2)] + \
                        [(f'mlp_{i}', base_mlp) for i in range(n_classifiers // 2, n_classifiers)]
        for split in splits:
            # Define the StackingClassifier
            stacking_model = StackingClassifier(estimators=base_estimators, final_estimator=MLPClassifier(max_iter=1000), cv=5)
            
            # Evaluate the model
            accuracy = evaluate_classifier(stacking_model, X, y, split)
            print(f'{split[1]}, {n_classifiers}, {accuracy}', flush=True)

    base_estimators = [(f'knn_{i}', base_knn) for i in range(1)] + \
                        [(f'mlp_{i}', base_mlp) for i in range(1)]+ \
                        [(f'ad_{i}', base_classifiers["AD"]) for i in range(1)]+ \
                        [(f'NB_{i}', base_classifiers["NB"]) for i in range(1)]
    stacking_model = StackingClassifier(estimators=base_estimators, final_estimator=MLPClassifier(hidden_layer_sizes= 111, learning_rate_init= 0.001, max_iter= 500, random_state= 9), cv=10)
            
    # Evaluate the model
    accuracy = evaluate_classifier(stacking_model, X, y, (0.3, '70/30'))
    print(f'Stacking com decision tree {accuracy}')