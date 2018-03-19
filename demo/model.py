from sklearn.ensemble import RandomForestClassifier


model = RandomForestClassifier(n_estimators=50, oob_score=True)