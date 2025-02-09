# type: ignore
# -*- coding: utf-8 -*-
#
#       ramstk.analyses.milhdbk217f.models.efilter.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Filter MIL-HDBK-217F Constants and Calculations Module."""

# Standard Library Imports
from typing import Dict, Union

# RAMSTK Package Imports
from ramstk.constants.efilter import (
    PART_COUNT_LAMBDA_B,
    PART_STRESS_LAMBDA_B,
    PI_E,
    PI_Q,
)


def calculate_part_stress(
    attributes: Dict[str, Union[float, int, str]]
) -> Dict[str, Union[float, int, str]]:
    """Calculate the part stress active hazard rate for a filter.

    :param attributes: the attributes for the filter being calculated.
    :return: attributes; the keyword argument (hardware attribute) dictionary with
        updated values.
    :rtype: dict
    """
    try:
        attributes["hazard_rate_active"] = (
            attributes["hazard_rate_active"] * attributes["piQ"] * attributes["piE"]
        )

        return attributes
    except KeyError as err:
        raise KeyError(
            f"calculate_part_stress: Missing required electronic filter attribute:"
            f" {err}."
        )


def get_environment_factor(attributes: Dict[str, Union[float, int, str]]) -> float:
    """Retrieve the electronic filter environment factor (piE).

    :param attributes: the attributes for the filter being calculated.
    :return: the environment factor for the selected environment ID.
    :rtype: float
    :raises: IndexError if passed an invalid environment ID.
    """
    _environment_id = attributes["environment_active_id"]

    try:
        return PI_E[_environment_id - 1]
    except IndexError:
        raise IndexError(
            f"get_environment_factor: Invalid electronic filter environment "
            f"ID {_environment_id}."
        )


def get_quality_factor(attributes: Dict[str, Union[float, int, str]]) -> float:
    """Retrieve the electronic filter quality factor (piQ).

    :param attributes: the attributes for the filter being calculated.
    :return: the quality factor for the selected quality ID.
    :rtype: float
    :raises: IndexError if passed an invalid quality ID.
    """
    _quality_id = attributes["quality_id"]

    try:
        return PI_Q[_quality_id - 1]
    except IndexError:
        raise IndexError(
            f"get_quality_factor: Invalid electronic filter quality ID {_quality_id}."
        )


def get_part_count_lambda_b(attributes: Dict[str, Union[float, int, str]]) -> float:
    """Retrieve the part count base hazard rate for a filter.

    :param attributes: the attributes for the filter being calculated.
    :return: the part count base hazard rate for the active environment.
    :rtype: float
    :raises: IndexError if passed an invalid environment ID.
    :raises: KeyError if passed an invalid type ID.
    """
    _environment_id = attributes["environment_active_id"]
    _type_id = attributes["type_id"]

    try:
        return PART_COUNT_LAMBDA_B[_type_id][_environment_id - 1]
    except IndexError:
        raise IndexError(
            f"get_part_count_lambda_b: Invalid electronic filter environment "
            f"ID {_environment_id}."
        )
    except KeyError:
        raise KeyError(
            f"get_part_count_lambda_b: Invalid electronic filter type ID {_type_id}."
        )


def get_part_stress_lambda_b(attributes: Dict[str, Union[float, int, str]]) -> float:
    """Retrieve the base hazard rate for part stress calculations.

    :param attributes: the attributes for the filter being calculated.
    :return: the base hazard rate for the filter.
    :rtype: float
    :raises: KeyError if passed an invalid type ID.
    """
    _type_id = attributes["type_id"]

    try:
        return PART_STRESS_LAMBDA_B[_type_id]
    except KeyError:
        raise KeyError(
            f"get_part_stress_lambda_b: Invalid electronic filter type ID {_type_id}."
        )


def set_default_values(
    **attributes: Dict[str, Union[float, int, str]],
) -> Dict[str, Union[float, int, str]]:
    """Set the default value of various parameters.

    :param attributes: the attribute dict for the electronic filter being calculated.
    :return: attributes; the updated attribute dict.
    :rtype: dict
    """
    if attributes.get("quality_id", 0) <= 0:
        attributes["quality_id"] = 1

    return attributes
