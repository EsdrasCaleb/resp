import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score, KFold
from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np


from db_paper import db_paper
import csv
import os.path
import time

original_database = pd.read_csv('checkpoint/data.csv')
df_lessattr = pd.read_csv('checkpoint/redusida2.csv')