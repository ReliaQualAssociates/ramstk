# type: ignore
# -*- coding: utf-8 -*-
#
#       ramstk.analyses.milhdbk217f.models.switch.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Switch Reliability Calculations Module."""

# Standard Library Imports
from math import exp
from typing import Dict, List, Union

# RAMSTK Package Imports
from ramstk.constants.switch import (
    PART_COUNT_LAMBDA_B,
    PART_COUNT_LAMBDA_B_BREAKER,
    PART_COUNT_PI_Q,
    PART_STRESS_LAMBDA_B_BREAKER,
    PART_STRESS_LAMBDA_B_TOGGLE,
    PART_STRESS_PI_Q,
    PI_C,
    PI_E,
)


def calculate_part_stress(
    attributes: Dict[str, Union[float, int, str]]
) -> Dict[str, Union[float, int, str]]:
    """Calculate the part stress active hazard rate for a switch.

    This function calculates the MIL-HDBK-217FN2 hazard rate using the part stress
    method.

    :param attributes: the hardware attributes dict for the switch being calculated.
    :return attributes: the updated hardware attributes dict.
    :rtype: dict
    :raises: KeyError when the hardware attributes dict is missing one or more keys.
    """
    try:
        attributes["piL"] = calculate_load_stress_factor(
            attributes["application_id"],
            attributes["current_ratio"],
        )

        # Determine the contact form and quantity factor (piC).
        if attributes["subcategory_id"] in [1, 5]:
            attributes["piC"] = PI_C[attributes["subcategory_id"]][
                attributes["contact_form_id"]
            ]

        # Determine the cycling factor (piCYC).
        if attributes["n_cycles"] > 1:
            attributes["piCYC"] = float(attributes["n_cycles"])

        # Determine the use factor (piU).
        attributes["piU"] = 10.0 if attributes["application_id"] - 1 else 1.0

        attributes["hazard_rate_active"] = (
            attributes["hazard_rate_active"] / attributes["piQ"]
        )
        if attributes["subcategory_id"] == 1:
            attributes["hazard_rate_active"] = (
                attributes["hazard_rate_active"]
                * attributes["piCYC"]
                * attributes["piL"]
                * attributes["piC"]
            )
        elif attributes["subcategory_id"] in [2, 3, 4]:
            attributes["hazard_rate_active"] = (
                attributes["hazard_rate_active"]
                * attributes["piCYC"]
                * attributes["piL"]
            )
        elif attributes["subcategory_id"] == 5:
            attributes["hazard_rate_active"] = (
                attributes["hazard_rate_active"]
                * attributes["piC"]
                * attributes["piU"]
                * attributes["piQ"]
            )

        return attributes
    except KeyError as err:
        raise KeyError(
            f"calculate_part_stress: Missing required switch attribute: {err}."
        )


def calculate_load_stress_factor(
    application_id: int,
    current_ratio: float,
) -> float:
    """Calculate the load stress factor (piL).

    :param application_id: the switch application ID.
    :param current_ratio: the ratio of switch operating to switch rated current.
    :return: the calculated load stress factor (piL).
    :rtype: float
    """
    _pi_l = 0.0

    if application_id == 1:  # Resistive
        _pi_l = exp((current_ratio / 0.8) ** 2.0)
    elif application_id == 2:  # Inductive
        _pi_l = exp((current_ratio / 0.4) ** 2.0)
    elif application_id == 3:  # Capacitive
        _pi_l = exp((current_ratio / 0.2) ** 2.0)

    return _pi_l


