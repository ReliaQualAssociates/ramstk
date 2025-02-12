# type: ignore
# -*- coding: utf-8 -*-
#
#       ramstk.analyses.milhdbk217f.models.relay.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Relay MIL-HDBK-217F Calculations Module."""

# Standard Library Imports
from math import exp
from typing import Dict, Union

# RAMSTK Package Imports
from ramstk.constants.relay import (
    PART_COUNT_LAMBDA_B,
    PART_COUNT_PI_Q,
    PART_STRESS_PI_Q,
    PI_C,
    PI_E,
    PI_F,
)


def calculate_part_stress(
    attributes: Dict[str, Union[float, int, str]]
) -> Dict[str, Union[float, int, str]]:
    """Calculate the part stress hazard rate for a relay.

    This function calculates the MIL-HDBK-217F hazard rate using the part stress method.

    :param attributes: the hardware attributes dict for the relay being calculated.
    :return: the hardware attributes dict with updated values.
    :rtype: dict
    :raises: KeyError if the attribute dict is missing one or more keys.
    """
    try:
        attributes["piCYC"] = _calculate_cycling_factor(
            attributes["quality_id"], attributes["n_cycles"]
        )
        attributes["piL"] = _calculate_load_stress_factor(
            attributes["technology_id"], attributes["current_ratio"]
        )
        attributes["piF"] = _get_application_construction_factor(
            attributes["quality_id"],
            attributes["contact_rating_id"],
            attributes["construction_id"],
            attributes["application_id"],
        )

        if attributes["subcategory_id"] == 1:
            attributes["piC"] = PI_C[attributes["subcategory_id"]][
                attributes["contact_form_id"] - 1
            ]
            attributes["hazard_rate_active"] = (
                attributes["hazard_rate_active"]
                * attributes["piL"]
                * attributes["piC"]
                * attributes["piCYC"]
                * attributes["piF"]
            )

        return attributes
    except KeyError as err:
        raise KeyError(
            f"calculate_part_stress: Missing required relay attribute: {err}."
        )


def calculate_part_stress_lambda_b(
    attributes: Dict[str, Union[float, int, str]]
) -> float:
    """Calculate the base hazard rate for the relay.

    :param attributes: the hardware attributes dict for the relay being calculated.
    :return: the calculated part stress base hazard rate or 0.0 if passed an invalid
        subcategory ID.
    :rtype: float
    :raises: IndexError when passed an invalid type ID.
    :raises: KeyError when passed an invalid subcategory ID.
    """
    _subcategory_id = attributes["subcategory_id"]
    _temperature_active = attributes["temperature_active"]
    _type_id = attributes["type_id"]

    _dic_factors = {
        1: [[0.00555, 352.0, 15.7], [0.0054, 377.0, 10.4]],
        2: [0.4, 0.5, 0.5],
    }
    _lambda_b = 0.0

    try:
        if _subcategory_id == 1:
            _f0, _f1, _f2 = _dic_factors[_subcategory_id][_type_id - 1]
            return _f0 * exp(((_temperature_active + 273.0) / _f1) ** _f2)
        elif _subcategory_id == 2:
            return _dic_factors[_subcategory_id][_type_id - 1]
        else:
            raise KeyError(
                f"calculate_part_stress_lambda_b: Invalid relay subcategory "
                f"ID {_subcategory_id}."
            )
    except IndexError:
        raise IndexError(
            f"calculate_part_stress_lambda_b: Invalid relay type ID {_type_id}."
        )


