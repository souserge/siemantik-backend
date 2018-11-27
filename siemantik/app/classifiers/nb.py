import pickle as pkl
from time import time
from scipy.stats import randint, uniform, expon

from .utils import documents_to_xy

from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import RandomizedSearchCV


def train(documents):
    X_train, y_train = documents_to_xy(documents)

    tfidf = TfidfVectorizer()
    nb = MultinomialNB()
    pipeline = Pipeline([
        ('tfidf', tfidf),
        ('nb', nb),
    ])

    parameters = {
        'tfidf__max_df': uniform(0.5,0.5), # Filter most popular words (acts as stoplist)
        'tfidf__max_features': randint(1000, 10000), # limit number of features
        'tfidf__ngram_range': [(1, 1), (1, 2)], # unigrams or bigrams
        'tfidf__use_idf': [True, False], # use tf-idf or bag of words
    }

    random_search = RandomizedSearchCV(pipeline, param_distributions=parameters,
                                   n_iter=100, n_jobs=-1, verbose=1)

    random_search.fit(X_train, y_train)

    return (random_search.best_estimator_, random_search.best_score_)


def classify(estimator, documents):
    X = [x.text for x in documents]
    print(estimator.classes_)
    return estimator.predict_proba(X)