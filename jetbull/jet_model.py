class JetModel():

    def __init__(self):
        # Marker Interface to distinguish the model
        pass

    def fit(self, X, y=None, **fit_params):
        if y is None:
            return self.fit(X, **fit_params)
        else:
            return self.fit(X, y, **fit_params)