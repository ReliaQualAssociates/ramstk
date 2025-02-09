# type: ignore
# -*- coding: utf-8 -*-
#
#       ramstk.analyses.milhdk217f.models.inductor.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Inductor MIL-HDBK-217F Constants and Calculations Module."""

# Standard Library Imports
from math import exp
from typing import Dict, Union

# RAMSTK Package Imports
from ramstk.constants.inductor import (
    PART_COUNT_LAMBDA_B,
    PART_COUNT_PI_Q,
    PART_STRESS_PI_Q,
    PI_E,
    REF_TEMPS,
)


def calculate_part_stress(
    attributes: Dict[str, Union[float, int, str]]
) -> Dict[str, Union[float, int, str]]:
    """Calculate the part stress hazard rate for an inductive device.

    This function calculates the MIL-HDBK-217F hazard rate using the part stress method.

    :param attributes: the dict containing the inductive device hardware attributes.
    :return: attributes; the hardware attribute dict with updated values.
    :rtype: dict
    """
    attributes["piC"] = float(attributes["construction_id"])

    _power_input = attributes["voltage_dc_operating"] * attributes["current_operating"]
    if attributes["subcategory_id"] == 2 and attributes["specification_id"] == 2:
        attributes["temperature_rise"] = get_temperature_rise_spec_sheet(
            int(attributes["page_number"])
        )
    elif attributes["power_operating"] > 0.0 and attributes["area"] > 0.0:
        attributes["temperature_rise"] = calculate_temperature_rise_power_loss_surface(
            attributes["power_operating"], attributes["area"]
        )
    elif attributes["power_operating"] > 0.0 and attributes["weight"] > 0.0:
        attributes["temperature_rise"] = calculate_temperature_rise_power_loss_weight(
            attributes["power_operating"], attributes["weight"]
        )
    elif _power_input > 0.0 and attributes["weight"] > 0.0:
        attributes["temperature_rise"] = calculate_temperature_rise_input_power_weight(
            _power_input, attributes["weight"]
        )
    else:
        attributes["temperature_rise"] = 0.0
    attributes["temperature_hot_spot"] = calculate_hot_spot_temperature(
        attributes["temperature_active"], attributes["temperature_rise"]
    )

    attributes["lambda_b"] = calculate_part_stress_lambda_b(attributes)

    attributes["hazard_rate_active"] = (
        attributes["lambda_b"] * attributes["piQ"] * attributes["piE"]
    )
    if attributes["subcategory_id"] == 2:
        attributes["hazard_rate_active"] = (
            attributes["hazard_rate_active"] * attributes["piC"]
        )

    return attributes


def calculate_hot_spot_temperature(
    temperature_active: float,
    temperature_rise: float,
) -> float:
    """Calculate the coil or transformer hot spot temperature.

    :return: _temperature_hot_spot; the calculated hot spot temperature.
    :rtype: float
    """
    return temperature_active + 1.1 * temperature_rise


def calculate_part_stress_lambda_b(
    attributes: Dict[str, Union[float, int, str]]
) -> float:
    """Calculate part stress base hazard rate (lambda b) from MIL-HDBK-217F.

    This function calculates the MIL-HDBK-217F hazard rate using the parts stress
    method.

    :param attributes: the dict containing the inductive device hardware attributes.
    :return: _lambda_b; the calculated parts stress lambda_b.
    :rtype: float
    :raises: KeyError when passed an unknown subcategory ID or insulation ID.
    """
    _insulation_id: int = attributes["insulation_id"]
    _subcategory_id: int = attributes["subcategory_id"]
    _temperature_hot_spot: float = attributes["temperature_hot_spot"]

    _dic_factors = {
        1: {
            1: [0.0018, 15.6],
            2: [0.002, 14.0],
            3: [0.0018, 8.7],
            4: [0.002, 10.0],
            5: [0.00125, 3.8],
            6: [0.00159, 8.4],
        },
        2: {
            1: [0.000335, 15.6],
            2: [0.000379, 14.0],
            3: [0.000319, 8.7],
            4: [0.00035, 10.0],
        },
    }

    try:
        _ref_temp = REF_TEMPS[_subcategory_id][_insulation_id]
        _f0 = _dic_factors[_subcategory_id][_insulation_id][0]
        _f1 = _dic_factors[_subcategory_id][_insulation_id][1]
        return _f0 * exp(((_temperature_hot_spot + 273.0) / _ref_temp) ** _f1)
    except KeyError:
        raise KeyError(
            f"calculate_part_stress_lambda_b: Invalid subcategory ID {_subcategory_id} "
            f"or insulation ID {_insulation_id}."
        )


