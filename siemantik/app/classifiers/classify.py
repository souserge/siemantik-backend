from siemantik.app.classifiers.utils import proba_to_classes, text_to_lemmas, predictions_to_classes


def classify(estimator, documents):
    X = [text_to_lemmas(x.text) for x in documents]

    try: 
        proba = estimator.predict_proba(X)
        return proba_to_classes(estimator.classes_, proba, documents)
    except:
        preds = estimator.predict(X)
        return predictions_to_classes(preds, documents)