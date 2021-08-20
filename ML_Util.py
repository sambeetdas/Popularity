from math import pi
import re
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV, RandomizedSearchCV
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn import preprocessing
from query_handler import query_handler
from util_handler import util_handler
import pickle


class ML_Util(object):

    def remove_special_char(self, data_set):   
        data_set.replace('[^a-zA-Z0-9 \n\.]', '',regex=True,inplace=True)
        data_set= data_set.applymap(lambda s:s.lower() if type(s) == str else s)
        return data_set

    def label_encoder(self, data_column):
        label_encoder = preprocessing.LabelEncoder()
        data_column = label_encoder.fit_transform(data_column)
        return data_column    

    def vectorize_X(self, X):
        vectorized = CountVectorizer(min_df=5, ngram_range=(1,2)).fit(X)        
        return vectorized

    def transform(self, vectorized, X):
        X_train_vectorized = vectorized.transform(X)
        return X_train_vectorized    

    def train_test_split(self, X, y, test_size_perc, random_state):
        return train_test_split(X, y, test_size = test_size_perc, stratify = y, random_state = random_state)


    def publish_model(self, model, model_name):
        pickle.dump(model, open(model_name,'wb'))

    def load_model(self, model_name):
        model = pickle.load(open(model_name,'rb'))
        return model

    def train_model(self,alg, X, y):
        model = alg.fit(X, y)
        return model

    def evaluate_classification(self, model, X, y_test):
        X_test_prediction = model.predict(X)
        test_data_accuracy = accuracy_score(X_test_prediction, y_test)
        return test_data_accuracy    
