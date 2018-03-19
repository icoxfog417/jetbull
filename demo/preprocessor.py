from sklearn.preprocessing import LabelEncoder
from sklearn.base import BaseEstimator, TransformerMixin


class ColumnEncoder(LabelEncoder):

    def __init__(self, column):
        super().__init__()
        self.column = column

    def fit(self, X, y=None):
        series = X[self.column]
        return super().fit(series)

    def fit_transform(self, X, y=None):
        return self.fit(X, y).transform(X)

    def transform(self, X):
        series = X[self.column]
        converted = super().transform(series)
        X[self.column] = converted
        return X

    def inverse_transform(self, X):
        series = X[self.column]
        inversed = super().inverse_transform(series)
        X[self.column] = inversed
        return X


class DropColumn(BaseEstimator, TransformerMixin):

    def __init__(self, column):
        self.column = column

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        if self.column in X.columns:
            return X.drop(columns=[self.column])
        else:
            return X


class CategoricalToNumerical(BaseEstimator, TransformerMixin):

    def __init__(self, column, rule_dict):
        self.column = column
        self.rule_dict = rule_dict

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        def convert(x):
            if x in self.rule_dict:
                return self.rule_dict[x]
            else:
                return x

        if self.column in X.columns:
            X[self.column] = X[self.column].map(convert)
        return X

    def inverse_transform(self, X):
        inv = {v: k for k, v in self.rule_dict.items()}

        def convert(x):
            if x in inv:
                return inv[x]
            else:
                return x

        if self.column in X.columns:
            X[self.column] = X[self.column].map(convert)
        return X
