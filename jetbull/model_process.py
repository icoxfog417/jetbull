from enum import Enum
from sklearn.base import RegressorMixin, ClassifierMixin
from sklearn.pipeline import Pipeline
from sklearn.pipeline import _fit_transform_one
from sklearn.utils.validation import check_memory
from sklearn.utils.metaestimators import if_delegate_has_method
from sklearn.base import clone
from jetbull.jet_model import JetModel
from jetbull.threshold_estimator import ThresholdEstimator


class ProcKind(Enum):
    PROCESS = 0
    MODEL = 1


class ModelProcess(Pipeline):

    def __init__(self, steps, memory=None):
        super().__init__(steps, memory)
        self.steps = steps
        self._validate_steps()
        self.memory = memory

    def get_procs(self, unit_kind, with_name=False):
        results = []
        kind = None
        for n, e in self.steps:
            if isinstance(e, (ClassifierMixin, RegressorMixin)):
                kind = ProcKind.MODEL
            elif isinstance(e, JetModel):
                kind = ProcKind.MODEL
            elif isinstance(e, ThresholdEstimator):
                kind = ProcKind.THRESHOLD
            elif unit_kind == ProcKind.PROCESS:
                kind = ProcKind.PROCESS

            if kind == unit_kind:
                if with_name:
                    results.append((n, e))
                else:
                    results.append(e)
        return results

    def _validate_steps(self):
        names, estimators = zip(*self.steps)

        # validate names
        self._validate_names(names)

        # validate estimators
        transformers = self.get_procs(ProcKind.PROCESS)
        estimator = self.get_procs(ProcKind.MODEL)[0]

        for t in transformers:
            if t is None:
                continue
            if (not (hasattr(t, "fit") or hasattr(t, "fit_transform")) or not
                    hasattr(t, "transform")):
                raise TypeError("All intermediate steps should be "
                                "transformers and implement fit and transform."
                                " '%s' (type %s) doesn't" % (t, type(t)))

        # We allow last estimator to be None as an identity transformation
        if estimator is not None and not hasattr(estimator, "fit"):
            raise TypeError("Last step of Pipeline should implement fit. "
                            "'%s' (type %s) doesn't"
                            % (estimator, type(estimator)))

    @property
    def _estimator_type(self):
        model = self.get_procs(ProcKind.MODEL)[0]
        return model._estimator_type

    @property
    def _final_estimator(self):
        model = self.get_procs(ProcKind.MODEL)[0]
        return model

    def _fit_local(self, X, y=None, **fit_params):
        # shallow copy of steps - this should really be steps_
        self.steps = list(self.steps)
        self._validate_steps()
        # Setup the memory
        memory = check_memory(self.memory)

        fit_transform_one_cached = memory.cache(_fit_transform_one)

        fit_params_steps = dict((name, {}) for name, step in self.steps
                                if step is not None)
        for pname, pval in fit_params.items():
            step, param = pname.split('__', 1)
            fit_params_steps[step][param] = pval
        Xt = X
        transformers = self.get_procs(ProcKind.PROCESS, with_name=True)
        for step_idx, (name, transformer) in enumerate(transformers):
            if transformer is None:
                pass
            else:
                if hasattr(memory, "cachedir") and memory.cachedir is None:
                    cloned_transformer = transformer
                else:
                    cloned_transformer = clone(transformer)

                Xt, fitted_transformer = fit_transform_one_cached(
                    cloned_transformer, None, Xt, y,
                    **fit_params_steps[name])
                self.steps[step_idx] = (name, fitted_transformer)
        if self._final_estimator is None:
            return Xt, {}
        name_estimator = self.get_procs(ProcKind.MODEL, with_name=True)[0]
        return Xt, fit_params_steps[name_estimator[0]]

    def fit_cloud(self, X, **fit_params):
        raise Exception("Have to implements")

    def train(self, X, y=None, on_cloud=False, **fit_params):
        if not on_cloud:
            self.fit(X, y, **fit_params)
        else:
            self._fit_cloud(X, **fit_params)

    @if_delegate_has_method(delegate="_final_estimator")
    def predict(self, X, **predict_params):
        Xt = X
        for transform in self.get_procs(ProcKind.PROCESS):
            if transform is not None:
                Xt = transform.transform(Xt)
        model = self.get_procs(ProcKind.MODEL)[0]
        return model.predict(Xt, **predict_params)

    @if_delegate_has_method(delegate="_final_estimator")
    def fit_predict(self, X, y=None, **fit_params):
        Xt, fit_params = self._fit(X, y, **fit_params)
        model = self.get_procs(ProcKind.MODEL)[0]
        return model.fit_predict(Xt, y, **fit_params)

    @if_delegate_has_method(delegate="_final_estimator")
    def predict_proba(self, X):
        Xt = X
        for transform in self.get_procs(ProcKind.PROCESS):
            if transform is not None:
                Xt = transform.transform(Xt)
        model = self.get_procs(ProcKind.MODEL)[0]
        return model.predict_proba(Xt)

    def transform_data(self, X):
        Xt = X
        for transformer in self.get_procs(ProcKind.PROCESS):
            if transformer is not None:
                Xt = transformer.transform(Xt)
        return Xt
