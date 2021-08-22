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
from ML_Util import ML_Util
import pickle

class sentiment_analysis():

    obj_util = util_handler()
    obj_query = query_handler()
    obj_ml_util = ML_Util()

    def get_review_data(self):     
        query = self.obj_query.get_all()
        rows = self.obj_util.execute(query,False)
        result = self.obj_util.convert_data_to_json(rows)
        return pd.DataFrame(result)

    def insert_model_stats(self, accuracy):
        query = self.obj_query.insert_model_stat("CLASS_LG","LogisticRegression","Classification",accuracy)
        self.obj_util.execute(query,True)

    def process_review_train(self):
        data_set =  self.get_review_data()
        data_set = self.obj_ml_util.remove_special_char(data_set)
        data_set['SENTIMENT'] = self.obj_ml_util.label_encoder(data_set['SENTIMENT'])
        X_train, X_test, y_train, y_test = self.obj_ml_util.train_test_split(data_set['REVIEW'], data_set['SENTIMENT'], 0.2, 2)
        vectorized = self.obj_ml_util.vectorize_X(X_train)
        self.obj_ml_util.publish_model(vectorized, "vectorized.pkl")
        X_train_vectorized = self.obj_ml_util.transform(vectorized, X_train)
        model = self.obj_ml_util.train_model(LogisticRegression(solver='lbfgs',max_iter=5000), X_train_vectorized,y_train)
        X_test_vectorized = self.obj_ml_util.transform(vectorized, X_test)
        score = self.obj_ml_util.evaluate_classification(model, X_test_vectorized, y_test)
        self.insert_model_stats(score)
        self.obj_ml_util.publish_model(model, "classification.pkl")

    def predict_classification(self, review):
        model = self.obj_ml_util.load_model("classification.pkl")
        vectorized = self.obj_ml_util.load_model("vectorized.pkl")
        review_vectorized = self.obj_ml_util.transform(vectorized, [review])
        result = model.predict(review_vectorized)
        if result == 1:
            return "Positive"

        return "Negative"   