def calculate_temperature_rise_input_power_weight(
    power_input: float,
    weight: float,
) -> float:
    """Calculate the temperature rise based on input power and xfmr weight.

    .. attention:: input power must be calculated by the calling function from
    voltage and current as it is not an attribute of an inductive device.

    :param power_input: the input power in W.
    :param weight: the weight of the xfmr in lbf.
    :returm: _temperature_rise; the calculated temperature rise in C.
    :rtype: float
    :raises: ZeroDivisionError if passed a weight=0.0.
    """
    try:
        return 2.1 * (power_input / weight**0.6766)
    except ZeroDivisionError:
        raise ZeroDivisionError(
            "calculate_temperature_rise_input_power_weight: Inductive device weight "
            "may not be zero."
        )


def calculate_temperature_rise_power_loss_surface(
    power_operating: float,
    area: float,
) -> float:
    """Calculate the temperature rise based on the power loss and surface area.

    :param power_operating: the power loss in W.
    :param area: the radiating surface area of the case in sq. inches.
    :return: _temperature_rise; the calculated temperature rise in C.
    :rtype: float
    :raises: ZeroDivisionError if passed an area=0.0.
    """
    try:
        return 125.0 * power_operating / area
    except ZeroDivisionError:
        raise ZeroDivisionError(
            "calculate_temperature_rise_power_loss_surface: Inductive device area "
            "must not be zero."
        )


def calculate_temperature_rise_power_loss_weight(
    power_operating: float,
    weight: float,
) -> float:
    """Calculate the temperature rise based on the power loss and xfmr weight.

    :param power_operating: the power loss in W.
    :param weight: the weight of the device in lbf.
    :return: _temperature_rise; the calculated temperature rise in C.
    :rtype: float
    :raises: ZeroDivisionError if passed a weight=0.0.
    """
    try:
        return 11.5 * (power_operating / weight**0.6766)
    except ZeroDivisionError:
        raise ZeroDivisionError(
            "calculate_temperature_rise_power_loss_weight: Inductive device weight "
            "may not be zero."
        )


