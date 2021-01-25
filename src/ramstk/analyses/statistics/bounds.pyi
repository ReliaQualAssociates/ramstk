# Standard Library Imports
from typing import Any, Callable, List, Tuple

# Third Party Imports
import numpy as np

def do_calculate_beta_bounds(
        minimum: float, likely: float, maximum: float,
        alpha: float) -> Tuple[float, float, float, float]:
    ...


def do_calculate_fisher_information(model: Callable,
                                    p0: List[float],
                                    data: np.ndarray,
                                    noise: Any = ...) -> np.ndarray:
    ...
