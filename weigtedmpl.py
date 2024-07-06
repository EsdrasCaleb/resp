from sklearn.neural_network import MLPClassifier
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.utils.validation import check_X_y, check_array, check_is_fitted
import numpy as np

class WeightedMLPClassifier(BaseEstimator, ClassifierMixin):
    def __init__(self, hidden_layer_sizes=(100,), activation='relu', solver='adam', alpha=0.0001,
                 batch_size='auto', learning_rate='constant', learning_rate_init=0.001, power_t=0.5,
                 max_iter=200, shuffle=True, random_state=None, tol=1e-4, verbose=False,
                 warm_start=False, momentum=0.9, nesterovs_momentum=True, early_stopping=False,
                 validation_fraction=0.1, beta_1=0.9, beta_2=0.999, epsilon=1e-8,
                 n_iter_no_change=10, max_fun=15000):
        self.hidden_layer_sizes = hidden_layer_sizes
        self.activation = activation
        self.solver = solver
        self.alpha = alpha
        self.batch_size = batch_size
        self.learning_rate = learning_rate
        self.learning_rate_init = learning_rate_init
        self.power_t = power_t
        self.max_iter = max_iter
        self.shuffle = shuffle
        self.random_state = random_state
        self.tol = tol
        self.verbose = verbose
        self.warm_start = warm_start
        self.momentum = momentum
        self.nesterovs_momentum = nesterovs_momentum
        self.early_stopping = early_stopping
        self.validation_fraction = validation_fraction
        self.beta_1 = beta_1
        self.beta_2 = beta_2
        self.epsilon = epsilon
        self.n_iter_no_change = n_iter_no_change
        self.max_fun = max_fun
        self.mlp = MLPClassifier(hidden_layer_sizes=self.hidden_layer_sizes,
                            activation=self.activation, solver=self.solver,
                            alpha=self.alpha, batch_size=self.batch_size,
                            learning_rate=self.learning_rate, learning_rate_init=self.learning_rate_init,
                            power_t=self.power_t, max_iter=self.max_iter, shuffle=self.shuffle,
                            random_state=self.random_state, tol=self.tol, verbose=self.verbose,
                            warm_start=self.warm_start, momentum=self.momentum,
                            nesterovs_momentum=self.nesterovs_momentum, early_stopping=self.early_stopping,
                            validation_fraction=self.validation_fraction, beta_1=self.beta_1,
                            beta_2=self.beta_2, epsilon=self.epsilon, n_iter_no_change=self.n_iter_no_change,
                            max_fun=self.max_fun)

    def fit(self, X, y, sample_weight=None):
        X, y = check_X_y(X, y, accept_sparse=['csr', 'csc', 'coo'])
        self.classes_ = np.unique(y)
        if sample_weight is not None:
            sample_weight = np.array(sample_weight)
            sample_weight /= np.sum(sample_weight)  # Normalize weights
            X_weighted = np.repeat(X, np.ceil(sample_weight * len(y)).astype(int), axis=0)
            y_weighted = np.repeat(y, np.ceil(sample_weight * len(y)).astype(int))
        else:
            X_weighted, y_weighted = X, y
        
        self.mlp.fit(X_weighted, y_weighted)
        return self

    def predict(self, X):
        check_is_fitted(self.mlp)
        X = check_array(X, accept_sparse=['csr', 'csc', 'coo'])
        return self.mlp.predict(X)

    def predict_proba(self, X):
        check_is_fitted(self.mlp)
        X = check_array(X, accept_sparse=['csr', 'csc', 'coo'])
        return self.mlp.predict_proba(X)
