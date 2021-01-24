# Standard Library Imports
from typing import Any, Callable, List, Tuple

# Third Party Imports
import numpy as np

def calculate_variance_covariance(n_failures: Any, max_time: Any, alpha: Any,
                                  beta: Any):
    ...


def calculate_nhpp_mean_variance(n_failures: Any,
                                 max_time: Any,
                                 alpha: Any,
                                 beta: Any,
                                 metric: int = ...):
    ...


def calculate_fisher_bounds(metric: Any, variance: Any, alpha: Any):
    ...


def calculate_crow_bounds(n_failures: Any,
                          t_star: Any,
                          _lambda: Any,
                          beta: Any,
                          alpha: Any,
                          metric: Any,
                          data: int = ...):
    ...


def do_calculate_beta_bounds(
        minimum: float, likely: float, maximum: float,
        alpha: float) -> Tuple[float, float, float, float]:
    ...


def do_calculate_fisher_information(model: Callable,
                                    p0: List[float],
                                    X: np.ndarray,
                                    noise: Any = ...) -> np.ndarray:
    ...
