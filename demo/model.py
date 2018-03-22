from sklearn.ensemble import RandomForestClassifier


def make_model(n_estimators):
    return RandomForestClassifier(n_estimators=n_estimators, oob_score=True)
