# -*- coding: utf-8 -*-
#
#       ramstk.analyses.prediction.Lamp.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Lamp MIL-HDBK-217F Calculations Module."""

# Standard Library Imports
from typing import Any, Dict

PART_COUNT_LAMBDA_B = {
    1: [
        3.9, 7.8, 12.0, 12.0, 16.0, 16.0, 16.0, 19.0, 23.0, 19.0, 2.7, 16.0,
        23.0, 100.0
    ],
    2: [
        13.0, 26.0, 38.0, 38.0, 51.0, 51.0, 51.0, 64.0, 77.0, 64.0, 9.0, 51.0,
        77.0, 350.0
    ]
}
PI_E = [1.0, 2.0, 3.0, 3.0, 4.0, 4.0, 4.0, 5.0, 6.0, 5.0, 0.7, 4.0, 6.0, 27.0]


def calculate_part_count(**attributes: Dict[str, Any]) -> float:
    """Wrap get_part_count_lambda_b().

    This wrapper allows us to pass an attributes dict from a generic parts
    count function.

    :param attributes: the attributes for the connection being calculated.
    :return: _base_hr; the parts count base hazard rates.
    :rtype: float
    """
    return get_part_count_lambda_b(
        attributes['application_id'],  # type: ignore
        attributes['environment_active_id'])  # type: ignore


def calculate_part_stress(**attributes: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate the part stress hazard rate for a lamp.

    This function calculates the MIL-HDBK-217F hazard rate using the part
    stress method.

    :return: attributes; the keyword argument (hardware attribute)
             dictionary with updated values.
    :rtype: dict
    """
    attributes[
        'lambda_b'] = 0.074 * attributes['voltage_rated']**1.29  # type: ignore

    # Determine the utilization factor (piU).
    if attributes['duty_cycle'] < 10.0:  # type: ignore
        attributes['piU'] = 0.1  # type: ignore
    elif 10.0 <= attributes['duty_cycle'] < 90.0:  # type: ignore
        attributes['piU'] = 0.72  # type: ignore
    else:
        attributes['piU'] = 1.0  # type: ignore

    # Determine the application factor (piA).
    attributes['piA'] = (
        3.3 if (attributes['application_id']) -  # type: ignore
        (1) else 1.0)

    attributes['hazard_rate_active'] = (
        attributes['lambda_b']  # type: ignore
        * attributes['piU'] * attributes['piA'] * attributes['piE'])

    return attributes


def get_part_count_lambda_b(application_id: int,
                            environment_active_id: int) -> float:
    """Retrieve the part count hazard rate for a lamp.

    This function calculates the MIL-HDBK-217F hazard rate using the parts
    count method.

    :param application_id: the lamp application identifier.
    :param environment_active_id: the operating environment identifier.
    :return: _base_hr; the base part count hazard rate.
    :rtype: float
    :raise: IndexError if passed an unknown active environment ID.
    :raise: KeyError if passed an unknown application ID.
    """
    return PART_COUNT_LAMBDA_B[application_id][environment_active_id - 1]