def get_environment_factor(attributes: Dict[str, Union[float, int, str]]) -> float:
    """Retrieve the environment factor (piE) for the passed environment ID.

    :param attributes: the hardware attributes dict for the relay being calculated.
    :return: the selected environment factor (pIE).
    :rtype: float
    :raises: IndexError if passed an invalid active environment ID.
    :raises: KeyError if passed an invalid subcategory ID.
    """
    _environment_active_id = attributes["environment_active_id"]
    _quality_id = attributes["quality_id"]
    _subcategory_id = attributes["subcategory_id"]
    _quality = 1 if _quality_id in {1, 2, 3, 4, 5, 6} else 2

    try:
        return (
            PI_E[_subcategory_id][_quality][_environment_active_id - 1]
            if _subcategory_id == 1
            else PI_E[_subcategory_id][_environment_active_id - 1]
        )
    except IndexError:
        raise IndexError(
            f"get_environment_factor: Invalid relay environment ID "
            f"{_environment_active_id}."
        )
    except KeyError:
        raise KeyError(
            f"get_environment_factor: Invalid relay subcategory ID "
            f"{_subcategory_id}."
        )


def get_part_count_lambda_b(attributes: Dict[str, Union[float, int, str]]) -> float:
    """Retrieve the parts count base hazard rate (lambda b) from MIL-HDBK-217F.

    This function calculates the MIL-HDBK-217F hazard rate using the parts
    count method.

    This function calculates the MIL-HDBK-217F hazard rate using the parts
    count method.  The dictionary PART_COUNT_217F_LAMBDA_B contains the
    MIL-HDBK-217F parts count base hazard rates.  Keys are for
    PART_COUNT_217F_LAMBDA_B are:

        #. subcategory_id
        #. environment_active_id
        #. type id; if the relay subcategory is NOT type dependent, then
            the second key will be zero.

    Current subcategory IDs are:

    +----------------+-------------------------------+-----------------+
    | Subcategory    |              Relay            | MIL-HDBK-217F   |
    |       ID       |              Style            |    Section      |
    +================+===============================+=================+
    |        1       | Mechanical                    |       13.1      |
    +----------------+-------------------------------+-----------------+
    |        2       | Solid State                   |       13.2      |
    +----------------+-------------------------------+-----------------+

    :param attributes: the hardware attributes dict for the relay being calculated.
    :return: the parts count base hazard rate.
    :rtype: float
    :raise: IndexError if passed an unknown active environment ID.
    :raise: KeyError if passed an unknown subcategory ID or type ID.
    """
    _environment_active_id = attributes["environment_active_id"]
    _subcategory_id = attributes["subcategory_id"]
    _type_id = attributes["type_id"]

    try:
        return PART_COUNT_LAMBDA_B[_subcategory_id][_type_id][
            _environment_active_id - 1
        ]
    except IndexError:
        raise IndexError(
            f"get_part_count_lambda_b: Invalid relay environment ID "
            f"{_environment_active_id}."
        )
    except KeyError:
        raise KeyError(
            f"get_part_count_lambda_b: Invalid relay subcategory ID "
            f"{_subcategory_id} or type ID {_type_id}."
        )


def get_part_count_quality_factor(
    attributes: Dict[str, Union[float, int, str]]
) -> float:
    """Retrieve the quality factor (piQ) for the passed quality ID.

    :param attributes: the hardware attributes dict for the relay being calculated.
    :return: the quality factor (piQ) for the passed quality ID.
    :rtype: float
    :raises: IndexError if passed an invalid quality ID.
    :raises: KeyError if passed an invalid subcategory ID.
    """
    _quality_id = attributes["quality_id"]
    _subcategory_id = attributes["subcategory_id"]

    try:
        return PART_COUNT_PI_Q[_subcategory_id][_quality_id - 1]
    except IndexError:
        raise IndexError(
            f"get_part_count_quality_factor: Invalid relay quality ID {_quality_id}."
        )
    except KeyError:
        raise KeyError(
            f"get_part_count_quality_factor: Invalid relay subcategory ID "
            f"{_subcategory_id}."
        )


