class CurveLinearClassifier(object):
    def __init__(self, min_child_samples, penalty, C):
        self.min_child_samples = min_child_samples
        self.penalty = penalty
        self.C = C
        self.feature_transformer = feature_transformer.FeatureTransformer()
        self.linear_model = linear_model.LogisticRegression(penalty=self.penalty, C=self.C)

    def fit(self, X, y):
        self.feature_transformer.fit(X, y)
        newX = self.feature_transformer.transform(X)
        self.linear_model.fit(newX, y)
