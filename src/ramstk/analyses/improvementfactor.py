# -*- coding: utf-8 -*-
#
#       ramstk.analyses.improvementfactor.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Stakeholder Improvement Factor Analysis Module."""

# Standard Library Imports
from typing import Dict, Tuple


def calculate_improvement(planned_rank: int, customer_rank: int, priority: int,
                          **kwargs: Dict[str, float]) -> Tuple[float, float]:
    """Calculate the stakeholder improvement factor and overall weighting.

    :param planned_rank: the rank the design team plans.
    :param customer_rank: the rank the customer places on the input.
    :param priority: the design team's priority.
    :return: (_improvement, _weight); the improvement factor and overall
        weighting of the stakeholder input.
    :rtype: tuple
    """
    _user_float_1 = kwargs.get('user_float_1', 1.0)
    _user_float_2 = kwargs.get('user_float_2', 1.0)
    _user_float_3 = kwargs.get('user_float_3', 1.0)
    _user_float_4 = kwargs.get('user_float_4', 1.0)
    _user_float_5 = kwargs.get('user_float_5', 1.0)

    _improvement = 1.0 + 0.2 * (planned_rank - customer_rank)
    _weight = (
        float(priority) * _improvement * _user_float_1  # type: ignore
        * _user_float_2 * _user_float_3 * _user_float_4  # type: ignore
        * _user_float_5  # type: ignore
    )

    return _improvement, _weight