def get_part_stress_quality_factor(
    attributes: Dict[str, Union[float, int, str]]
) -> float:
    """Retrieve the part stress quality factor (piQ) for the passed quality ID.

    :param attributes: the hardware attributes dict for the relay to be calculated.
    :return: the quality factor (piQ) for the passed quality ID.
    :rtype: float
    :raises: IndexError when passed an invalid quality ID.
    :raises: KeyError when passed an invalid subcategory ID.
    """
    _quality_id = attributes["quality_id"]
    _subcategory_id = attributes["subcategory_id"]

    try:
        return PART_STRESS_PI_Q[_subcategory_id][_quality_id - 1]
    except IndexError:
        raise IndexError(
            f"get_part_stress_quality_factor: Invalid relay quality ID {_quality_id}."
        )
    except KeyError:
        raise KeyError(
            f"get_part_stress_quality_factor: Invalid relay subcategory "
            f"ID {_subcategory_id}."
        )


def set_default_values(
    attributes: Dict[str, Union[float, int, str]],
) -> Dict[str, Union[float, int, str]]:
    """Set the default value of various parameters.

    The subcategory ID and the type ID must be set for default values to be applied.

    :param attributes: the attribute dict for the relay being calculated.
    :return: attributes; the updated attribute dict.
    :rtype: dict
    """
    if attributes["quality_id"] <= 0:
        attributes["quality_id"] = _set_default_quality(attributes["subcategory_id"])

    if attributes["current_ratio"] <= 0.0:
        attributes["current_ratio"] = 0.5

    attributes["technology_id"] = _set_default_load_type(
        attributes["technology_id"], attributes["type_id"]
    )

    attributes["contact_form_id"] = _set_default_contact_form(
        attributes["contact_form_id"], attributes["type_id"]
    )

    attributes["contact_rating_id"] = _set_default_contact_rating(
        attributes["contact_rating_id"], attributes["type_id"]
    )

    attributes["application_id"] = _set_default_application(
        attributes["application_id"], attributes["type_id"]
    )

    attributes["construction_id"] = _set_default_construction(
        attributes["construction_id"], attributes["type_id"]
    )

    attributes["duty_cycle"] = _set_default_duty_cycle(
        attributes["duty_cycle"], attributes["type_id"]
    )

    attributes["temperature_rated_max"] = _set_default_rated_temperature(
        attributes["temperature_rated_max"], attributes["type_id"]
    )

    return attributes


def _calculate_cycling_factor(
    quality_id: int,
    n_cycles: float,
) -> float:
    """Calculate the cycling factor (piCYC) for the relay.

    :param quality_id: the quality level identifier.
    :param n_cycles: the number of relay cycles per hour in application.
    :return: _pi_cyc; the calculated cycling factor.
    :rtype: float
    """
    if quality_id in {1, 2, 3, 4, 5, 6} and n_cycles < 1.0:
        return 0.1
    elif quality_id == 7 and n_cycles > 1000.0:
        return (n_cycles / 100.0) ** 2.0
    elif quality_id == 7 and 10.0 < n_cycles < 1000.0:
        return n_cycles / 10.0
    else:
        return 0.0


def _calculate_load_stress_factor(
    technology_id: int,
    current_ratio: float,
) -> float:
    """Calculate the load stress factor (piL).

    Only subcategory 1 relays use this in their calculation.

    :param technology_id: the relay technology identifier.
    :param current_ratio: the operating current ratio of the relay.
    :return: _pi_l; the calculated value of piL.
    :rtype: float
    """
    if technology_id == 1:
        return (current_ratio / 0.8) ** 2.0
    elif technology_id == 2:
        return (current_ratio / 0.4) ** 2.0
    elif technology_id == 3:
        return (current_ratio / 0.2) ** 2.0
    else:
        return 0.0


