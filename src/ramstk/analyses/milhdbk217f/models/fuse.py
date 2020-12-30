# -*- coding: utf-8 -*-
#
#       ramstk.analyses.prediction.Fuse.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Fuse MIL-HDBK-217F Constants and Calculations Module."""

# Standard Library Imports
from typing import Any, Dict

PART_COUNT_LAMBDA_B = [
    0.01, 0.02, 0.06, 0.05, 0.11, 0.09, 0.12, 0.15, 0.18, 0.18, 0.009, 0.1,
    0.21, 2.3
]
PI_E = [
    1.0, 2.0, 8.0, 5.0, 11.0, 9.0, 12.0, 15.0, 18.0, 16.0, 0.9, 10.0, 21.0,
    230.0
]


def calculate_part_count(**attributes: Dict[str, Any]) -> float:
    """Wrap get_part_count_lambda_b().

    This wrapper allows us to pass an attributes dict from a generic parts
    count function.

    :param attributes: the attributes for the fuse being calculated.
    :return: _base_hr; the parts count base hazard rates.
    :rtype: float
    """
    return get_part_count_lambda_b(
        attributes['environment_active_id'])  # type: ignore


def calculate_part_stress(**attributes: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate the part stress hazard rate for a fuse.

    This function calculates the MIL-HDBK-217F hazard rate using the part
    stress method.

    :return: attributes; the keyword argument (hardware attribute) dictionary
        with updated values.
    :rtype: dict
    """
    attributes['hazard_rate_active'] = (
        0.010 * attributes['piE']  # type: ignore
    )

    return attributes


def get_part_count_lambda_b(environment_active_id: int) -> float:
    """Retrieve the part count hazard rate for a fuse.

    :param environment_active_id: the active environment identifer.
    :return: _base_hr; the part count base hazard rate.
    :rtype: float
    :raise: IndexError when passed an unkown active environment ID.
    """
    return PART_COUNT_LAMBDA_B[environment_active_id - 1]
