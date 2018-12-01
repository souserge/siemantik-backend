import numpy as np
from pymystem3 import Mystem

mystems = list(map(
    lambda i: { 'id': i, 'mystem': Mystem(), 'in_use': False },
    range(3)
))

def get_mystem():
    for mys in mystems:
        if not mys['in_use']:
            return mys['mystem']
    else:
        new_mys = Mystem()
        return new_mys


def documents_to_xy(documents):
    X = []
    y = []
    for d in documents:
        X.append(d.text)
        y.append(d.label.id)

    return (X, y)


def text_to_lemmas(text):
    mystem = get_mystem()
    lemmas = mystem.lemmatize(text)
    lemmas_no_spaces = list(
        filter(
            lambda x: len(x) != 0,
            map(lambda x: x.strip(), lemmas)
        )
    )
    return ' '.join(lemmas_no_spaces)


def doc_info(_id, label, prob):
    return {
        'id': _id,
        'label': label,
        'prob': prob
    }


def proba_to_classes(classes, proba, docs):
    label_idxs = map(lambda probs: np.argmax(np.array(probs)), proba)
    return list(map(
        lambda probs, idx, doc: 
            doc_info(doc.id, classes[idx], probs[idx]),
        proba, label_idxs, docs 
    ))


def predictions_to_classes(preds, docs):
    return list(map(
        lambda pred, doc:
            doc_info(doc.id, pred, None),
        preds, docs
    ))