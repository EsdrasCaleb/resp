from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.utils.validation import check_X_y, check_array, check_is_fitted
import numpy as np

class WeightedKNeighborsClassifier(BaseEstimator, ClassifierMixin):
    def __init__(self, n_neighbors=5, **kwargs):
        self.n_neighbors = n_neighbors
        self.kwargs = kwargs
        self.scaler_ = StandardScaler()

    def fit(self, X, y, sample_weight=None):
        X, y = check_X_y(X, y)
        self.classes_ = np.unique(y)
        
        # Scale the features
        X = self.scaler_.fit_transform(X)
        
        if sample_weight is not None:
            self.sample_weight_ = np.sqrt(sample_weight)
            self.X_ = X * self.sample_weight_[:, np.newaxis]
            self.y_ = y
        else:
            self.X_ = X
            self.y_ = y
        
        self.knn_ = KNeighborsClassifier(n_neighbors=self.n_neighbors, **self.kwargs)
        self.knn_.fit(self.X_, self.y_)
        return self

    def predict(self, X):
        check_is_fitted(self)
        X = check_array(X)
        X = self.scaler_.transform(X)
        return self.knn_.predict(X)

    def predict_proba(self, X):
        check_is_fitted(self)
        X = check_array(X)
        X = self.scaler_.transform(X)
        return self.knn_.predict_proba(X)
