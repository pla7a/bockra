import os
import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.feature_extraction.text import CountVectorizer as CV
from collections import Counter
from sklearn.naive_bayes import BernoulliNB as BNB
from sklearn.model_selection import KFold as KF

# Load the dataset for training
def load_data():
    data_path = os.path.join(os.getcwd(), 'data/', 'sent140_train.csv')
    s140_train = pd.read_csv(data_path, delimiter = ',')
    # Rename the columns
    s140_train.columns = ["target", "id", "date", "flag", "user", "text"]
    return s140_train

# Return the CountVectorizer object
def count_init(s140_train):
    # Fit the corpus to the CountVectorizer (bag of words)
    eng_words = np.genfromtxt("data/corpus.txt", dtype="str")
    CVec = CV()
    CVec.fit(eng_words)
    return CVec

# Return the build analyzer function for CountVectorizer
def build_analyzer(CVec):
    return CVec.build_analyzer()

# Get a count vector of the given corpus
def count_corpus(CVec, s140_train):
    corpus = s140_train["text"].values
    return CVec.transform(corpus)

# Get the target classes
def get_classes(s140_train):
    classes = s140_train[["target"]]
    return classes.values

# Initialize Naive Bayes predictor
def naive_bayes(corpus_CV, classes):
    bnb = BNB()
    classes = np.ravel(classes)
    bnb.fit(corpus_CV, classes)
    return bnb

s140_train = load_data()
CVec = count_init(s140_train)
anly_CV = build_analyzer(CVec)
corpus_CV = count_corpus(CVec, s140_train)
classes_df = get_classes(s140_train)
bnb = naive_bayes(corpus_CV, classes_df)

