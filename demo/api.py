import os
import sys
import numpy as np
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from jetbull.api import API  # noqa
from jetbull.threshold_estimator import ThresholdEstimator  # noqa


api = API(ThresholdEstimator, [np.arange(0.3, 0.9, 0.1)])