def calculate_part_stress_lambda_b(
    attributes: Dict[str, Union[float, int, str]]
) -> float | None:
    """Calculate the part stress base hazard rate (lambda b).

    This function calculates the MIL-HDBK-217FN2 base hazard rate for the parts stress
    method.

    :param attributes: the hardware attributes dict for the switch being calculated.
    :return: the calculated part stress base hazard rate (lambdaB).
    :rtype: float
    :raises: IndexError when passed an invalid application ID or quality ID.
    :raises: KeyError when passed an invalid construction ID or subcategory ID.
    """
    _application_id: int = attributes["application_id"]
    _construction_id: int = attributes["construction_id"]
    _n_elements: int = attributes["n_elements"]
    _quality_id: int = attributes["quality_id"]
    _subcategory_id: int = attributes["subcategory_id"]

    _dic_factors: Dict[int, List[List[float]]] = {
        2: [[0.1, 0.00045, 0.0009], [0.1, 0.23, 0.63]],
        3: [[0.0067, 0.00003, 0.00003], [0.1, 0.02, 0.06]],
        4: [[0.0067, 0.062], [0.086, 0.089]],
    }

    try:
        if _subcategory_id == 1:
            return PART_STRESS_LAMBDA_B_TOGGLE[_construction_id][_quality_id - 1]
        elif _subcategory_id in {2, 3}:
            _lambda_be, _lambda_bc, _lambda_b0 = _dic_factors[_subcategory_id][
                _quality_id - 1
            ]
            return (
                _lambda_be + _n_elements * _lambda_bc
                if _construction_id == 1
                else _lambda_be + _n_elements * _lambda_b0
            )

        elif _subcategory_id == 4:
            _lambda_b1, _lambda_b2 = _dic_factors[_subcategory_id][_quality_id - 1]
            return _lambda_b1 + _n_elements * _lambda_b2
        elif _subcategory_id == 5:
            return PART_STRESS_LAMBDA_B_BREAKER[_application_id - 1]
    except IndexError:
        raise IndexError(
            f"calculate_part_stress_lambda_b: Invalid switch application "
            f"ID {_application_id} or quality ID {_quality_id}."
        )
    except KeyError:
        raise KeyError(
            f"calculate_part_stress_lambda_b: Invalid switch construction "
            f"ID {_construction_id} or subcategory ID {_subcategory_id}."
        )


def get_environment_factor(attributes: Dict[str, Union[float, int, str]]) -> float:
    """Retrieve the environment factor (piE) for the passed environment ID.

    :param attributes: the hardware attributes dict for the switch being calculated.
    :return: the selected environment factor (pIE).
    :rtype: float
    :raises: IndexError when passed an invalid environment ID.
    :raises: KeyError when passed an invalid subcategory ID.
    """
    _environment_active_id = attributes["environment_active_id"]
    _subcategory_id = attributes["subcategory_id"]

    try:
        return PI_E[_subcategory_id][_environment_active_id - 1]
    except IndexError:
        raise IndexError(
            f"get_environment_factor: Invalid switch environment "
            f"ID {_environment_active_id}."
        )
    except KeyError:
        raise KeyError(
            f"get_environment_factor: Invalid switch subcategory "
            f"ID {_subcategory_id}."
        )


def get_part_count_lambda_b(attributes: Dict[str, Union[float, int, str]]) -> float:
    """Retrieve the part count base hazard rate (lambdaB).

    This function retrieves the MIL-HDBK-217FN2 part count base hazard rate.  The
    dictionary PART_COUNT_LAMBDA_B contains the MIL-HDBK-217FN2 part count base
    hazard rates.  Keys for PART_COUNT_LAMBDA_B are:

        #. subcategory_id
        #. environment_active_id
        #. construction_id; if the switch subcategory is construction dependent.

    Current subcategory IDs are:

    +----------------+-------------------------------+-----------------+
    | Subcategory    |             Switch            | MIL-HDBK-217F   |
    |       ID       |              Style            |    Section      |
    +================+===============================+=================+
    |        1       | Toggle or Pushbutton          |       15.1      |
    +----------------+-------------------------------+-----------------+
    |        2       | Sensitive                     |       15.2      |
    +----------------+-------------------------------+-----------------+
    |        3       | Rotary                        |       15.3      |
    +----------------+-------------------------------+-----------------+
    |        4       | Thumbwheel                    |       16.1      |
    +----------------+-------------------------------+-----------------+
    |        5       | Circuit Breaker               |       17.1      |
    +----------------+-------------------------------+-----------------+

    :param attributes: the hardware attributes dict for the switch being calculated.
    :return: the selected part count base hazard rate (lambdaB).
    :rtype: float
    :raise: IndexError when passed an invalid active environment ID.
    :raise: KeyError when passed an invalid construction ID or  subcategory ID.
    """
    _construction_id = attributes["construction_id"]
    _environment_active_id = attributes["environment_active_id"]
    _subcategory_id = attributes["subcategory_id"]

    try:
        return (
            PART_COUNT_LAMBDA_B_BREAKER[_construction_id][_environment_active_id - 1]
            if _subcategory_id == 5
            else PART_COUNT_LAMBDA_B[_subcategory_id][_environment_active_id - 1]
        )
    except IndexError:
        raise IndexError(
            f"get_part_count_lambda_b: Invalid switch environment ID "
            f"{_environment_active_id}."
        )
    except KeyError:
        raise KeyError(
            f"get_part_count_lambda_b: Invalid switch construction ID "
            f"{_construction_id} or subcategory ID {_subcategory_id}."
        )


