import numpy as np

def documents_to_xy(documents):
    X = []
    y = []
    for d in documents:
        X.append(d.text)
        y.append(d.label.id)

    return (X, y)