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

    This function calculates the MIL-HDBK-217FN2 hazard rate using the part stress
    method.  Because the part stress model for a filter is simply the based hazard rate
    (lambdaB) multiplied by the environment factor (piE) and quality factor (piQ), this
    function only needs to return the hardware attributes dict as this calculation is
    performed in the milhdbk217f._do_calculate_part_stress() function.

    :param attributes: the hardware attributes dict for the filter being calculated.
    :return: the hardware attributes dict.
    :rtype: dict
    """
    return attributes


def get_environment_factor(attributes: Dict[str, Union[float, int, str]]) -> float:
    """Retrieve the environment factor (piE) for the passed environment ID.

    :param attributes: the hardware attributes dict for the filter being calculated.
    :return: the selected environment factor (pIE).
    :rtype: float
    :raises: IndexError when passed an invalid environment ID.
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
    """Retrieve the quality factor (piQ) for the passed quality ID.

    This function is used for both MIL-HDBK-217FN2 part count and part stress methods.

    :param attributes: the hardware attributes dict for the filter being calculated.
    :return: the selected quality factor (piQ).
    :rtype: float
    :raises: IndexError when passed an invalid quality ID.
    """
    _quality_id = attributes["quality_id"]

    try:
        return PI_Q[_quality_id - 1]
    except IndexError:
        raise IndexError(
            f"get_quality_factor: Invalid electronic filter quality ID {_quality_id}."
        )


def get_part_count_lambda_b(attributes: Dict[str, Union[float, int, str]]) -> float:
    """Retrieve the part count base hazard rate (lambdaB).

    This function retrieves the MIL-HDBK-217FN2 part count base hazard rate. The
    dictionary PART_COUNT_LAMBDA_B contains the MIL-HDBK-217FN2 part count base hazard
    rates.  The keys for PART_COUNT_LAMBDA_B are:

    #. type_id #. environment_active_id

    :param attributes: the hardware attributes dict for the filter being calculated.
    :return: the selected part count base hazard rate (lambdaB).
    :rtype: float
    :raises: IndexError when passed an invalid environment ID.
    :raises: KeyError when passed an invalid type ID.
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
    """Retrieve the part stress base hazard rate (lambdaB).

    This function retrieves the MIL-HDBK-217FN2 part stress base hazard rate.

    :param attributes: the attributes for the filter being calculated.
    :return: the selected part stress base hazard rate (lambdaB).
    :rtype: float
    :raises: KeyError when passed an invalid type ID.
    """
    _type_id = attributes["type_id"]

    try:
        return PART_STRESS_LAMBDA_B[_type_id]
    except KeyError:
        raise KeyError(
            f"get_part_stress_lambda_b: Invalid electronic filter type ID {_type_id}."
        )


def set_default_values(
    attributes: Dict[str, Union[float, int, str]],
) -> Dict[str, Union[float, int, str]]:
    """Set the default value for various electronic filter parameters.

    :param attributes: the hardware attributes dict for the electronic filter being
        calculated.
    :return: the updated hardware attributes dict.
    :rtype: dict
    """
    if attributes.get("quality_id", 0) <= 0:
        attributes["quality_id"] = 1

    return attributes
