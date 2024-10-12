# -*- coding: utf-8 -*-
#
#       ramstk.analyses.improvementfactor.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Stakeholder Improvement Factor Analysis Module."""
# Standard Library Imports
import math
from typing import Any, Dict, List, Tuple


def calculate_improvement(
    planned_rank: int,
    customer_rank: int,
    priority: int,
    **kwargs: Dict[str, Any],
) -> Tuple[float, float]:
    """Calculate the stakeholder improvement factor and overall weighting.

    :param planned_rank: the rank the design team plans.
    :param customer_rank: the rank the customer places on the input.
    :param priority: the design team's priority.
    :return: (_improvement, _weight); the improvement factor and overall weighting of
        the stakeholder input.
    :rtype: tuple
    """
    # Input validation for ranks and priority
    if not isinstance(planned_rank, int) or planned_rank < 0:
        raise ValueError("planned_rank must be a non-negative integer.")
    if not isinstance(customer_rank, int) or customer_rank < 0:
        raise ValueError("customer_rank must be a non-negative integer.")
    if not isinstance(priority, (int, float)) or priority <= 0:
        raise ValueError("priority must be a positive number.")

    # Collect user floats dynamically from kwargs and validate them
    _user_floats: List[float] = []
    for key, value in kwargs.items():
        if key.startswith("user_float_"):
            if not isinstance(value, (int, float)):
                raise ValueError(f"{key} must be a number, got {type(value)}")
            _user_floats.append(float(value))

    # Use default user_float value of 1.0 if no user floats were provided
    if not _user_floats:
        _user_floats.append(1.0)

    # Validate that user-provided floats are non-negative
    if any(_value <= 0 for _value in _user_floats):
        raise ValueError("All user_float_X values must be positive numbers.")

    _improvement = 1.0 + 0.2 * (planned_rank - customer_rank)
    _weight = float(priority) * _improvement * math.prod(_user_floats)

    return _improvement, _weight
