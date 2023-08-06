from sklearn.base import (
    BaseEstimator,
    TransformerMixin
)
from sklearn import (
    pipeline,
    impute
)
import lightgbm


class FeatureTransformer(TransformerMixin, BaseEstimator):
    def __init__(self, is_cl, min_child_samples=100):
        self.is_cl = is_cl
        self.min_child_samples = min_child_samples

    def fit(self, X, y):
        self.feature_models = {
            i: _train_monotonic_tree(X[:, [i]], y, self.is_cl, self.min_child_samples)
            for i in range(X.shape[1])
        }

    def transform(self, X):
        return numpy.concatenate(
            [
                self.transform_each_features(X, i)
                for i in self.feature_models.keys()
            ]
        )

    def transform_each_features(self, X, i):
        return numpy.concatenate(
            [
                model.predict(X[:, [i]])
                for model in self.feature_models[i]
            ], axis=1
        )


def _train_monotonic_tree(x, y, is_cl, min_child_samples):
    increasing_model = _get_pipeline(is_cl, True, min_child_samples)
    decreasing_model = _get_pipeline(is_cl, False, min_child_samples)
    increasing_model.fit(x, y)
    decreasing_model.fit(x, y)
    models = [AsIsFeature(), increasing_model, decreasing_model]
    return _select_features(x, y, models)


def _get_pipeline(is_cl, is_increasing, min_child_samples):
    model = lightgbm.LGBMClassifier if is_cl else lightgbm.LGBMRegressor
    monotone_c = 1 if is_increasing else -1
    lgbm = model(monotone_constraints=monotone_c, min_child_samples=min_child_samples)
    return pipeline.Pipeline(
        steps=[
            ("mvi", impute.SimpleImputer()),
            ("tree", lgbm)
        ]
    )


def _select_features(x, y, models):
    features = numpy.concatenate(
        [
            models[i].predict(x)
            for i in range(len(models))
        ], axis=1
    )
    abs_corr = [abs(numpy.corrcoef(x[:, i], y))[0, 1] for i in range(len(models))]
    if abs_corr[0] > abs_corr[1] and abs_corr[0] > abs_corr[2]:
        return [models[0]]
    else:
        return [models[i] for i in range(1, len(models)) if abs_corr[i] > abs_corr[0]]


class AsIsFeature(object):
    def predict(x):
        return x[:, 0]