def get_part_count_quality_factor(
    attributes: Dict[str, Union[float, int, str]]
) -> float:
    """Retrieve the part count quality factor (piQ) for the passed quality ID.

    :param attributes: the hardware attributes dict for the switch being calculated.
    :return: the selected part count quality factor (piQ).
    :rtype: float
    :raises: IndexError when passed an invalid quality ID.
    :raises: KeyError when passed an invalid subcategory ID.
    """
    _quality_id = attributes["quality_id"]
    _subcategory_id = attributes["subcategory_id"]

    try:
        return PART_COUNT_PI_Q[_subcategory_id][_quality_id - 1]
    except IndexError:
        raise IndexError(
            f"get_part_count_quality_factor: Invalid switch quality ID {_quality_id}."
        )
    except KeyError:
        raise KeyError(
            f"get_part_count_quality_factor: Invalid switch subcategory "
            f"ID {_subcategory_id}."
        )


def get_part_stress_quality_factor(
    attributes: Dict[str, Union[float, int, str]]
) -> float:
    """Retrieve the part stress quality factor (piQ) for the passed quality ID.

    :param attributes: the hardware attributes dict for the switch being calculated.
    :return: the selected part stress quality factor (piQ).
    :rtype: float
    :raises: IndexError when passed an invalid quality ID.
    """
    _quality_id = attributes["quality_id"]
    _subcategory_id = attributes["subcategory_id"]

    try:
        if _subcategory_id == 5:
            return PART_STRESS_PI_Q[_quality_id - 1]
        else:
            return 1.0
    except IndexError:
        raise IndexError(
            f"get_part_stress_quality_factor: Invalid switch quality ID {_quality_id}."
        )


def set_default_values(
    attributes: Dict[str, Union[float, int, str]],
) -> Dict[str, Union[float, int, str]]:
    """Set the default value for various switch parameters.

    :param attributes: the hardware attributes dict for the switch being calculated.
    :return: the updated hardware attributes dict.
    :rtype: dict
    """
    attributes["piC"] = 1.0
    attributes["piCYC"] = 1.0

    if attributes["application_id"] <= 0:
        attributes["application_id"] = 1

    if attributes["quality_id"] <= 0:
        attributes["quality_id"] = 1

    if attributes["current_ratio"] < 0.0:
        attributes["current_ratio"] = 0.5

    attributes["construction_id"] = _set_default_construction_id(
        attributes["construction_id"],
        attributes["subcategory_id"],
    )

    attributes["contact_form_id"] = _set_default_contact_form_id(
        attributes["contact_form_id"],
        attributes["subcategory_id"],
    )

    attributes["n_cycles"] = _set_default_cycle_rate(
        attributes["n_cycles"],
        attributes["subcategory_id"],
    )

    attributes["n_elements"] = _set_default_active_contacts(
        attributes["n_elements"],
        attributes["subcategory_id"],
    )

    return attributes


def _set_default_construction_id(construction_id: int, subcategory_id: int) -> int:
    """Set the default construction ID.

    :param construction_id: the current switch construction ID.
    :param subcategory_id: the switch subcategory ID.
    :return: the default construction ID.
    :rtype: int
    """
    if construction_id > 0:
        return construction_id

    try:
        return {
            1: 1,
            2: 1,
        }[subcategory_id]
    except KeyError:
        return 0


def _set_default_contact_form_id(contact_form_id: int, subcategory_id: int) -> int:
    """Set the default contact form ID.

    :param contact_form_id: the current switch contact form ID.
    :param subcategory_id: the switch subcategory ID.
    :return: the default contact form ID.
    :rtype: int
    """
    if contact_form_id > 0:
        return contact_form_id

    try:
        return {
            1: 2,
            5: 3,
        }[subcategory_id]
    except KeyError:
        return 0


def _set_default_cycle_rate(cycle_rate: float, subcategory_id: int) -> float:
    """Set the default cycling rate.

    :param cycle_rate: the current switch cycling rate.
    :param subcategory_id: the switch subcategory ID.
    :return: the default number of hourly cycles.
    :rtype: float
    """
    if cycle_rate > 0.0:
        return cycle_rate

    try:
        return {
            1: 1.0,
            2: 1.0,
            3: 30.0,
            4: 1.0,
        }[subcategory_id]
    except KeyError:
        return 0.0


def _set_default_active_contacts(active_contacts: int, subcategory_id: int) -> int:
    """Set the default active number of contacts.

    :param active_contacts: the current switch active number of contacts.
    :param subcategory_id: the switch subcategory ID.
    :return: the default number of active contacts.
    :rtype: float
    """
    if active_contacts > 0:
        return active_contacts

    try:
        return {
            2: 1,
            3: 24,
            4: 6,
        }[subcategory_id]
    except KeyError:
        return 0
