import pickle as pkl
from time import time
from scipy.stats import randint, uniform, expon
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import RandomizedSearchCV

from siemantik.app.classifiers.utils import documents_to_xy, proba_to_classes, text_to_lemmas

def nb():
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
    return (pipeline, parameters)

def svm():
    tfidf = TfidfVectorizer()
    clf = SGDClassifier(tol=1e-3)
    pipeline = Pipeline([
        ('tfidf', tfidf),
        ('clf', clf),
    ])

    parameters = {
        'tfidf__max_df': (0.5, 0.75, 1.0),
        'tfidf__max_features': (None, 5000, 10000, 50000),
        'tfidf__ngram_range': ((1, 1), (1, 2)),  # unigrams or bigrams
        'tfidf__use_idf': (True, False),
        'tfidf__norm': ('l1', 'l2'),
        'clf__alpha': (0.00001, 0.000001),
        'clf__penalty': ('l2', 'elasticnet'),
        'clf__max_iter': (10, 50, 80),
    }

    return pipeline, parameters

def mlp():
    return nb()


def classifier(type):
    alg_funs = {
        'nb': nb,
        'svm': svm,
        'mlp': mlp
    }
    return alg_funs.get(type, nb)()


def train(alg, documents):
    X_train_raw, y_train = documents_to_xy(documents)
    X_train = [text_to_lemmas(x) for x in X_train_raw]

    pipeline, parameters = classifier(alg)

    random_search = RandomizedSearchCV(
        pipeline, param_distributions=parameters,
        n_iter=100, n_jobs=-1, verbose=1
    )

    random_search.fit(X_train, y_train)

    estimator = random_search.best_estimator_

    results = {
        'accuracy': random_search.best_score_
    }

    return (estimator, results)