def get_environment_factor(attributes: Dict[str, Union[float, int, str]]) -> float:
    """Retrieve the environment factor (piE) for the passed environment ID.

    :param attributes: the dict containing the inductive device hardware attributes.
    :return: the environment factor for the passed environment ID.
    :rtype: float
    :raises: IndexError if passed an invalid environment ID.
    :raises: KeyError if passed an invalid subcategory ID.
    """
    _environment_id: int = attributes["environment_active_id"]
    _subcategory_id: int = attributes["subcategory_id"]

    try:
        return PI_E[_subcategory_id][_environment_id - 1]
    except IndexError:
        raise IndexError(
            f"get_environment_factor: Invalid inductive device environment "
            f"ID {_environment_id}."
        )
    except KeyError:
        raise KeyError(
            f"get_environment_factor: Invalid inductive device subcategory "
            f"ID {_subcategory_id}."
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
        #. family id; if the inductor subcategory is NOT family dependent, then
            the second key will be zero.

    Current subcategory IDs are:

    +----------------+-------------------------------+-----------------+
    | Subcategory    |           Inductor            | MIL-HDBK-217F   |
    |       ID       |             Style             |    Section      |
    +================+===============================+=================+
    |        1       | Transformer                   |       11.1      |
    +----------------+-------------------------------+-----------------+
    |        2       | Coil                          |       11.2      |
    +----------------+-------------------------------+-----------------+

    These keys return a list of base hazard rates.  The hazard rate to use is
    selected from the list depending on the active environment.

    :param attributes: the dict containing the inductive device hardware attributes.
    :return: _base_hr; the part count base hazard rate.
    :rtype: float
    :raises: KeyError if passed an unknown subcategory ID or family ID.
    :raises: IndexError if passed an unknown active environment ID.
    """
    _environment_id = attributes["environment_active_id"]
    _family_id = attributes["family_id"]
    _subcategory_id = attributes["subcategory_id"]

    try:
        return PART_COUNT_LAMBDA_B[_subcategory_id][_family_id][_environment_id - 1]
    except IndexError:
        raise IndexError(
            f"get_part_count_lambda_b: Invalid inductive device environment "
            f"ID {_environment_id}."
        )
    except KeyError:
        raise KeyError(
            f"get_part_count_lambda_b: Invalid inductive device family "
            f"ID {_family_id} or subcategory ID {_subcategory_id}."
        )


def get_part_count_quality_factor(
    attributes: Dict[str, Union[float, int, str]]
) -> float:
    """Retrieve the quality factor (piQ) for the passed quality ID.

    :param attributes: the inductive device hardware attributes dict.
    :return: the value of the quality factor.
    :rtype: float
    :raises: IndexError when passed an invalid quality ID.
    """
    _quality_id = attributes["quality_id"]

    try:
        return PART_COUNT_PI_Q[_quality_id - 1]
    except IndexError:
        raise IndexError(
            f"get_part_count_quality_factor: Invalid inductive device quality "
            f"ID {_quality_id}."
        )


def get_part_stress_quality_factor(
    attributes: Dict[str, Union[float, int, str]]
) -> float:
    """Select the MIL-HDBK-217F quality factor for the inductive device.

    :param attributes: the dict containing the inductive device hardware attributes.
    :return: _pi_q; the selected quality factor
    :rtype: float
    :raises: IndexError if passed an unknown quality ID.
    :raises: KeyError if passed an unknown subcategory ID or family ID.
    """
    _family_id = attributes["family_id"]
    _quality_id = attributes["quality_id"]
    _subcategory_id = attributes["subcategory_id"]

    try:
        return (
            PART_STRESS_PI_Q[_subcategory_id][_family_id][_quality_id - 1]
            if _subcategory_id == 1
            else PART_STRESS_PI_Q[_subcategory_id][_quality_id - 1]
        )
    except IndexError:
        raise IndexError(
            f"get_part_stress_quality_factor: Invalid inductive device quality "
            f"ID {_quality_id}."
        )
    except KeyError:
        raise KeyError(
            f"get_part_stress_quality_factor: Invalid inductive device "
            f"family ID {_family_id} or subcategory ID {_subcategory_id}."
        )


def get_temperature_rise_spec_sheet(page_number: int) -> float:
    """Retrieve the temperature rise based on the spec sheet from MIL-C-39010.

    :param page_number: the spec sheet to retrieve the temperature rise for.
    :return: _temperature_rise; the spec sheet temperature rise.
    :rtype: float
    :raises: KeyError if an unknown spec sheet is passed.
    """
    try:
        return {
            1: 15.0,
            2: 15.0,
            3: 15.0,
            4: 35.0,
            5: 15.0,
            6: 35.0,
            7: 15.0,
            8: 35.0,
            9: 15.0,
            10: 15.0,
            11: 35.0,
            12: 35.0,
            13: 15.0,
            14: 15.0,
        }[page_number]
    except KeyError:
        raise KeyError(
            f"get_temperature_rise_spec_sheet: Invalid inductive device "
            f"page number {page_number}."
        )


def set_default_values(
    attributes: Dict[str, Union[float, int, str]],
) -> Dict[str, Union[float, int, str]]:
    """Set the default value of various parameters.

    :param attributes: the attribute dict for the inductove device being calculated.
    :return: attributes; the updated attribute dict.
    :rtype: dict
    """
    if attributes["rated_temperature_max"] <= 0.0:
        attributes["rated_temperature_max"] = _set_default_rated_temperature(
            attributes["subcategory_id"]
        )

    if attributes["temperature_rise"] <= 0.0:
        attributes["temperature_rise"] = _set_default_temperature_rise(
            attributes["subcategory_id"],
            attributes["family_id"],
        )

    return attributes


def _set_default_rated_temperature(subcategory_id: int) -> float:
    """Set the default maximum rated temperature.

    :param subcategory_id: the subcategory ID of the inductive device with missing
        defaults.
    :return: _rated_temperature_max
    :rtype: float
    """
    return 130.0 if subcategory_id == 1 else 125.0


def _set_default_temperature_rise(
    subcategory_id: int,
    family_id: int,
) -> float:
    """Set the default temperature rise.

    :param subcategory_id: the subcategory ID of the inductive device with missing
        defaults.
    :param family_id: the family ID of the inductive device with missing defaults.
    :return: _temperature_rise
    :rtype: float
    """
    return 30.0 if subcategory_id == 1 and family_id == 3 else 10.0
