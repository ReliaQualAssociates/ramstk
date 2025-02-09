# type: ignore
# -*- coding: utf-8 -*-
#
#       ramstk.analyses.milhdbk217f.models.fuse.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Fuse MIL-HDBK-217F Calculations Module."""

# Standard Library Imports
from typing import Dict, Union

# RAMSTK Package Imports
from ramstk.constants.fuse import PART_COUNT_LAMBDA_B, PI_E


def calculate_part_stress(
    attributes: Dict[str, Union[float, int, str]]
) -> Dict[str, Union[float, int, str]]:
    """Calculate the part stress hazard rate for a fuse.

    This function calculates the MIL-HDBK-217F hazard rate using the part stress method.

    :param attributes: the attributes for the capacitor being calculated.
    :return: attributes; the keyword argument (hardware attribute) dictionary with
        updated values.
    :rtype: dict
    """
    attributes["hazard_rate_active"] *= attributes["piE"]

    return attributes


def get_environment_factor(attributes: Dict[str, Union[float, int, str]]) -> float:
    """Retrieve the environment factor (piE) for the passed environment ID.

    :param attributes: the attributes for the capacitor being calculated.
    :return: the environment factor.
    :rtype: float
    :raises: IndexError when passed an invalid active environment ID.
    """
    _environment_id = attributes["environment_active_id"]

    try:
        return PI_E[_environment_id - 1]
    except IndexError:
        raise IndexError(
            f"get_environment_factor: Invalid fuse environment ID {_environment_id}."
        )


def get_part_count_lambda_b(attributes: Dict[str, Union[float, int, str]]) -> float:
    """Retrieve the part count base hazard rate.

    :param attributes: the attributes for the capacitor being calculated.
    :return: the part count base hazard rate.
    :rtype: float
    :raises: IndexError when passed an invalid active environment ID.
    """
    _environment_id = attributes["environment_active_id"]

    try:
        return PART_COUNT_LAMBDA_B[_environment_id - 1]
    except IndexError:
        raise IndexError(
            f"get_part_count_lambda_b: Invalid fuse environment ID {_environment_id}."
        )


def get_part_stress_lambda_b(attributes: Dict[str, Union[float, int, str]]) -> float:
    """Retrieve the part stress base hazard rate.

    :param attributes: the attributes for the capacitor being calculated.
    :return: the part count base hazard rate.
    :rtype: float
    """
    return 0.010


def set_default_values(
    attributes: Dict[str, Union[float, int, str]],
) -> Dict[str, Union[float, int, str]]:
    """Set the default value of various fuse parameters.

    :param attributes: the attribute dict for the electronic filter being calculated.
    :return: attributes; the updated attribute dict.
    :rtype: dict
    """
    if attributes["lambda_b"] <= 0.0:
        attributes["lambda_b"] = 0.01

    return attributes