def _get_application_construction_factor(
    quality_id: int,
    contact_rating_id: int,
    construction_id: int,
    application_id: int,
) -> float:
    """Calculate the construction factor (piF) for the relay.

    :param quality_id: the quality level identifier.
    :param contact_rating_id: the relay contact current rating identifier.
    :param construction_id: the relay construction identifier.
    :param application_id: the relay application identifier.
    :return: _pi_f; the selected application factor.
    :rtype: float
    :raises: KeyError if passed an invalid contact rating ID, construction ID, or
        application ID.
    """
    _quality = 1 if quality_id in {1, 2, 3, 4, 5, 6} else 2

    try:
        return PI_F[contact_rating_id][application_id][construction_id][_quality - 1]
    except KeyError:
        raise KeyError(
            f"_get_application_construction_factor: Invalid relay application "
            f"ID {application_id}, contact rating ID {contact_rating_id}, construction "
            f"ID {construction_id}."
        )


def _set_default_quality(subcategory_id: int) -> int:
    """Set the default quality for mechanical relays.

    :param subcategory_id: the subcategory ID of the relay with missing defaults.
    :return: _quality_id
    :rtype: float
    """
    return 5 if subcategory_id == 4 else 1


def _set_default_load_type(technology_id: int, type_id: int) -> int:
    """Set the default max rated temperature for mechanical relays.

    :param technology_id: the current technology ID (represents the load type).
    :param type_id: the type ID of the relay with missing defaults.
    :return: _contact_form_id
    :rtype: int
    """
    if technology_id > 0:
        return technology_id
    return 1 if type_id in {1, 3, 4, 6} else 2


def _set_default_contact_form(contact_form_id: int, type_id: int) -> int:
    """Set the default contact form for mechanical relays.

    :param contact_form_id: the current contact form ID.
    :param type_id: the type ID of the relay with missing defaults.
    :return: _contact_form_id
    :rtype: int
    """
    if contact_form_id > 0:
        return contact_form_id
    return 1 if type_id in {4, 5} else 6


def _set_default_contact_rating(contact_rating_id: int, type_id: int) -> int:
    """Set the default contact rating for mechanical relays.

    :param contact_form_id: the current contact rating ID.
    :param type_id: the type ID of the relay with missing defaults.
    :return: contact_rating_id
    :rtype: int
    """
    if contact_rating_id > 0:
        return contact_rating_id
    return {1: 2, 2: 4, 3: 2, 4: 1, 5: 2, 6: 2}[type_id]


def _set_default_application(application_id: int, type_id: int) -> int:
    """Set the default application for mechanical relays.

    :param application_id: the current application ID.
    :param type_id: the type ID of the relay with missing defaults.
    :return: application_id
    :rtype: int
    """
    if application_id > 0:
        return application_id
    return {1: 1, 2: 1, 3: 8, 4: 1, 5: 6, 6: 3}[type_id]


def _set_default_construction(construction_id: int, type_id: int) -> int:
    """Set the default construction for mechanical relays.

    :param construction_id: the current construction ID.
    :param type_id: the type ID of the relay with missing defaults.
    :return: construction_id
    :rtype: int
    """
    if construction_id > 0:
        return construction_id
    return {1: 2, 2: 4, 3: 2, 4: 2, 5: 1, 6: 2}[type_id]


def _set_default_duty_cycle(duty_cycle: float, type_id: int) -> float:
    """Set the default max rated temperature for mechanical relays.

    :param duty_cycle: the current duty cycle.
    :param type_id: the type ID of the relay with missing defaults.
    :return: _duty_cycle
    :rtype: float
    """
    if duty_cycle > 0.0:
        return duty_cycle
    return 20.0 if type_id == 4 else 10.0


def _set_default_rated_temperature(rated_temperature_max: float, type_id: int) -> float:
    """Set the default max rated temperature for mechanical relays.

    :param rated_temperature_max: the current maximum rated temperature.
    :param type_id: the type ID of the relay with missing defaults.
    :return: _rated_temperature_max
    :rtype: float
    """
    if rated_temperature_max > 0.0:
        return rated_temperature_max
    return 85.0 if type_id == 4 else 125.0
