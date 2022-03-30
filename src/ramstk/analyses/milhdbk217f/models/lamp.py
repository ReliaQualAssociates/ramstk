# type: ignore
# -*- coding: utf-8 -*-
#
#       ramstk.analyses.milhdbk217f.models.lamp.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Lamp MIL-HDBK-217F Calculations Module."""

# Standard Library Imports
from typing import Dict, Union

PART_COUNT_LAMBDA_B = {
    1: [
        3.9,
        7.8,
        12.0,
        12.0,
        16.0,
        16.0,
        16.0,
        19.0,
        23.0,
        19.0,
        2.7,
        16.0,
        23.0,
        100.0,
    ],
    2: [
        13.0,
        26.0,
        38.0,
        38.0,
        51.0,
        51.0,
        51.0,
        64.0,
        77.0,
        64.0,
        9.0,
        51.0,
        77.0,
        350.0,
    ],
}
PI_E = [1.0, 2.0, 3.0, 3.0, 4.0, 4.0, 4.0, 5.0, 6.0, 5.0, 0.7, 4.0, 6.0, 27.0]


def calculate_part_count(**attributes: Dict[str, Union[float, int, str]]) -> float:
    """Wrap get_part_count_lambda_b().

    This wrapper allows us to pass an attribute dict from a generic parts
    count function.

    :param attributes: the attributes for the connection being calculated.
    :return: _base_hr; the parts count base hazard rates.
    :rtype: float
    """
    return get_part_count_lambda_b(
        attributes["application_id"],
        attributes["environment_active_id"],
    )


def calculate_part_stress(
    **attributes: Dict[str, Union[float, int, str]]
) -> Dict[str, Union[float, int, str]]:
    """Calculate the part stress hazard rate for a lamp.

    This function calculates the MIL-HDBK-217F hazard rate using the part
    stress method.

    :param attributes: the attribute dict for the lamp being calculated.
    :return: attributes; the keyword argument (hardware attribute)dictionary with
        updated values.
    :rtype: dict
    """
    attributes["lambda_b"] = 0.074 * attributes["voltage_rated"] ** 1.29

    # Determine the utilization factor (piU).
    if attributes["duty_cycle"] < 10.0:
        attributes["piU"] = 0.1
    elif 10.0 <= attributes["duty_cycle"] < 90.0:
        attributes["piU"] = 0.72
    else:
        attributes["piU"] = 1.0

    # Determine the application factor (piA).
    attributes["piA"] = 3.3 if attributes["application_id"] - 1 else 1.0

    attributes["hazard_rate_active"] = (
        attributes["lambda_b"]
        * attributes["piU"]
        * attributes["piA"]
        * attributes["piE"]
    )

    return attributes


def get_part_count_lambda_b(
    application_id: int,
    environment_active_id: int,
) -> float:
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


def set_default_values(
    **attributes: Dict[str, Union[float, int, str]],
) -> Dict[str, Union[float, int, str]]:
    """Set the default value of various parameters.

    :param attributes: the attribute dict for the lamp being calculated.
    :return: attributes; the updated attribute dict.
    :rtype: dict
    """
    if attributes["rated_voltage"] <= 0.0:
        attributes["rated_voltage"] = 28.0

    if attributes["duty_cycle"] <= 0.0:
        attributes["duty_cycle"] = 50.0

    return attributes
